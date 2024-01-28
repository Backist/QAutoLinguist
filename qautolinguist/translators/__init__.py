"""Translators module that contains all valid translators for QAutoLinguist."""




from translators.google import GoogleTranslator
from translators.microsoft import MicrosoftTranslator
from translators.mymemory import MyMemoryTranslator
from translators.deepl import DeeplTranslator
from translators.constants import SILENT_SEPARATORS # export



__all__ = [
    "GoogleTranslator",
    "MicrosoftTranslator",
    "DeeplTranslator",
    "MyMemoryTranslator",
    "SILENT_SEPARATORS"
]
