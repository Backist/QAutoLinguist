"Custom QPushButton that implements QAutoLinguist workflow"

from qautolinguist.qal import QAutoLinguist
from pyside6 import QtWidgets

class LangSelector(QAutoLinguist, QtWidgets.QComboBox):
    """Widget que incrustra una implementaion de QAutoLinguist a través de un ComboBox.
    
    """
    
    def available_locales(self): ...
    def reload_locales(self): ...
    @property
    def current_locale(self): ...
    def set_locale(locale: str): ...
    @staticmethod
    def dynamic_translation(to_translate): ...