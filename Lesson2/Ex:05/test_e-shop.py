import pytest
from e_shop import calculate_discount_for_eshop


valid_amounts_no_discount = [0.10, 0.11, 150, 299.99, 300.00]
@pytest.mark.parametrize("amount", valid_amounts_no_discount)
def test_calculate_discount_no_discount(amount):

    # Arrange
    expected_result = 0.0

    # Act
    discount = calculate_discount_for_eshop(amount)

    # Assert
    assert discount == expected_result


valid_amounts_five_percent = [300.01, 300.02, 550, 799.99, 800.00]
@pytest.mark.parametrize("amount", valid_amounts_five_percent)
def test_calculate_discount_five_percent(amount):

    # Arrange
    expected_result = 0.05

    # Act
    discount = calculate_discount_for_eshop(amount)

    # Assert
    assert discount == expected_result


valid_amounts_ten_percent = [800.01, 800.02, 5000, 99999.99, 100000.00]
@pytest.mark.parametrize("amount", valid_amounts_ten_percent)
def test_calculate_discount_ten_percent(amount):

    # Arrange
    expected_result = 0.10

    # Act
    discount = calculate_discount_for_eshop(amount)

    # Assert
    assert discount == expected_result


below_minimum_amount = [0.01, 0.05, 0.08, 0.09]
@pytest.mark.parametrize("amount", below_minimum_amount)
def test_calculate_discount_below_minimum(amount):

    # Arrange
    expected_result = "Amount must be at least 0.1 kr"

    # Act
    with pytest.raises(ValueError) as excinfo:
        calculate_discount_for_eshop(amount)

    # Assert
    assert str(excinfo.value) == expected_result


negative_or_zero_amounts = [-0.01, 0.00]
@pytest.mark.parametrize("amount", negative_or_zero_amounts)
def test_calculate_discount_negative_or_zero(amount):

    # Arrange
    expected_result = "Amount must be greater than 0"

    # Act
    with pytest.raises(ValueError) as excinfo:
        calculate_discount_for_eshop(amount)

    # Assert
    assert str(excinfo.value) == expected_result


def test_calculate_discount_with_non_numeric():
    # Arrange
    amount = "abc"
    expected_result = "Amount must be a number"

    # Act
    with pytest.raises(ValueError) as excinfo:
        calculate_discount_for_eshop(amount)

    # Assert
    assert str(excinfo.value) == expected_result