import pytest
import exceptions as qal_excs
from translator import Translator
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