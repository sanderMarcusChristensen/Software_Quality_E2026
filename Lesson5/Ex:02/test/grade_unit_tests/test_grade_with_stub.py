import pytest

import grade
from grade import Grade


class DatabaseStub:
    """Giver et fast svar uden at åbne en database eller udføre SQL."""

    def __init__(self, row):
        self.row = row

    # Disse to metoder gør det muligt at bruge stubben med 'with'.
    def __enter__(self):
        return self

    def __exit__(self, _error_type, _error, _traceback):
        return False

    # _ betyder, at stubben modtager argumenterne, men ikke bruger dem.
    def execute(self, _query, _parameters):
        return self

    def fetchone(self):
        return self.row


@pytest.fixture
def stub_database(monkeypatch):
    """Lader hver test vælge det svar, database-stubben skal give."""

    def set_result(row):
        database_stub = DatabaseStub(row)

        def connect_stub(_database_path):
            return database_stub

        monkeypatch.setattr(grade.sqlite3, "connect", connect_stub)

    return set_result


# (karakter, land for input, forventet konverteret karakter)
valid_cases = [
    ("00", "Denmark", "F"),
    ("02", "Denmark", "D"),
    ("04", "Denmark", "C+"),
    ("07", "Denmark", "B"),
    ("10", "Denmark", "A"),
    ("12", "Denmark", "A+"),
    ("F", "USA", "00"),
    ("D", "USA", "02"),
    ("C+", "USA", "04"),
    ("B", "USA", "07"),
    ("A", "USA", "10"),
    ("A+", "USA", "12"),
]


@pytest.mark.parametrize("value, country, expected", valid_cases)
def test_valid_grade(value, country, expected, stub_database):
    # Arrange
    stub_database((expected,))
    converter = Grade()

    # Act
    result = converter.convert(value, country)

    # Assert
    assert result == expected


# Ugyldige karakterer fra partitions og BVA. Dubletter er kun med én gang.
invalid_grade_cases = [
    ("-5", "Denmark"),
    ("13", "Denmark"),
    ("03", "Denmark"),
    ("-3", "Denmark"),
    ("C", "USA"),
    ("ABC", "Denmark"),
    ("Z", "USA"),
    ("", "Denmark"),
    (None, "Denmark"),
    ([], "Denmark"),
    (True, "Denmark"),
    ("A", "Denmark"),
    ("12", "USA"),
    ("-1", "Denmark"),
    ("01", "Denmark"),
    ("11", "Denmark"),
    ("11", "Denmark"),
]


@pytest.mark.parametrize("value, country", invalid_grade_cases)
def test_grade_not_found(value, country, stub_database):
    # Arrange
    stub_database(None)
    converter = Grade()
    expected_message = "Grade was not found in the database."

    # Act
    with pytest.raises(ValueError) as error:
        converter.convert(value, country)

    # Assert
    assert str(error.value) == expected_message


invalid_country_cases = ["Sweden", "", None, 123]


@pytest.mark.parametrize("country", invalid_country_cases)
def test_invalid_country(country, stub_database):
    # Arrange
    # Et gyldigt stub-svar sikrer, at fejlen skyldes landet, ikke et tomt opslag.
    stub_database(("A+",))
    converter = Grade()
    expected_message = "Country must be 'Denmark' or 'USA'."

    # Act
    with pytest.raises(ValueError) as error:
        converter.convert("12", country)

    # Assert
    assert str(error.value) == expected_message
