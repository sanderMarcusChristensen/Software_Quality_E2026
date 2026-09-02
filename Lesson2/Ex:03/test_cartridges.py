import pytest
from cartridges import calculate_discount

valid_quantities_no_discount = [5, 6, 50, 98, 99]
@pytest.mark.parametrize("quantity", valid_quantities_no_discount)
def test_calculate_discount_no_discount(quantity):

    # Arrange
    expected_result = 0.0

    # Act
    discount = calculate_discount(quantity)

    # Assert
    assert discount == expected_result



valid_quantities_with_discount = [100, 101, 1000]
@pytest.mark.parametrize("quantity", valid_quantities_with_discount)
def test_calculate_discount_with_discount(quantity):

    # Arrange
    expected_result = 0.2  # Assuming a 20% discount

    # Act
    discount = calculate_discount(quantity)

    # Assert
    assert discount == expected_result


below_discount_threshold = [0, 1, 2, 3, 4]
@pytest.mark.parametrize("quantity", below_discount_threshold)
def test_calculate_discount_below_threshold(quantity):

    # Arrange
    expected_result = "Minimum order quantity is 5"

    # Act
    with pytest.raises(ValueError) as excinfo:
        calculate_discount(quantity)

    # Assert
    assert str(excinfo.value) == expected_result


def test_calculate_discount_negative_number():
    # Arrange
    quantity = -1
    expected_result = "Minimum order quantity is 5"

    # Act
    with pytest.raises(ValueError) as excinfo:
        calculate_discount(quantity)

    # Assert
    assert str(excinfo.value) == expected_result


def test_calculate_discount_with_non_integer():
    # Arrange
    quantity = "abc"
    expected_result = "Quantity must be an integer"

    # Act
    with pytest.raises(ValueError) as excinfo:
        calculate_discount(quantity)

    # Assert
    assert str(excinfo.value) == expected_result