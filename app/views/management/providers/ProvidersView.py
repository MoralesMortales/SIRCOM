from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QMessageBox, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from app.windows.py.providersWds import Ui_Form
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from app.database.management.loadProviders import getAllProviders
from app.views.management.providers.AddProviderView import AddProviderView
from app.functions.tools.getIcon import getIcon
from app.database.auth.delete import deleteProvider
from app.database.auth.get import getProviderData
from PyQt5 import QtCore
import sys

class ProvidersView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Proveedores")
        self.adjust_table_settings()
        self.load_data()
        self.AddProviderView = AddProviderView()
        self.btnAdd.clicked.connect(self.goToAddProvider)
        
        # Agregar botón de cerrar sesión AL FINAL DEL LAYOUT EXISTENTE
        self.setup_logout_button()
        
        #tabs
        self.menuItemInventario.mousePressEvent = lambda event: self.tabLogic("Inventory")
        self.menuItemRecursos.mousePressEvent = lambda event: self.tabLogic("Buy")
        self.menuItemHistorial.mousePressEvent = lambda event: self.tabLogic("History")
        
        #styles
        self.menuItemProveedores.setStyleSheet("""
        #menu QWidget {
        background: #7f5b5f;
        }""")
        
        self.menuItemHistorial.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemInventario.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemProveedores.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemRecursos.setCursor(QtCore.Qt.PointingHandCursor)
        
    def setup_logout_button(self):
        """Configura el botón de cerrar sesión en la parte inferior derecha"""
        # Crear un layout horizontal para el pie de página
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(20, 10, 20, 15)
        
        # Espaciador a la izquierda
        footer_layout.addStretch()
        
        # Crear label para cerrar sesión (parecido a un botón)
        self.logout_label = QLabel("Cerrar sesión")
        self.logout_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 13px;
                padding: 8px 20px;
                border: 1px solid #3a6365;
                border-radius: 4px;
                font-weight: bold;
                background-color: #f5f5f5;
            }
            QLabel:hover {
                color: #d32f2f;
                border-color: #d32f2f;
                background-color: #ffebee;
            }
        """)
        self.logout_label.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Conectar el click
        self.logout_label.mousePressEvent = self.handle_logout_click
        
        # Tooltip
        self.logout_label.setToolTip("Cerrar sesión")
        
        footer_layout.addWidget(self.logout_label)
        
        # Agregar el layout de pie de página AL FINAL del layout vertical existente
        self.verticalLayout.addLayout(footer_layout)
    
    def handle_logout_click(self, event):
        """Maneja el clic en el botón de cerrar sesión"""
        confirm = QMessageBox.question(
            self,
            "Confirmar cierre de sesión",
            "¿Estás seguro de que deseas cerrar sesión?.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Importar session para limpiar datos
            from app import session
            
            # Limpiar datos de sesión
            session.currentUserCedula = None
            session.currentUserUsername = None
            session.isLogged = False
            
            # Cerrar la aplicación
            self.close_application()
    
    def close_application(self):
        """Cierra la aplicación completamente"""
        try:
            # Abrir la pantalla de login
            self.open_login_screen()
        except Exception as e:
            print(f"Error cerrando aplicación: {e}")
            # Si hay error, cerrar la ventana actual
            self.close()
    
    def open_login_screen(self):
        """Abre la pantalla de login"""
        try:
            from app.views.auth.LoginView import LoginView
            self.login_view = LoginView()
            self.login_view.showMaximized()
            self.close()
        except Exception as e:
            print(f"Error abriendo pantalla de login: {e}")
            # Si hay error, cerrar la ventana actual
            self.close()
    
    def tabLogic(self, tab):
        if tab == "Inventory":
            from app.views.management.inventory.InventoryView import InventoryView
            
            self.InventoryView = InventoryView()
            self.InventoryView.showMaximized()
            self.close()
            
        elif tab == "Buy":
            from app.views.management.buy.BuyView import BuyView
            
            self.BuyView = BuyView()
            self.BuyView.showMaximized()
            self.close()
            
        elif tab == "History":
            from app.views.management.history.HistoryView import HistoryView
            
            self.HistoryView = HistoryView()
            self.HistoryView.showMaximized()
            self.close()
    
    def adjust_table_settings(self):
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        
        self.tableWidget.setSelectionBehavior(self.tableWidget.SelectRows)
        
        headers = ["RIF", "Empresa", "Dirección", "Telefono", "Correo", "Acciones"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.tableWidget.setSortingEnabled(True) 
            
    def goToAddProvider(self):
        self.AddProviderView.showMaximized()
        self.close()
        
    def load_data(self):
        rows = getAllProviders()

        self.tableWidget.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                str_value = str(value)
                
                if col_idx == 0:
                    # Formatear RIF
                    if isinstance(value, str) and len(value) > 0 and value[0] in ['G', 'V', 'J']:
                        # Si ya tiene formato (G-, V-, J-)
                        formatedRif = value
                    else:
                        # Si es solo número, asumir que es J- (Jurídico)
                        value_str = str(value)
                        if len(value_str) == 9:  # RIF Jurídico: 9 dígitos
                            formatedRif = f"J-{value_str[:8]}-{value_str[8:]}"
                        elif len(value_str) == 8:  # Personal/Gubernamental
                            formatedRif = f"J-{value_str}"
                        else:
                            formatedRif = value_str
                    value = formatedRif  
                
                elif col_idx == 3:  # Columna de teléfono
                    # Asegurar que el teléfono empiece con 0 y tenga 11 dígitos
                    telefono_str = str(value).strip()
                    
                    # Si es un número entero, convertirlo a string con ceros a la izquierda
                    if telefono_str.isdigit():
                        # Asegurar que tenga 11 dígitos
                        if len(telefono_str) == 11:
                            # Ya tiene 11 dígitos, asegurar que empiece con 0
                            if not telefono_str.startswith('0'):
                                telefono_str = '0' + telefono_str[1:] if len(telefono_str) == 11 else '0' + telefono_str
                        elif len(telefono_str) == 10:
                            # Tiene 10 dígitos, agregar 0 al inicio
                            telefono_str = '0' + telefono_str
                        elif len(telefono_str) < 10:
                            # Menos de 10 dígitos, llenar con ceros a la izquierda
                            telefono_str = '0' + telefono_str.zfill(10)
                        
                        # Formatear con guión: 0412-1234567
                        if len(telefono_str) >= 11:
                            telefono_str = f"{telefono_str[:4]}-{telefono_str[4:]}"
                    
                    value = telefono_str
              
                item = QTableWidgetItem(str(value))
                item.setToolTip(str_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                self.tableWidget.setItem(row_idx, col_idx, item)
                
            actions_widget = self.create_action_buttons(row_idx, row)
            self.tableWidget.setCellWidget(row_idx, 5, actions_widget)
            
    def create_action_buttons(self, row_idx, row_data):
        
        SumIcon = getIcon("Edit.png")
        MinusIcon = getIcon("Trash.png")

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) 

        layout.addStretch() 

        btn_edit = QPushButton()
        btn_edit.setIcon(QIcon(SumIcon))
        btn_edit.setToolTip("Editar")
        btn_edit.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_edit)
        btn_edit.clicked.connect(lambda: self.handle_edit(row_data))
  
        layout.addStretch() 

        btn_delete = QPushButton()
        btn_delete.setIcon(QIcon(MinusIcon))
        btn_delete.setToolTip("Eliminar")
        btn_delete.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_delete)
        btn_delete.clicked.connect(lambda: self.handle_delete(row_data))
        layout.addStretch() 

        return widget

    def handle_edit(self, data):
        from app.views.management.providers.EditProviderView import EditProviderView
        
        self.EditProviderView = EditProviderView()
        print(data[0], "aaaa")
        self.EditProviderView.openWindow(data[0])
        self.close()

    def handle_delete(self, data):
        rif_original = data[0]

        providerData = getProviderData(data[0])
        businessName = providerData[0]
        
        confirm = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Estás seguro de que deseas eliminar al proveedor '{businessName}'?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                # 2. Llamar a la función de la base de datos
                deleteProvider(rif_original)
                
                # 3. Notificar éxito y recargar los datos
                QMessageBox.information(self, "Eliminado", "Proveedor eliminado correctamente.")
                self.load_data() 
                
            except Exception as e:
                # Manejar errores (por ejemplo, si tiene productos asociados)
                QMessageBox.critical(
                    self, 
                    "Error", 
                    f"No se pudo eliminar el proveedor. Detalles: {str(e)}"
                )