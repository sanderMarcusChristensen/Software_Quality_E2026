"""Gør Grade-klassen tilgængelig for pytest."""

import sys
from pathlib import Path


database_code_folder = Path(__file__).resolve().parents[2] / "code" / "db"
sys.path.insert(0, str(database_code_folder))
