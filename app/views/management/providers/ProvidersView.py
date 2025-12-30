from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QMessageBox
from app.windows.py.providersWds import Ui_Form
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from app.database.management.loadProviders import getAllProviders
from app.views.management.providers.AddProviderView import AddProviderView
from app.functions.tools.getIcon import getIcon
from app.database.auth.delete import deleteProvider
from app.database.auth.get import getProviderData
from PyQt5 import QtCore

class ProvidersView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Proveedores")
        self.adjust_table_settings()
        self.load_data()
        self.AddProviderView = AddProviderView()
        self.btnAdd.clicked.connect(self.goToAddProvider)
        
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
        
        headers = ["RIF", "Empresa", "Dirreccion", "Telefono", "Correo", "Acciones"]
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
                    formatedRif = 'J-'
                    value = str(value)
                    for i in range(len(value)):
                        if i < 8:
                            formatedRif += value[i]
                        else:
                            formatedRif += ("-" + value[i]) 
                    value = formatedRif  
              
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
