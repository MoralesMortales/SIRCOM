from app.windows.py.usersWds import Ui_Form
from app.database.auth.get import getAllUsers
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QLabel
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon, QFont
from app.database.auth.delete import deleteUser
from PyQt5 import QtGui

class UsersView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Administrar Usuarios")
        self.adjust_table_settings()
        self.load_data()
        self.btnCancelar.clicked.connect(self.cancelOperation)
                
    def adjust_table_settings(self):
        self.tableProducto.verticalHeader().setDefaultSectionSize(40)
        self.tableProducto.setSelectionBehavior(self.tableProducto.SelectRows)
        
        headers = ["Cedula", "Nombre", "Apellido", "Correo", "Estado", "Accion"]
        self.tableProducto.setColumnCount(len(headers))
        self.tableProducto.setHorizontalHeaderLabels(headers)
        
        header = self.tableProducto.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Ajustar ancho de columnas específicas
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Estado - ancho fijo
        self.tableProducto.setColumnWidth(4, 100)  # Ancho para columna Estado
        
        self.tableProducto.setSortingEnabled(True) 
        
    def load_data(self):
        rows = getAllUsers()
        from app import session
        ownCode = session.currentUserCedula
        
        self.tableProducto.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row[:4]):  # Solo las primeras 4 columnas de datos
                str_value = str(value)
                
                item = QTableWidgetItem(str(value))
                item.setToolTip(str_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                # Resaltar fila del usuario actual
                if str(row[0]) == str(ownCode):
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                
                self.tableProducto.setItem(row_idx, col_idx, item)
            
            # Columna 4: Estado (con icono si es el usuario actual)
            estado_widget = self.create_status_widget(row[0], ownCode)
            self.tableProducto.setCellWidget(row_idx, 4, estado_widget)
            
            # Columna 5: Acciones
            actions_widget = self.create_action_buttons(row_idx, row)
            self.tableProducto.setCellWidget(row_idx, 5, actions_widget)

    def create_status_widget(self, user_cedula, own_cedula):
        """Crea el widget para la columna de estado"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        if str(user_cedula) == str(own_cedula):
            # Usuario actual - mostrar icono y texto
            UserIcon = getIcon("User.png")
            
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(UserIcon).pixmap(16, 16))
            icon_label.setToolTip("Usuario actualmente conectado")
            
            text_label = QLabel("Admin")
            
            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            layout.setAlignment(Qt.AlignCenter)
        else:
            # Otro usuario
            text_label = QLabel("Usuario")
            layout.addWidget(text_label)
            layout.setAlignment(Qt.AlignCenter)
        
        return widget

    def create_action_buttons(self, row_idx, row_data):
        """Crea los botones de acción para cada fila"""
        TrashIcon = getIcon("Trash.png")
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) 

        layout.addStretch() 

        btnTrash = QPushButton()
        btnTrash.setIcon(QIcon(TrashIcon))
        btnTrash.setToolTip("Eliminar usuario")
        btnTrash.setCursor(Qt.PointingHandCursor)
        
        # Deshabilitar botón si es el usuario actual
        from app import session
        if str(row_data[0]) == str(session.currentUserCedula):
            btnTrash.setEnabled(False)
            btnTrash.setToolTip("No se puede eliminar el usuario en sesión")
            btnTrash.setStyleSheet("opacity: 0.5;")
        else:
            btnTrash.clicked.connect(lambda: self.handleTrash(row_data))

        layout.addWidget(btnTrash)
        layout.addStretch() 

        return widget

    def cancelOperation(self):
        from app.views.management.inventory.InventoryView import InventoryView 
        self.InventoryView = InventoryView()
        self.InventoryView.showMaximized()
        self.close()
    
    def handleTrash(self, data):
        code = data[0]
        
        from app import session
        ownCode = session.currentUserCedula

        if str(code) != str(ownCode):
            confirm = QMessageBox.question(
                self, 
                "Confirmar Eliminación", 
                f"¿Estás seguro de que deseas eliminar al usuario con cédula '{code}'?\n\n"
                f"Nombre: {data[1]} {data[2]}\n"
                f"Correo: {data[3]}\n\n"
                f"Esta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    deleteUser(code)
                    
                    QMessageBox.information(self, "Eliminado", 
                                          "Usuario eliminado correctamente.")
                    self.load_data() 
                    
                except Exception as e:
                    QMessageBox.critical(
                        self, 
                        "Error", 
                        f"No se pudo eliminar el usuario. Detalles: {str(e)}"
                    )
        else:
            QMessageBox.warning(
                self, 
                "Operación no permitida", 
                "No puedes eliminar tu propio usuario mientras estás en sesión."
            )