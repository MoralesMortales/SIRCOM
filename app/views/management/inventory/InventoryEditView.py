from app.windows.py.inventoryEditWds import Ui_Form
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon

from app.database.auth.get import getInventoryProducts

class InventoryEditView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inventario")
        self.adjust_table_settings()
        self.load_data()

        #tabs
        self.menuItemRecursos.mousePressEvent = lambda event: self.tabLogic("Buy")
        self.menuItemProveedores.mousePressEvent = lambda event: self.tabLogic("Provider")
        self.menuItemHistorial.mousePressEvent = lambda event: self.tabLogic("History")

        #styles
        self.menuItemInventario.setStyleSheet("""
        #menu QWidget {
        background: #e0e0e0;
        }""")
        
        self.menuItemHistorial.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemInventario.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemProveedores.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemRecursos.setCursor(QtCore.Qt.PointingHandCursor)
        
    def tabLogic(self, tab):
        if tab == "Buy":
            from app.views.management.buy.BuyView import BuyView
            
            self.BuyView = BuyView()
            self.BuyView.showMaximized()
            self.close()
            
        elif tab == "Provider":
            from app.views.management.providers.ProvidersView import ProvidersView
            
            self.ProvidersView = ProvidersView()
            self.ProvidersView.showMaximized()
            self.close()
            
        elif tab == "History":
            from app.views.management.history.HistoryView import HistoryView
            
            self.HistoryView = HistoryView()
            self.HistoryView.showMaximized()
            self.close()
            
    
    def adjust_table_settings(self):

        self.tableWidgetInventario.verticalHeader().setDefaultSectionSize(40)
        
        self.tableWidgetInventario.setSelectionBehavior(self.tableWidgetInventario.SelectRows)
        
        headers = ["Codigo", "Producto", "Proveedor", "Stock", "Acciones"]
        self.tableWidgetInventario.setColumnCount(len(headers))
        self.tableWidgetInventario.setHorizontalHeaderLabels(headers)
        
        header = self.tableWidgetInventario.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.tableWidgetInventario.setSortingEnabled(True) 
        
    def load_data(self):
        rows = getInventoryProducts()
        
        print(rows)

        self.tableWidgetInventario.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                str_value = str(value)
                
                item = QTableWidgetItem(str(value))
                item.setToolTip(str_value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                self.tableWidgetInventario.setItem(row_idx, col_idx, item)
                
            actions_widget = self.create_action_buttons(row_idx, row)
            self.tableWidgetInventario.setCellWidget(row_idx, 4, actions_widget)

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

        return widget