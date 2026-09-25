import pytest

from weight import Weight


# (measure, system, expected converted value)
valid_cases = [
    (0.01, "Metric", 0.02),
    (0.02, "Metric", 0.04),
    (1, "Metric", 2.20),
    (50.5, "Metric", 111.33),
    (1000.25, "Metric", 2205.17),
    (0.01, "Imperial", 0.00),
    (1, "Imperial", 0.45),
    (2.5, "Imperial", 1.13),
]


@pytest.mark.parametrize("measure, system, expected", valid_cases)
def test_valid_weight(measure, system, expected):
    # Arrange
    weight = Weight(measure, system)

    # Act
    result = weight.convert()

    # Assert
    assert result == expected


# (measure, system, expected error)
invalid_cases = [
    (0, "Metric", ValueError),
    (-0.01, "Metric", ValueError),
    (-1, "Imperial", ValueError),
    (1.234, "Metric", ValueError),
    ("abc", "Metric", (TypeError, ValueError)),
    (1, "Unknown", ValueError),
    (1, "", ValueError),
    (1, 123, ValueError),
]


@pytest.mark.parametrize("measure, system, expected_error", invalid_cases)
def test_invalid_weight(measure, system, expected_error):
    # Arrange: the inputs above are invalid according to the test plan.

    # Act
    with pytest.raises(expected_error):
        Weight(measure, system).convert()

    # Assert: pytest.raises checks that an error was raised.
