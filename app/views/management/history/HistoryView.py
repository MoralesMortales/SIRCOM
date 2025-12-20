from app.windows.py.historyWds import Ui_Form
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
from app.functions.tools.getIcon import getIcon
from app.database.auth.get import getAllCompras, geUserName
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta


class HistoryView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Historial de Acciones")
        self.adjust_table_settings()
        self.load_data()

        #tabs
        self.menuItemInventario.mousePressEvent = lambda event: self.tabLogic("Inventory")
        self.menuItemProveedores.mousePressEvent = lambda event: self.tabLogic("Provider")
        self.menuItemRecursos.mousePressEvent = lambda event: self.tabLogic("Buy")
        
        #styles
        self.menuItemHistorial.setStyleSheet("""
        #menu QWidget {
        background: #e0e0e0;
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
            
        elif tab == "Provider":
            from app.views.management.providers.ProvidersView import ProvidersView
            
            self.ProvidersView = ProvidersView()
            self.ProvidersView.showMaximized()
            self.close()
            
        elif tab == "Buy":
            from app.views.management.buy.BuyView import BuyView
            
            self.BuyView = BuyView()
            self.BuyView.showMaximized()
            self.close()
   
    def adjust_table_settings(self):

        self.tableWidgetHistorial.verticalHeader().setDefaultSectionSize(40)
        
        self.tableWidgetHistorial.setSelectionBehavior(self.tableWidgetHistorial.SelectRows)
        
        headers = ["Codigo", "Usuario", "Fecha", "Hora", "Total", "Ver Factura"]
        self.tableWidgetHistorial.setColumnCount(len(headers))
        self.tableWidgetHistorial.setHorizontalHeaderLabels(headers)
        self.tableWidgetHistorial.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        header = self.tableWidgetHistorial.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetHistorial.setColumnHidden(0, True)

        self.tableWidgetHistorial.setSortingEnabled(True) 
        
    def create_action_buttons(self, row_idx, row_data):
        
        EyeIcon = getIcon("Eye.png")

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) 

        layout.addStretch() 

        btn_edit = QPushButton()
        btn_edit.setIcon(QIcon(EyeIcon))
        btn_edit.setToolTip("Editar")
        btn_edit.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_edit)
        btn_edit.clicked.connect(lambda: self.handlePurchaseView(row_data))
  
        layout.addStretch() 

        return widget
    
    def load_data(self):
        raw_rows = getAllCompras()
        
        new_rows = []
        
        for row in raw_rows:
            code = row[0]
            username = row[1]
            fecha_str = row[2]
            total = row[3]
            total = str(total)
            total += " $"
            dt_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            
            dt_local = dt_obj - timedelta(hours=4)
            
            solo_fecha = dt_local.strftime('%d-%m-%Y')
            solo_hora = dt_local.strftime('%I:%M %p')
            
            new_rows.append((code, username, solo_fecha, solo_hora, total))
        
            self.tableWidgetHistorial.setRowCount(len(new_rows))
            
            for row_idx, row in enumerate(new_rows):
                for col_idx, value in enumerate(row):
                    str_value = str(value)
                    
                    item = QTableWidgetItem(str(value))
                    item.setToolTip(str_value)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    
                    self.tableWidgetHistorial.setItem(row_idx, col_idx, item)
                    
                actions_widget = self.create_action_buttons(row_idx, row)
                self.tableWidgetHistorial.setCellWidget(row_idx, 5, actions_widget)

    def handlePurchaseView(self, data):
        from app.views.management.history.PurchaseView import PurchaseView
        
        self.PurchaseView = PurchaseView()
        self.PurchaseView.openWindow(data)
        self.close()