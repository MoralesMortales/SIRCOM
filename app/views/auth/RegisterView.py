from PyQt5 import QtWidgets
from app.database.auth.insertNew import newUser
from app.windows.py.registerWds import Ui_Form
from PyQt5.QtGui import QIntValidator
import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class RegisterView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Registro")
        self.buttonCancelar.clicked.connect(self.comeBack)
        self.buttonCrear.clicked.connect(self.handleRegister)

    #Validators

        cedulaValidator = QIntValidator(1000000,99999999, self)
        self.lineEditCedula.setValidator(cedulaValidator)

    def comeBack(self):
        from app.views.auth.LoginView import LoginView

        self.loginView = LoginView()
        self.loginView.showMaximized()
        self.close()

    def isValidEmail(self, email):
        if not email:
            return False
            
        if re.match(EMAIL_REGEX, email):
            return True
        else:
            return False

    def handleRegister(self):
        cedula = self.lineEditCedula.text().strip()
        correo = self.lineEditCorreo.text().strip()
        fisrtName = self.lineEditNombre.text().strip()
        lastName = self.lineEditApellido.text().strip()
        password = self.lineEditPass.text().strip()
        confirmPassword = self.lineEditPass_2.text().strip()
        
        if not cedula:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su cédula")
            self.lineEditCedula.setFocus()
            return
        
        if len(cedula) < 7:
            QtWidgets.QMessageBox.warning(self, "Error", "La cédula debe tener al menos 7 dígitos")
            return
        
        if not fisrtName:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su nombre")
            self.lineEditNombre.setFocus()
            return
        
        if not lastName:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su apellido")
            self.lineEditApellido.setFocus()
            return

        if not correo:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su correo")
            self.lineEditCorreo.setFocus()
            return
        
        if not self.isValidEmail(correo):
            QtWidgets.QMessageBox.warning(self, "Error", "Su correo no es válido")
            self.lineEditCorreo.setFocus()
            return

        if len(password) < 8:
            QtWidgets.QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 8 dígitos")
            return
        
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su contraseña")
            self.lineEditPass.setFocus()
            return
        
        if not confirmPassword:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor confirme su contraseña")
            self.lineEditPass.setFocus()
            return
        
        if not password == confirmPassword:
            QtWidgets.QMessageBox.warning(self, "Error", "No coinciden las contraseñas")
            return

        if newUser(cedula, fisrtName.capitalize(), lastName.capitalize(), correo, password):
            QtWidgets.QMessageBox.warning(self, "Exito", "Usuario creado")

        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Usuario no creado")

    # def openWindow(self):
    #     self.inventoryView = inventoryMainView()
    #     self.inventoryView.showMaximized()
    #     self.close()

