"""Class for generating a list of customers from a given location"""

import logging
import os
import json
import collections

from math import radians, sin, cos, acos

class InviteGenerator():
    def __init__(self, distance, debug):
        self.customers_file = None
        self.output_file = None
        self.office_longitude = -6.257664
        self.office_latitude = 53.339428
        self.debug = debug 
        self.distance = float(distance)
        self.setup()


    def setup(self):
        """
        Setup Function
        """
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
        self.customers_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'customers.txt'
        )
        self.output_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'output.txt'
        )


    def run(self):
        """
        Main method of execution for the invite generator
        """
        logging.info('Getting customer data for input file: {}'.format(self.customers_file))
        customers_data = self._get_customers_data()
        logging.info('Getting customers within the given distance: {}'.format(self.distance))
        valid_customers = self._get_customers_within_range(customers_data)
        logging.info('Outputting results to console and writing to file')
        self._output_valid_customers(valid_customers)


    def _get_customers_within_range(self, customers_data):
        """
        Method to return all customers within range of the office valid for an invite
        :param customers_data:
        :return: Map
        """
        valid_customers = {}
        for customer in customers_data:
            data = customers_data[customer]
            customer_distance = self._get_great_circle_distance(
                data['long'], data['lat']
            )
            if customer_distance < self.distance:
                logging.info('Customer {} is within the given distance'.format(customer))
                valid_customers[customer] = {
                    'name': data['name']
                }
        return valid_customers


    def _get_great_circle_distance(self, longitude, latitude):
        """
        Mehtod to calculate the distance for given customers long and lat from the office
        :param longitude:
        :param latitude:
        :return: Int
        """
        c_long, c_lat, o_long, o_lat = map(
            radians, [longitude, latitude, self.office_longitude, self.office_latitude]
        )
        delta = acos(
            sin(c_lat) * sin(o_lat) + cos(c_lat) * cos(o_lat) * cos(c_long - o_long)
        )
        # Distance formula =  r *  delta where
        # delta = (sin(lat1)sin(lat2) + cos(lat1)cos(lat2)cos(long1-long2)) long & lat varibales are in radians
        # r = radius of the earth ~ 6371 km
        # See: https://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas
        distance = 6371 * delta
        return distance


    def _get_customers_data(self):
        """
        Helper methos to parse the customers data from the customers.txt file
        :return: Map
        """
        try:
            customer_data = {}
            with open(self.customers_file, 'r') as _file:
                for customer in _file:
                    data = json.loads(customer)
                    customer_data[data['user_id']] = {
                        'name': data['name'],
                        'lat': float(data['latitude']),
                        'long': float(data['longitude'])
                    }
        except Exception as ex:
            logging.exception('Error occured while trying to parse customer data')
            raise Exception
        return customer_data


    def _output_valid_customers(self, valid_customers):
        """
        Method to output valid data to the console and write to an output.txt file
        :param valid_customers:
        :return: 
        """
        output = ''
        for customer in sorted(valid_customers):
            output += 'Customer ID - {} Customer Name - {}\n'.format(
                customer, valid_customers[customer]['name']
            )
        print(output)
        with open(self.output_file, 'w')as _file:
            _file.write(output)
        