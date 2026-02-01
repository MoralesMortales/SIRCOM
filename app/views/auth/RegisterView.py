from PyQt5 import QtWidgets, QtCore, QtGui
from app.database.auth.insertNew import newUser
from app.windows.py.registerWds import Ui_Form
from PyQt5.QtGui import QIntValidator
from app.functions.tools.getIcon import getIcon
import re
import os

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class RegisterView(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Registro")
        self.buttonCancelar.clicked.connect(self.comeBack)
        self.buttonCrear.clicked.connect(self.handleRegister)

        # Validators
        cedulaValidator = QIntValidator(1000000, 99999999, self)
        self.lineEditCedula.setValidator(cedulaValidator)

        # Crear etiquetas de "obligatorio" dentro del layout
        self.setup_required_labels()

        # Conectar señales de cambio de texto para ocultar etiquetas
        self.connect_text_changes()

        # Configurar botones de mostrar/ocultar para ambos campos de contraseña
        self.setup_password_toggle(self.lineEditPass)
        self.setup_password_toggle(self.lineEdit_3)
        
        # Restaurar el espaciado original del layout
        self.verticalLayout_4.setSpacing(10)  # Volver al espaciado original

    def setup_password_toggle(self, line_edit):
        """Configurar botón para mostrar/ocultar contraseña para un campo específico"""
        # Crear botón
        toggle_btn = QtWidgets.QToolButton(line_edit)
        toggle_btn.setCursor(QtCore.Qt.PointingHandCursor)
        
        # Obtener rutas de los íconos usando getIcon
        try:
            eye_icon_path = getIcon("Eye.png")
            eye_closed_icon_path = getIcon("EyeClosed.png")
            
            # Crear QIcon a partir de las rutas
            eye_icon = QtGui.QIcon(eye_icon_path) if eye_icon_path and os.path.exists(eye_icon_path) else None
            eye_closed_icon = QtGui.QIcon(eye_closed_icon_path) if eye_closed_icon_path and os.path.exists(eye_closed_icon_path) else None
            
            if eye_icon and not eye_icon.isNull() and eye_closed_icon and not eye_closed_icon.isNull():
                toggle_btn.eye_icon = eye_icon
                toggle_btn.eye_closed_icon = eye_closed_icon
                toggle_btn.setIcon(eye_closed_icon)
                toggle_btn.setIconSize(QtCore.QSize(20, 20))
                toggle_btn.use_icons = True
            else:
                # Si no hay íconos válidos, crear íconos básicos
                print("Creando íconos básicos para mostrar/ocultar contraseña")
                eye_icon, eye_closed_icon = self.create_basic_icons()
                toggle_btn.eye_icon = eye_icon
                toggle_btn.eye_closed_icon = eye_closed_icon
                toggle_btn.setIcon(eye_closed_icon)
                toggle_btn.setIconSize(QtCore.QSize(20, 20))
                toggle_btn.use_icons = True
                
        except Exception as e:
            print(f"Error al cargar íconos: {e}")
            # Crear íconos básicos como fallback
            eye_icon, eye_closed_icon = self.create_basic_icons()
            toggle_btn.eye_icon = eye_icon
            toggle_btn.eye_closed_icon = eye_closed_icon
            toggle_btn.setIcon(eye_closed_icon)
            toggle_btn.setIconSize(QtCore.QSize(20, 20))
            toggle_btn.use_icons = True
        
        # Configurar estilo
        toggle_btn.setStyleSheet("""
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
        toggle_btn.clicked.connect(lambda: self.toggle_password_visibility(line_edit, toggle_btn))
        
        # Estado inicial
        toggle_btn.password_visible = False
        line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Guardar referencia al botón en el line_edit
        line_edit.toggle_btn = toggle_btn
        
        # Posicionar botón
        self.position_toggle_button(line_edit)
        
        # Actualizar posición cuando cambie el tamaño
        original_resize_event = line_edit.resizeEvent
        def new_resize_event(event):
            if original_resize_event:
                original_resize_event(event)
            self.position_toggle_button(line_edit)
        line_edit.resizeEvent = new_resize_event

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
        
        eye_icon = QtGui.QIcon(pixmap_eye)
        
        # Crear un ícono de ojo cerrado simple
        pixmap_eye_closed = QtGui.QPixmap(20, 20)
        pixmap_eye_closed.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap_eye_closed)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        
        # Dibujar ojo cerrado (línea)
        painter.drawLine(4, 10, 16, 10)
        painter.end()
        
        eye_closed_icon = QtGui.QIcon(pixmap_eye_closed)
        
        return eye_icon, eye_closed_icon

    def position_toggle_button(self, line_edit):
        """Posicionar el botón dentro del QLineEdit"""
        if not hasattr(line_edit, 'toggle_btn'):
            return
            
        toggle_btn = line_edit.toggle_btn
        
        # Obtener dimensiones
        frame_width = line_edit.style().pixelMetric(
            QtWidgets.QStyle.PM_DefaultFrameWidth)
        
        # Calcular posición
        btn_size = toggle_btn.sizeHint()
        x = line_edit.width() - btn_size.width() - frame_width - 5
        y = (line_edit.height() - btn_size.height()) // 2
        
        toggle_btn.move(x, y)
        
    def toggle_password_visibility(self, line_edit, toggle_btn):
        """Alternar entre mostrar y ocultar la contraseña"""
        if not toggle_btn.password_visible:
            # Mostrar contraseña
            line_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
            if hasattr(toggle_btn, 'use_icons') and toggle_btn.use_icons:
                toggle_btn.setIcon(toggle_btn.eye_icon)
        else:
            # Ocultar contraseña
            line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
            if hasattr(toggle_btn, 'use_icons') and toggle_btn.use_icons:
                toggle_btn.setIcon(toggle_btn.eye_closed_icon)
        
        toggle_btn.password_visible = not toggle_btn.password_visible

    def setup_required_labels(self):
        """Crear etiquetas de 'obligatorio' debajo de cada campo"""
        # Estilo base para las etiquetas
        required_style = """
            QLabel { 
                color: red; 
                font-size: 14px; 
                padding-left: 5px;
            }
        """
        
        # Para cédula - insertar después del QLineEdit
        self.cedula_required_label = QtWidgets.QLabel("El campo cédula es obligatorio", self.lineEditCedula.parent())
        self.cedula_required_label.setStyleSheet(required_style)
        # Ajustar tamaño mínimo para mantener espacio
        self.cedula_required_label.setMinimumHeight(20)
        self.cedula_required_label.setMaximumHeight(20)
        index = self.verticalLayout_4.indexOf(self.lineEditCedula)
        self.verticalLayout_4.insertWidget(index + 1, self.cedula_required_label)
        
        # Para nombre - insertar después del QLineEdit
        self.nombre_required_label = QtWidgets.QLabel("El campo nombre es obligatorio", self.lineEditNombre.parent())
        self.nombre_required_label.setStyleSheet(required_style)
        self.nombre_required_label.setMinimumHeight(20)
        self.nombre_required_label.setMaximumHeight(20)
        index = self.verticalLayout_4.indexOf(self.lineEditNombre)
        self.verticalLayout_4.insertWidget(index + 1, self.nombre_required_label)
        
        # Para apellido - insertar después del QLineEdit
        self.apellido_required_label = QtWidgets.QLabel("El campo apellido es obligatorio", self.lineEditApellido.parent())
        self.apellido_required_label.setStyleSheet(required_style)
        self.apellido_required_label.setMinimumHeight(20)
        self.apellido_required_label.setMaximumHeight(20)
        index = self.verticalLayout_4.indexOf(self.lineEditApellido)
        self.verticalLayout_4.insertWidget(index + 1, self.apellido_required_label)
        
        # Para correo - insertar después del QLineEdit
        self.correo_required_label = QtWidgets.QLabel("El campo correo es obligatorio", self.lineEditCorreo.parent())
        self.correo_required_label.setStyleSheet(required_style)
        self.correo_required_label.setMinimumHeight(20)
        self.correo_required_label.setMaximumHeight(20)
        index = self.verticalLayout_4.indexOf(self.lineEditCorreo)
        self.verticalLayout_4.insertWidget(index + 1, self.correo_required_label)
        
        # Para contraseña - insertar después del QLineEdit
        self.pass_required_label = QtWidgets.QLabel("El campo contraseña es obligatorio (mínimo 8 caracteres)", self.lineEditPass.parent())
        self.pass_required_label.setStyleSheet(required_style)
        self.pass_required_label.setMinimumHeight(20)
        self.pass_required_label.setMaximumHeight(20)
        index = self.verticalLayout_4.indexOf(self.lineEditPass)
        self.verticalLayout_4.insertWidget(index + 1, self.pass_required_label)
        
        # Para confirmar contraseña - insertar después del QLineEdit
        self.confirm_required_label = QtWidgets.QLabel("El campo confirmar contraseña es obligatorio", self.lineEdit_3.parent())
        self.confirm_required_label.setStyleSheet(required_style)
        self.confirm_required_label.setMinimumHeight(20)
        self.confirm_required_label.setMaximumHeight(20)
        index = self.verticalLayout_4.indexOf(self.lineEdit_3)
        self.verticalLayout_4.insertWidget(index + 1, self.confirm_required_label)

        # Crear un diccionario para manejar fácilmente las etiquetas
        self.required_labels = {
            'cedula': self.cedula_required_label,
            'nombre': self.nombre_required_label,
            'apellido': self.apellido_required_label,
            'correo': self.correo_required_label,
            'pass': self.pass_required_label,
            'confirm': self.confirm_required_label
        }

    def update_label_style(self, label, is_visible):
        """Actualizar el estilo de la etiqueta según su visibilidad"""
        if is_visible:
            # Cuando está visible, mostrar texto rojo
            label.setStyleSheet("""
                QLabel { 
                    color: red; 
                    font-size: 14px; 
                    padding-left: 5px;
                }
            """)
            label.setVisible(True)
        else:
            # Cuando está oculta, hacer transparente pero mantener el espacio
            label.setStyleSheet("""
                QLabel { 
                    color: transparent; 
                    font-size: 14px; 
                    padding-left: 5px;
                }
            """)
            label.setVisible(True)  # ¡Importante! Mantener visible para conservar espacio

    def connect_text_changes(self):
        """Conectar las señales de cambio de texto para ocultar/mostrar etiquetas"""
        self.lineEditCedula.textChanged.connect(self.update_cedula_label)
        self.lineEditNombre.textChanged.connect(self.update_nombre_label)
        self.lineEditApellido.textChanged.connect(self.update_apellido_label)
        self.lineEditCorreo.textChanged.connect(self.update_correo_label)
        self.lineEditPass.textChanged.connect(self.update_pass_label)
        self.lineEdit_3.textChanged.connect(self.update_confirm_label)

        # Inicializar estado de las etiquetas
        self.update_cedula_label(self.lineEditCedula.text())
        self.update_nombre_label(self.lineEditNombre.text())
        self.update_apellido_label(self.lineEditApellido.text())
        self.update_correo_label(self.lineEditCorreo.text())
        self.update_pass_label(self.lineEditPass.text())
        self.update_confirm_label(self.lineEdit_3.text())

    def update_cedula_label(self, text):
        """Actualizar visibilidad de etiqueta de cédula"""
        self.update_label_style(self.cedula_required_label, not bool(text.strip()))

    def update_nombre_label(self, text):
        """Actualizar visibilidad de etiqueta de nombre"""
        self.update_label_style(self.nombre_required_label, not bool(text.strip()))

    def update_apellido_label(self, text):
        """Actualizar visibilidad de etiqueta de apellido"""
        self.update_label_style(self.apellido_required_label, not bool(text.strip()))

    def update_correo_label(self, text):
        """Actualizar visibilidad de etiqueta de correo"""
        self.update_label_style(self.correo_required_label, not bool(text.strip()))

    def update_pass_label(self, text):
        """Actualizar visibilidad de etiqueta de contraseña"""
        self.update_label_style(self.pass_required_label, not bool(text.strip()))

    def update_confirm_label(self, text):
        """Actualizar visibilidad de etiqueta de confirmación"""
        self.update_label_style(self.confirm_required_label, not bool(text.strip()))

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
        confirmPassword = self.lineEdit_3.text().strip()
        
        # Mostrar todas las etiquetas de obligatorio antes de validar
        # Solo mostrar aquellas que corresponden a campos vacíos
        self.update_cedula_label(cedula)
        self.update_nombre_label(fisrtName)
        self.update_apellido_label(lastName)
        self.update_correo_label(correo)
        self.update_pass_label(password)
        self.update_confirm_label(confirmPassword)
        
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
            self.comeBack()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Usuario no creado")