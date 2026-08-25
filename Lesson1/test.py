import calculator


def test_add():
    # Arrange
    number1 = 2
    number2 = 9

    # Act 
    result = calculator.add(number1, number2)

    # Assert
    assert result == 11
    


def test_subtract():
    # Arrange
    number1 = 5
    number2 = 3

    # Act
    result = calculator.subtract(number1, number2)

    # Assert
    assert result == 2

    print("subtract method :",calculator.subtract(number1, number2), "assert result:", result)
    


def test_multiply():
    # Arrange
    number1 = 2
    number2 = 3

    # Act
    result = calculator.multiply(number1, number2)

    # Assert
    assert result == 6


def test_divide():
    # Arrange
    number1 = 6
    number2 = 3

    # Act
    result = calculator.divide(number1, number2)

    # Assert
    assert result == 2



## BLACK BOX TESTING

def test_add_black_box():
    # Arrange
    number1 = 5
    number2 = 5

    # Act 
    result = calculator.add(number1, number2)

    # Assert
    assert result != 11


def test_subtract_black_box():
    # Arrange
    number1 = 5
    number2 = 3

    # Act
    result = calculator.subtract(number1, number2)

    # Assert
    assert result != -2



if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    test_add_black_box()
    test_subtract_black_box()
    print("All tests passed")
