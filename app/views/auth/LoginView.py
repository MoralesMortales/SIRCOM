from PyQt5 import QtWidgets, QtGui, QtCore
from app.database.auth.auth import authData
from app.windows.py.loginWds import Ui_Form
from app.views.auth.ForgotView import ForgotView
from app.views.auth.RegisterView import RegisterView


from app.functions.tools.getIcon import getIcon
import os

class LoginView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Autenticación")
        validator = QtGui.QIntValidator(0, 99999999, self)
        
        self.registerView = RegisterView()
        self.lineEditUser.setValidator(validator)
        self.lineEditUser.setMaxLength(8)
        
        # Configurar botón de mostrar/ocultar
        self.setup_password_toggle()
        
        # Configurar ícono para el botón de login
        self.setup_login_button_icon()
        
        self.forgotView = ForgotView()
        self.labelLink.mousePressEvent = self.goToForgot
        self.buttonLogin.clicked.connect(self.goInto)
        self.buttonCreateUser.clicked.connect(self.goToRegister)
        
    def goToRegister(self):
        self.registerView.showMaximized()
        self.close()

    
    def setup_password_toggle(self):
        """Configurar botón para mostrar/ocultar contraseña"""
        # Crear botón
        self.toggle_btn = QtWidgets.QToolButton(self.lineEditPass)
        self.toggle_btn.setCursor(QtCore.Qt.PointingHandCursor)
        
        # Obtener rutas de los íconos usando getIcon
        try:
            eye_icon_path = getIcon("Eye.png")
            eye_closed_icon_path = getIcon("EyeClosed.png")
            
            # Crear QIcon a partir de las rutas
            eye_icon = QtGui.QIcon(eye_icon_path) if eye_icon_path and os.path.exists(eye_icon_path) else None
            eye_closed_icon = QtGui.QIcon(eye_closed_icon_path) if eye_closed_icon_path and os.path.exists(eye_closed_icon_path) else None
            
            if eye_icon and not eye_icon.isNull() and eye_closed_icon and not eye_closed_icon.isNull():
                self.eye_icon = eye_icon
                self.eye_closed_icon = eye_closed_icon
                self.toggle_btn.setIcon(self.eye_closed_icon)
                self.toggle_btn.setIconSize(QtCore.QSize(20, 20))
                self.use_icons = True
            else:
                # Si no hay íconos válidos, crear íconos básicos
                print("Creando íconos básicos para mostrar/ocultar contraseña")
                self.create_basic_icons()
                self.toggle_btn.setIcon(self.eye_closed_icon)
                self.toggle_btn.setIconSize(QtCore.QSize(20, 20))
                self.use_icons = True
                
        except Exception as e:
            print(f"Error al cargar íconos: {e}")
            # Crear íconos básicos como fallback
            self.create_basic_icons()
            self.toggle_btn.setIcon(self.eye_closed_icon)
            self.toggle_btn.setIconSize(QtCore.QSize(20, 20))
            self.use_icons = True
        
        # Configurar estilo
        self.toggle_btn.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background: rgba(0, 0, 0, 0.05);
                border-radius: 3px;
            }
            QToolButton:pressed {
                background: rgba(0, 0, 0, 0.1);
            }
        """)
        
        # Conectar señal
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)
        
        # Posicionar botón
        self.position_toggle_button()
        
        # Estado inicial
        self.password_visible = False
        self.lineEditPass.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Actualizar posición cuando cambie el tamaño
        self.lineEditPass.resizeEvent = self.on_password_resize
        
    def create_basic_icons(self):
        """Crear íconos básicos si no se encuentran los archivos"""
        # Crear un ícono de ojo abierto simple
        pixmap_eye = QtGui.QPixmap(20, 20)
        pixmap_eye.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap_eye)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        
        # Dibujar ojo
        painter.drawEllipse(2, 2, 16, 16)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black))
        painter.drawEllipse(8, 8, 4, 4)
        painter.end()
        
        self.eye_icon = QtGui.QIcon(pixmap_eye)
        
        # Crear un ícono de ojo cerrado simple
        pixmap_eye_closed = QtGui.QPixmap(20, 20)
        pixmap_eye_closed.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap_eye_closed)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        
        # Dibujar ojo cerrado (línea)
        painter.drawLine(4, 10, 16, 10)
        painter.end()
        
        self.eye_closed_icon = QtGui.QIcon(pixmap_eye_closed)
        
    def setup_login_button_icon(self):
        """Configurar ícono para el botón de login"""
        try:
            # Obtener ruta del ícono usando getIcon
            login_icon_path = getIcon("Login.png")
            
            if login_icon_path and os.path.exists(login_icon_path):
                login_icon = QtGui.QIcon(login_icon_path)
                
                if not login_icon.isNull():
                    self.buttonLogin.setIcon(login_icon)
                    self.buttonLogin.setIconSize(QtCore.QSize(24, 24))
                    
                    # Ajustar texto para incluir el ícono
                    self.buttonLogin.setText("  Iniciar Sesión")
                    
                    # Configurar estilo para mejor visualización
                    current_style = self.buttonLogin.styleSheet()
                    new_style = """
                        QPushButton {
                            padding: 8px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #e6e6e6;
                        }
                    """
                    self.buttonLogin.setStyleSheet(new_style + current_style if current_style else new_style)
                    
        except Exception as e:
            print(f"Error al cargar ícono de login: {e}")
            # Continuar sin ícono si hay error
        
    def on_password_resize(self, event):
        """Manejar redimensionamiento del campo de contraseña"""
        QtWidgets.QLineEdit.resizeEvent(self.lineEditPass, event)
        self.position_toggle_button()
        
    def position_toggle_button(self):
        """Posicionar el botón dentro del QLineEdit"""
        # Obtener dimensiones
        frame_width = self.lineEditPass.style().pixelMetric(
            QtWidgets.QStyle.PM_DefaultFrameWidth)
        
        # Calcular posición
        btn_size = self.toggle_btn.sizeHint()
        x = self.lineEditPass.width() - btn_size.width() - frame_width - 5
        y = (self.lineEditPass.height() - btn_size.height()) // 2
        
        self.toggle_btn.move(x, y)
        
    def toggle_password_visibility(self):
        """Alternar entre mostrar y ocultar la contraseña"""
        if not self.password_visible:
            # Mostrar contraseña
            self.lineEditPass.setEchoMode(QtWidgets.QLineEdit.Normal)
            if self.use_icons:
                self.toggle_btn.setIcon(self.eye_icon)
        else:
            # Ocultar contraseña
            self.lineEditPass.setEchoMode(QtWidgets.QLineEdit.Password)
            if self.use_icons:
                self.toggle_btn.setIcon(self.eye_closed_icon)
        
        self.password_visible = not self.password_visible
    
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