import sqlite3
from pathlib import Path
from grade import Grade


class Grade:
    """Look up Danish and American grade equivalents in a SQLite database."""

    def __init__(self, database_path=None):
        if database_path is None:
            database_path = Path(__file__).with_name("grades.db")
        self.database_path = database_path

    def convert(self, grade, country):
        """Convert a grade from 'Denmark' or 'USA' to the other system."""
        if country == "Denmark":
            search_column = "danish_grade"
            result_column = "american_grade"
        elif country == "USA":
            search_column = "american_grade"
            result_column = "danish_grade"
        else:
            raise ValueError("Country must be 'Denmark' or 'USA'.")

        query = f"SELECT {result_column} FROM grades WHERE {search_column} = ?"

        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute(query, (str(grade),)).fetchone()

        if row is None:
            raise ValueError("Grade was not found in the database.")

        return row[0]
