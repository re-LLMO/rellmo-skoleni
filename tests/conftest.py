import sys
from pathlib import Path
import pytest

PLUGIN_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))


@pytest.fixture
def docasna_slozka(tmp_path):
    """Pracovní složka účastníka, čistá pro každý test."""
    return tmp_path
