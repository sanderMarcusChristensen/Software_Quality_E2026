"""Make the classes in Ex:02/code available to these tests."""

import sys
from pathlib import Path


code_folder = Path(__file__).resolve().parents[2] / "code"
sys.path.insert(0, str(code_folder))
