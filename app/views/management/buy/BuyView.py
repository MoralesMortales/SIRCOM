from app.windows.py.buyWds import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5 import QtCore
from app.database.management.loadProducts import getAllProducts
from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from app.functions.tools.getIcon import getIcon
from PyQt5.QtWidgets import QSpinBox 

class BuyView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Comprar Recursos")
        self.tableWidgetInventario.verticalHeader().setDefaultSectionSize(40)
        #tabs
        self.menuItemInventario.mousePressEvent = lambda event: self.tabLogic("Inventory")
        self.menuItemProveedores.mousePressEvent = lambda event: self.tabLogic("Provider")
        self.menuItemHistorial.mousePressEvent = lambda event: self.tabLogic("History")
        self.lineEditBuscar.textChanged.connect(self.filter_products)

        #styles
        self.menuItemRecursos.setStyleSheet("""
        #menu QWidget {
        background: #e0e0e0;
        }""")
        
        self.menuItemHistorial.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemInventario.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemProveedores.setCursor(QtCore.Qt.PointingHandCursor)
        self.menuItemRecursos.setCursor(QtCore.Qt.PointingHandCursor)
        
        self.btnComprar.clicked.connect(self.proceedPayment)
        
        self.adjust_table_settings()
        self.load_data()

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
            
        elif tab == "History":
            from app.views.management.history.HistoryView import HistoryView
            
            self.HistoryView = HistoryView()
            self.HistoryView.showMaximized()
            self.close()
            
    def load_data(self):
        rows = getAllProducts() 
        self.tableWidgetInventario.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):
            
            stock_disponible = int(row[3])
            price_str = f"{row[4]} $"

            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setToolTip(str(value))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidgetInventario.setItem(row_idx, col_idx, item)

            price_item = QTableWidgetItem(price_str)
            price_item.setTextAlignment(Qt.AlignCenter)
            price_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tableWidgetInventario.setItem(row_idx, 4, price_item)
                        
            spin_qty = QSpinBox()
            spin_qty.setRange(0, stock_disponible - 1)
            spin_qty.setValue(0) 
            spin_qty.setAlignment(Qt.AlignCenter)
            spin_qty.setButtonSymbols(QSpinBox.NoButtons) 
            self.tableWidgetInventario.setCellWidget(row_idx, 5, spin_qty)
            actions_widget = self.create_action_buttons(row_idx, row) 
            self.tableWidgetInventario.setCellWidget(row_idx, 6, actions_widget)

    def update_quantity(self, row, delta):
        spin_box = self.tableWidgetInventario.cellWidget(row, 5)
        if spin_box:
            current_qty = spin_box.value()
            new_qty = current_qty + delta
            if new_qty >= 0:
                spin_box.setValue(new_qty)

    def get_selected_products(self):
        purchased_items = []
        for row in range(self.tableWidgetInventario.rowCount()):
            spin_box = self.tableWidgetInventario.cellWidget(row, 4)
            qty = spin_box.value()
            
            if qty > 0:
                item_data = {
                    "product": self.tableWidgetInventario.item(row, 0).text(),
                    "provider": self.tableWidgetInventario.item(row, 1).text(),
                    "quantity": qty,
                    "price": self.tableWidgetInventario.item(row, 3).text()
                }
                purchased_items.append(item_data)
        
        print("Productos cargados:", purchased_items)
        return purchased_items
    
    def create_action_buttons(self, row_idx, row_data):
        
        height = 18
        width = 20
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(30) 

        btnSum = QPushButton()
        btnSum.setIcon(QIcon(getIcon("Sum.png")))
        btnSum.setFixedHeight(height)
        btnSum.setFixedWidth(width)
        btnSum.setStyleSheet("background-color:#D9D9D9; border:none;")
        
        btnSum.setCursor(Qt.PointingHandCursor)
        btnSum.clicked.connect(lambda _, r=row_idx: self.update_quantity(r, 1))
        
        btnMinus = QPushButton()
        btnMinus.setIcon(QIcon(getIcon("Minus.png")))
        btnMinus.setFixedHeight(height)
        btnMinus.setFixedWidth(width)
        btnMinus.setStyleSheet("background-color:#D9D9D9; border:none;")
        btnMinus.setCursor(Qt.PointingHandCursor)
        btnMinus.clicked.connect(lambda _, r=row_idx: self.update_quantity(r, -1))

        layout.addWidget(btnMinus)
        layout.addWidget(btnSum)
        return widget

    def adjust_table_settings(self):
        self.tableWidgetInventario.setSelectionBehavior(self.tableWidgetInventario.SelectRows)
        self.tableWidgetInventario.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        headers = ["ID", "Articulo", "Proveedor", "Stock", "Precio", "Cantidad", "Acciones"]
        self.tableWidgetInventario.setColumnCount(len(headers))
        self.tableWidgetInventario.setHorizontalHeaderLabels(headers)
        
        self.tableWidgetInventario.setColumnHidden(0, True)
        
        header = self.tableWidgetInventario.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

    def proceedPayment(self):
        from app.views.management.buy.ConfirmPurchaseView import ConfirmPurchaseView
        self.ConfirmPurchaseView = ConfirmPurchaseView()
                
        if self.getPurchaseList():
            self.ConfirmPurchaseView.openWindow(self.getPurchaseList())
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "No hay productos que comprar.")

    def getPurchaseList(self):
        purchased_items = []
        for row in range(self.tableWidgetInventario.rowCount()):
            spin_box = self.tableWidgetInventario.cellWidget(row, 5)
            qty = spin_box.value()
            
            if qty > 0:
                product_id = self.tableWidgetInventario.item(row, 0).text()
                
                item_data = {
                    "id": product_id,
                    "quantity": qty
                }
                purchased_items.append(item_data)
        
        return purchased_items
    
    def filter_products(self):
        search_text = self.lineEditBuscar.text().lower()
        
        # Recorrer todas las filas de la tabla
        for row_idx in range(self.tableWidgetInventario.rowCount()):
            # Obtenemos el ítem de la columna "Producto" (índice 1)
            item = self.tableWidgetInventario.item(row_idx, 1)
            
            if item is not None:
                # Comparamos el texto de la celda con el de búsqueda
                product_name = item.text().lower()
                
                # Si el texto de búsqueda está contenido en el nombre, mostramos la fila
                if search_text in product_name:
                    self.tableWidgetInventario.setRowHidden(row_idx, False)
                else:
                    # Si no coincide, ocultamos la fila
                    self.tableWidgetInventario.setRowHidden(row_idx, True)