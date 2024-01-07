"""Translators module that contains all valid translators for QAutoLinguist."""




from qautolinguist.translators.google import GoogleTranslator
from qautolinguist.translators.microsoft import MicrosoftTranslator
from qautolinguist.translators.mymemory import MyMemoryTranslator
from qautolinguist.translators.deepl import DeeplTranslator
from qautolinguist.translators.constants import SILENT_SEPARATORS # export



__all__ = [
    "GoogleTranslator",
    "MicrosoftTranslator",
    "DeeplTranslator",
    "MyMemoryTranslator",
    "SILENT_SEPARATORS"
]
