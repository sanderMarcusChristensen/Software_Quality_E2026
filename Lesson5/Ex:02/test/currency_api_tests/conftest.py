"""Gør Currency tilgængelig for tests i denne mappe og dens undermapper."""

import sys
from pathlib import Path


api_code_folder = Path(__file__).resolve().parents[2] / "code" / "api"
sys.path.insert(0, str(api_code_folder))
