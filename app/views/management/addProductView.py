from PyQt5.QtWidgets import QWidget
from windows.py.addProductWindow import Ui_container

class addProductView(QWidget, Ui_container):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("pepe")
        print("holsa")


