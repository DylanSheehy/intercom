import argparse

from invite_generator import InviteGenerator

def main(args):
    """
    Main method of execution
    :param args:
    :return: 
    """
    generator = InviteGenerator(
        distance=args.distance,
        debug=args.debug
    )
    generator.run()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a list of customers within a given distance of the office'
    )
    parser.add_argument(
        '--distance', dest='distance', action='store',
        help='distance from the office in km',
        default=100
    )
    parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help='Enable debug logs',
        default=False
    )
    args = parser.parse_args()
    main(args)