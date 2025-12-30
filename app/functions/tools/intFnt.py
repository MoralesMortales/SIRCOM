from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui

class NumericDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, is_int=True, min_val=0, max_val=999999):
        super().__init__(parent)
        self.is_int = is_int
        self.min_val = min_val
        self.max_val = max_val

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        
        if self.is_int:
            # Validador para números enteros
            validator = QtGui.QIntValidator(self.min_val, self.max_val, editor)
        else:
            validator = QtGui.QDoubleValidator(float(self.min_val), float(self.max_val), 2, editor)
            validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
            validator.setLocale(QtCore.QLocale(QtCore.QLocale.English)) # Usa punto para decimales
            
        editor.setValidator(validator)
        return editor