from PyQt5 import QtWidgets
from app.database.auth.auth import authCedula
from app.windows.py.forgotWds import Ui_Form
from app.views.auth.RegisterView import RegisterView
from app.views.auth.forgotPass.EmailCodeView import EmailCodeView

class ForgotView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Resetear Clave")
        self.buttonCrear.clicked.connect(self.goToRegister)
        self.buttonVolver.clicked.connect(self.comeBack)

        self.registerView = RegisterView()
        self.EmailCodeView = EmailCodeView()
        self.buttonCorreo.clicked.connect(self.sendEmail)

    def sendEmail(self):
        cedula = self.lineEditCedula.text().strip()
        
        if not cedula:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su cédula")
            self.lineEditCedula.setFocus()
            return
        
        if authCedula(cedula):
            self.EmailCodeView.openWindow(cedula)
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "No existe un usuario con esas credenciales")

    def goToRegister(self):
        self.registerView.showMaximized()
        self.close()

    def comeBack(self):
        from app.views.auth.LoginView import LoginView

        self.loginView = LoginView()
        self.loginView.showMaximized()
        self.close()
