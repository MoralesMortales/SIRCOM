from PyQt5 import QtWidgets
from app.database.auth.auth import authData
from app.windows.py.forgotWds import Ui_Form
from app.views.auth.RegisterView import RegisterView

class ForgotView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Resetear Clave")
        self.buttonCrear.clicked.connect(self.goToRegister)
        self.buttonVolver.clicked.connect(self.comeBack)
        self.registerView = RegisterView()

# Links

    def goToRegister(self):
        self.registerView.showMaximized()
        self.close()

    def comeBack(self):
        from app.views.auth.LoginView import LoginView

        self.loginView = LoginView()
        self.loginView.showMaximized()
        self.close()

    #      self.setupConnections()

    # def setupConnections(self):
    #     self.accessButtom.clicked.connect(self.handleLogin)
    #     self.cedulaField.returnPressed.connect(self.handleLogin)
    #     self.passwordField.returnPressed.connect(self.handleLogin)

    # def handleLogin(self):
    #     cedula = self.cedulaField.text().strip()
    #     password = self.passwordField.text()

    #     if not cedula:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su cédula")
    #         self.cedulaField.setFocus()
    #         return
            
    #     if not password:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su contraseña")
    #         self.passwordField.setFocus()
    #         return

    #     if authData(cedula,password):
    #         self.openWindow()

    #     else:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Usuario no encontrado")

    # def openWindow(self):
    #     self.inventoryView = inventoryMainView()
    #     self.inventoryView.showMaximized()
    #     self.close()
