from PyQt5 import QtWidgets
from app.windows.py.newPasswordWds import Ui_Form
from app.database.edit.change import changePassword

class NewPasswordView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cedula = 0
        self.setWindowTitle("Crear Nueva Clave")
        
        self.buttonAceptar.clicked.connect(self.changePassword)
        self.buttonVolver.clicked.connect(self.comeBack)
        
    def changePassword(self):
        password = self.lineEditPasscode.text().strip()
        confirmPassword = self.lineEditConfirmar.text().strip()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su contraseña.")
            return
     
        elif not confirmPassword:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor confirme su contraseña.")
            return
     
        elif password == confirmPassword:
            changePassword(self.cedula, password)
            QtWidgets.QMessageBox.information(self, "Exito", "Contraseña cambiada exitosamente.")
            self.comeBack()
        
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "No coinciden las contraseñas.")
            return
        
    def comeBack(self):
        from app.views.auth.LoginView import LoginView

        self.loginView = LoginView()
        self.loginView.showMaximized()
        self.close()
        
    def openWindow(self, cedula):
        self.cedula = cedula
        self.showMaximized()