import pytest

from temperature import Temperature


# (measure, starting scale, destination scale, expected converted value)
valid_cases = [
    (-10, "C", "F", 14.00),
    (25.55, "C", "K", 298.70),
    (32, "F", "C", 0.00),
    (25.5, "F", "K", 269.54),
    (273.15, "K", "C", 0.00),
    (0, "K", "F", -459.67),
]


@pytest.mark.parametrize("measure, source, destination, expected", valid_cases)
def test_valid_temperature(measure, source, destination, expected):
    # Arrange
    temperature = Temperature(measure, source)

    # Act
    result = temperature.convert(destination)

    # Assert
    assert result == expected


# (measure, starting scale, destination scale, expected error)
invalid_cases = [
    (25.555, "C", "F", ValueError),
    ("abc", "C", "F", (TypeError, ValueError)),
    (25, "X", "F", ValueError),
    (25, "", "F", ValueError),
    (25, 123, "F", ValueError),
    (25, "C", "X", ValueError),
    (25, "C", "", ValueError),
    (25, "C", 123, ValueError),
]


@pytest.mark.parametrize("measure, source, destination, expected_error", invalid_cases)
def test_invalid_temperature(measure, source, destination, expected_error):
    # Arrange: the inputs above are invalid according to the test plan.

    # Act
    with pytest.raises(expected_error):
        Temperature(measure, source).convert(destination)

    # Assert: pytest.raises checks that an error was raised.
