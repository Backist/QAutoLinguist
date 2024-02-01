

from qautolinguist.translators.base import BaseTranslator

__engines__ = {
    translator.__name__.replace("Translator", "").lower(): translator
    for translator in BaseTranslator.__subclasses__()
}
