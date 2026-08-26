import calculator


def test_add():
    # Arrange
    number1 = 2
    number2 = 9
    expected_result = 11

    # Act 
    result = calculator.add(number1, number2)

    # Assert
    assert result == expected_result 
    print("add method :",calculator.add(number1, number2), "assert result:", expected_result)
    


def test_subtract():
    # Arrange
    number1 = 5
    number2 = 3
    expected_result = 2

    # Act
    result = calculator.subtract(number1, number2)

    # Assert
    assert result == expected_result 

    print("subtract method :",calculator.subtract(number1, number2), "assert result:", expected_result)
    


def test_multiply():
    # Arrange
    number1 = 2
    number2 = 3
    expected_result = 6

    # Act
    result = calculator.multiply(number1, number2)

    # Assert
    assert result == expected_result 

    print("multiply method :",calculator.multiply(number1, number2), "assert result:", expected_result)


def test_divide():
    # Arrange
    number1 = 6
    number2 = 3
    expected_result = 2

    # Act
    result = calculator.divide(number1, number2)

    # Assert
    assert result == expected_result
    print("divide method :",calculator.divide(number1, number2), "assert result:", expected_result)



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