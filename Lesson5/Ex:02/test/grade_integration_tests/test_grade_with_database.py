import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from grade import Grade


@pytest.fixture
def test_database(tmp_path):
    """Giver hver test en frisk SQLite-kopi af projektets database."""
    source_path = Path(__file__).resolve().parents[2] / "code" / "db" / "grades.db"
    database_path = tmp_path / "grades.db"

    # Setup: kopier tabel og data. Originalen åbnes kun til læsning.
    with closing(sqlite3.connect(source_path.as_uri() + "?mode=ro", uri=True)) as source:
        with closing(sqlite3.connect(database_path)) as destination:
            source.backup(destination)

    try:
        yield database_path
    finally:
        # Teardown: kører også, hvis testen fejler.
        database_path.unlink()


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
def test_valid_grade(value, country, expected, test_database):
    # Arrange
    converter = Grade(test_database)

    # Act
    result = converter.convert(value, country)

    # Assert
    assert result == expected


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
    # SQL-lignende tekst skal behandles som en almindelig inputværdi.
    ("' OR 1=1 --", "Denmark"),
]


@pytest.mark.parametrize("value, country", invalid_grade_cases)
def test_grade_not_found(value, country, test_database):
    # Arrange
    converter = Grade(test_database)
    expected_message = "Grade was not found in the database."

    # Act
    with pytest.raises(ValueError) as error:
        converter.convert(value, country)

    # Assert
    assert str(error.value) == expected_message


@pytest.mark.parametrize("country", ["Sweden", "", None, 123])
def test_invalid_country(country, test_database):
    # Arrange
    converter = Grade(test_database)
    expected_message = "Country must be 'Denmark' or 'USA'."

    # Act
    with pytest.raises(ValueError) as error:
        converter.convert("12", country)

    # Assert
    assert str(error.value) == expected_message


def test_empty_table(test_database):
    # Arrange: kun denne tests kopi tømmes.
    with closing(sqlite3.connect(test_database)) as connection:
        connection.execute("DELETE FROM grades")
        connection.commit()
    converter = Grade(test_database)
    expected_message = "Grade was not found in the database."

    # Act
    with pytest.raises(ValueError) as error:
        converter.convert("12", "Denmark")

    # Assert
    assert str(error.value) == expected_message
