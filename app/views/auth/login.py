from PyQt6.QtWidgets import QWidget

from windows.py.loginWindow import Ui_container  

class LoginView(QWidget, Ui_container):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Iniciar Sesión")

