import pytest
import qautolinguist.exceptions as qal_excs
from qautolinguist.translator import Translator
from pathlib import Path

ROOT = Path(__file__).parent
VALID_ROOT = ROOT / "valid"
TARGETS = [
    pytest.param(p, id=p.stem)
    for p in VALID_ROOT.glob("*.txt")
]


class TestTranslator:
    
    inst = Translator()
    
    ...