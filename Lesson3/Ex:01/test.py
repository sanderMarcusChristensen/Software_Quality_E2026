# test_order_pricing_service.py

from unittest.mock import Mock    # Pytest needs an external library for mocking
import pytest
from order_pricings_service import OrderPricingService


# Python fixtures provide context for the tests
@pytest.fixture
def pricing_service():
    # set up
    discount_service = Mock()
    shipping_service = Mock()

    service = OrderPricingService(discount_service, shipping_service)

    # We return all three so the tests can configure/inspect the mocks too
    return service, discount_service, shipping_service


def test_calculates_total_with_discount_and_shipping(pricing_service):

    # Arrange
    sut, discount_service, shipping_service = pricing_service
    discount_service.get_discount.return_value = 50
    shipping_service.get_shipping_costs.return_value = 30

    # Act
    total = sut.calculate_total("DK", 200)

    # Assert
    assert total == pytest.approx(180)
    discount_service.get_discount.assert_called_once_with(200)
    shipping_service.get_shipping_costs.assert_called_once_with("DK", 200)