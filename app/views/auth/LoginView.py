from PyQt5 import QtWidgets
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))

from app.database.auth.auth import authData
from app.views.management.inventoryView import inventoryMainView  
from app.windows.py.loginWds import Ui_container

class LoginView(QtWidgets.QWidget, Ui_container):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Autenticación")
        self.setupConnections()

    def setupConnections(self):
        self.accessButtom.clicked.connect(self.handleLogin)
        self.cedulaField.returnPressed.connect(self.handleLogin)
        self.passwordField.returnPressed.connect(self.handleLogin)
        
        # self.inventoryView = None

    def handleLogin(self):
        cedula = self.cedulaField.text().strip()
        password = self.passwordField.text()

        if not cedula:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su cédula")
            self.cedulaField.setFocus()
            return
            
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su contraseña")
            self.passwordField.setFocus()
            return

        if authData(cedula,password):
            self.openWindow()

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Usuario no encontrado")

    def openWindow(self):
        self.inventoryView = inventoryMainView()
        self.inventoryView.showMaximized()
        self.close()
