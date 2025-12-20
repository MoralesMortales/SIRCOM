from PyQt5 import QtWidgets
from app.windows.py.emailCodeWds import Ui_Form
from app.database.auth.get import getEmail
from app.functions.tools.sendEmail import send_code
from app.views.auth.forgotPass.NewPasswordView import NewPasswordView
from PyQt5.QtGui import QIntValidator

class EmailCodeView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cedula = 0
        self.CODE = 0
        self.NewPasswordView = NewPasswordView()
        self.setWindowTitle("Validar Código")
        self.buttonComprobar.clicked.connect(self.validateCode)
        self.buttonVolver.clicked.connect(self.comeBack)

        #validator
        codeValidator = QIntValidator(0000,9999, self)
        self.lineEditCodigo.setValidator(codeValidator)
        
    def getCode(self):
        email = getEmail(self.cedula)
        self.CODE = send_code(email)
        
    def validateCode(self):
        codeGiven = self.lineEditCodigo.text().strip()
        print(codeGiven, self.CODE)
        if not codeGiven:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese su clave")
    
        elif self.CODE == int(codeGiven):
            self.NewPasswordView.openWindow(self.cedula)
            self.close()
            
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Clave incorrecta")
            self.lineEditCodigo.setFocus()

    def comeBack(self):
        from app.views.auth.LoginView import LoginView

        self.loginView = LoginView()
        self.loginView.showMaximized()
        self.close()
        
    def openWindow(self, cedula):
        self.cedula = cedula
        self.showMaximized()
        self.getCode()
  