import pytest
import json
import os

from src.invite_generator import InviteGenerator

valid_test_data = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_data/valid_customers.txt'
)
invalid_test_data = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_data/invalid_customers.txt'
)
test_output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'output.txt'
)

processed_dummy_data = {
    1: {"name": "Alice Cahill", "lat": 51.92893, "long": -10.27699},
    2: {"name": "Ian McArdle", "lat": 51.8856167, "long": -10.4240951},
    12: {"name": "Christina McArdle", "lat": 52.986375, "long": -6.043701}
}

@pytest.fixture
def mock_generator():
    test_gen = InviteGenerator(
        distance=100,
        debug=False
    )
    return test_gen


def test_get_customer_data_throws_expcetion_for_invalid_data(mock_generator):
    mock_generator.customers_file = invalid_test_data
    with pytest.raises(Exception):
        mock_generator._get_customers_data()


def test_get_customer_data_valid_data(mock_generator):
    mock_generator.customers_file = valid_test_data
    expected_data = processed_dummy_data
    assert mock_generator._get_customers_data() == expected_data


def test_get_great_circle_distance(mock_generator):
    assert mock_generator._get_great_circle_distance(
        -10.27699, 51.92893
    ) == 313.25563378141084
    assert mock_generator._get_great_circle_distance(
        -6.043701, 52.986375
    ) == 41.76872550078046


def test_get_customers_within_range_400km(mock_generator):
    mock_generator.distance = 400
    expected_data = {1: {'name': 'Alice Cahill'}, 2: {'name': 'Ian McArdle'}, 12: {"name": "Christina McArdle"}}
    assert mock_generator._get_customers_within_range(
        processed_dummy_data
    ) == expected_data


def test_get_customers_within_range_100km(mock_generator):
    expected_data = {12: {"name": "Christina McArdle"}}
    assert mock_generator._get_customers_within_range(
        processed_dummy_data
    ) == expected_data


def test_get_customers_within_range_30km(mock_generator):
    mock_generator.distance = 30
    expected_data = {}
    assert mock_generator._get_customers_within_range(
        processed_dummy_data
    ) == expected_data


def test_output_valid_customers(mock_generator):
    mock_generator.output_file = test_output_file
    mock_generator._output_valid_customers(
        {12: {"name": "Christina McArdle"}}
    )
    with open(test_output_file) as _file:
        assert "Customer ID - 12 Customer Name - Christina McArdle" in _file.read()
