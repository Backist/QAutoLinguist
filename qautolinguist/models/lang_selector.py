"Custom QPushButton that implements QAutoLinguist workflow"

from qautolinguist.qal import QAutoLinguist
from pyside6 import QtWidgets

class QPushButton(QAutoLinguist, QtWidgets.QComboBox):
    
    ...