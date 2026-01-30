from PyQt5 import QtWidgets, QtGui
from app.database.auth.auth import authData
from app.windows.py.loginWds import Ui_Form
from app.views.auth.ForgotView import ForgotView

class LoginView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Autenticación")
        validator = QtGui.QIntValidator(0, 99999999, self)
        self.lineEditUser.setValidator(validator)
        self.lineEditUser.setMaxLength(8)
        
        self.forgotView = ForgotView()
        self.labelLink.mousePressEvent = self.goToForgot
        self.buttonLogin.clicked.connect(self.goInto)
        
    def goToForgot(self, event):
        self.forgotView.showMaximized()
        self.close()

    def goInto(self):
        cedula = self.lineEditUser.text().strip()
        password = self.lineEditPass.text().strip()
        
        if not cedula:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su cédula")
            self.lineEditUser.setFocus()
            return
        
        elif not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su contraseña")
            self.lineEditPass.setFocus()
            return
        
        elif authData(cedula, password):
            from app.views.management.providers.ProvidersView import ProvidersView
            from app import session
            
            session.currentUserCedula = cedula
            
            self.ProvidersView = ProvidersView()
            self.ProvidersView.showMaximized()
            self.close()
            
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "No existe un usuario con esas credenciales")

        