"""Run this file whenever you change the grade pairs below."""
#SQLite
import sqlite3
from pathlib import Path


database_path = Path(__file__).with_name("grades.db")

# Simple grade pairs chosen for this project.
grade_pairs = [
    ("00", "F"),
    ("02", "D"),
    ("04", "C+"),
    ("07", "B"),
    ("10", "A"),
    ("12", "A+"),
]

with sqlite3.connect(database_path) as connection:
    connection.execute(
        """CREATE TABLE IF NOT EXISTS grades (
            danish_grade TEXT PRIMARY KEY,
            american_grade TEXT NOT NULL
        )"""
    )
    # Replace old rows so the database matches the list above exactly.
    connection.execute("DELETE FROM grades")
    connection.executemany(
        "INSERT INTO grades (danish_grade, american_grade) VALUES (?, ?)",
        grade_pairs,
    )

print("Database ready:", database_path)
print("Grade pairs in the setup list:", len(grade_pairs))
