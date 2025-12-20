from app.windows.py.usersWds import Ui_Form
from app.database.auth.get import getAllUsers
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon
from app.database.auth.delete import deleteUser
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
        
        headers = ["Cedula", "Nombre", "Apellido", "Correo", "Accion"]
        self.tableProducto.setColumnCount(len(headers))
        self.tableProducto.setHorizontalHeaderLabels(headers)
        
        header = self.tableProducto.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.tableProducto.setSortingEnabled(True) 
        
    def load_data(self):
        rows = getAllUsers()
        print(rows)
        
        print(rows)

        self.tableProducto.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                str_value = str(value)
                
                item = QTableWidgetItem(str(value))
                item.setToolTip(str_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                self.tableProducto.setItem(row_idx, col_idx, item)
                
            actions_widget = self.create_action_buttons(row_idx, row)
            self.tableProducto.setCellWidget(row_idx, 4, actions_widget)

    def create_action_buttons(self, row_idx, row_data):
        
        TrashIcon = getIcon("Trash.png")

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) 

        layout.addStretch() 

        btnTrash = QPushButton()
        btnTrash.setIcon(QIcon(TrashIcon))
        btnTrash.setToolTip("Eliminar")
        btnTrash.setCursor(Qt.PointingHandCursor)
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
        
        if code != ownCode:
            confirm = QMessageBox.question(
                self, 
                "Confirmar Eliminación", 
                f"¿Estás seguro de que deseas eliminar al usuario de la cedula '{code}'?\nEsta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    deleteUser(code)
                    
                    QMessageBox.information(self, "Eliminado", "Usuario eliminado correctamente.")
                    self.load_data() 
                    
                except Exception as e:
                    QMessageBox.critical(
                        self, 
                        "Error", 
                        f"No se pudo eliminar el usuario. Detalles: {str(e)}"
                    )
        else:
            QMessageBox.critical(
                        self, 
                        "Error", 
                        f"No se puede eliminar el usuario que esta usando actualmente."
                    )
