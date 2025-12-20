from app.windows.py.inventoryWds import Ui_Form
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from app.database.auth.get import getInventoryProducts, getLiteralInventoryProduct
from app.database.auth.update import updateInventoryProductCode, updateInventoryProductQuantity

class InventoryView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inventario")
        self.adjust_table_settings()
        self.load_data()
        self.lineEditBuscar.textChanged.connect(self.filter_products)

        #tabs
        self.menuItemRecursos.mousePressEvent = lambda event: self.tabLogic("Buy")
        self.menuItemProveedores.mousePressEvent = lambda event: self.tabLogic("Provider")
        self.menuItemHistorial.mousePressEvent = lambda event: self.tabLogic("History")

        #styles
        self.menuItemInventario.setStyleSheet("""
        #menu QWidget {
        background: #e0e0e0;
        }""")
        
        self.labelAdminUsers.mousePressEvent = self.openUsersView

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
            
    def openUsersView(self, event):
        from app.views.management. ManageUsers import UsersView
        
        self.UsersView = UsersView()
        self.UsersView.showMaximized()
        self.close()
    
    def adjust_table_settings(self):

        self.tableWidgetInventario.verticalHeader().setDefaultSectionSize(40)
        
        self.tableWidgetInventario.setSelectionBehavior(self.tableWidgetInventario.SelectRows)
        
        headers = ["Código", "Producto", "Proveedor", "Stock", "Acciones"]
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

    def handle_edit(self, row_data):
        # row_data contiene (Codigo, Producto, Proveedor, Stock)
        codigo_actual = row_data[0]
        producto_nombre = row_data[1]
        stock_actual = int(row_data[3])

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar: {producto_nombre}")
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel("Editar Código:"))
        edit_codigo = QLineEdit()
        edit_codigo.setText(str(codigo_actual))
        layout.addWidget(edit_codigo)

        layout.addWidget(QLabel(f"Cantidad actual:"))
        spin_stock = QSpinBox()
        spin_stock.setRange(0, stock_actual)
        spin_stock.setValue(stock_actual)
        layout.addWidget(spin_stock)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            nuevo_codigo = edit_codigo.text()
            nueva_cantidad = spin_stock.value()

            # Validaciones
            try:
                nuevo_codigo_int = int(nuevo_codigo)
            except ValueError:
                QMessageBox.warning(self, "Error", "El código debe ser un número entero.")
                return

            self.save_changes(codigo_actual, nuevo_codigo_int, nueva_cantidad)
            
    
    def save_changes(self, cod_viejo, cod_nuevo, cantidad_nueva):
        cod_viejo = int(cod_viejo)
        cod_nuevo = int(cod_nuevo)
        
        try:
            if cod_nuevo != cod_viejo:
                if getLiteralInventoryProduct(cod_nuevo):
                    QMessageBox.critical(self, "Error", f"El código {cod_nuevo} ya está en uso por otro producto.")
                    return

                updateInventoryProductCode(cod_viejo, cod_nuevo)
                print(f"Código actualizado de {cod_viejo} a {cod_nuevo}")
            
            codigo_para_query = cod_nuevo 
            updateInventoryProductQuantity(codigo_para_query, cantidad_nueva)
            print(f"Cantidad actualizada a {cantidad_nueva}")
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")

        except Exception as e:
            error_msg = str(e)
            QMessageBox.critical(self, "Error de Base de Datos", f"No se pudo actualizar: {error_msg}")
        
        self.load_data()
    
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