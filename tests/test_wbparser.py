import pytest
from unittest.mock import Mock

from wbparser.main import WBparser


@pytest.fixture
def mock_parser():
    parser = WBparser('11152183')
    parser.result = Mock(return_value={'brand': 'O`SHADE',
                                            'colors': [{'id': 0, 'name': 'черный'}],
                                            'diffPrice': False,
                                            'id': '11152183',
                                            'name': 'Ботинки женские натуральная кожа осенние',
                                            'pics': 16,
                                            'priceU': 757400,
                                            'qty': 1012,
                                            'questions': 1940,
                                            'rating': 4.7,
                                            'salePriceU': 560400,
                                            'sizes': ['36', '37', '38', '39', '40', '41', '42', '43']})
    return parser


def test_parse_data(mock_parser):
    result = mock_parser.parse_data()
    assert result is not None
    assert 'id', 'name' in result
