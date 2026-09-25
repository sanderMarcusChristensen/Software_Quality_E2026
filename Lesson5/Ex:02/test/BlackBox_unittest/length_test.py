import pytest

from length import Length


# (measure, system, expected converted value)
valid_cases = [
    (0.01, "Metric", 0.00),
    (0.02, "Metric", 0.01),
    (1, "Metric", 0.39),
    (50.5, "Metric", 19.88),
    (1000.25, "Metric", 393.80),
    (0.01, "Imperial", 0.03),
    (1, "Imperial", 2.54),
    (2.54, "Imperial", 6.45),
]


@pytest.mark.parametrize("measure, system, expected", valid_cases)
def test_valid_length(measure, system, expected):
    # Arrange
    length = Length(measure, system)

    # Act
    result = length.convert()

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
def test_invalid_length(measure, system, expected_error):
    # Arrange: the inputs above are invalid according to the test plan.

    # Act
    with pytest.raises(expected_error):
        Length(measure, system).convert()

    # Assert: pytest.raises checks that an error was raised.
