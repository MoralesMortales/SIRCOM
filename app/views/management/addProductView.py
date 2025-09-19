from PyQt5.QtWidgets import QWidget
from app.windows.py.newProductWds import Ui_Form

class addProductView(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("pepe")


