import sys
from pathlib import Path

def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path.cwd()
    return base_path / relative_path