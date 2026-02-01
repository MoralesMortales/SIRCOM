from app.windows.py.inventoryWds import Ui_Form
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from app.database.auth.get import getInventoryProducts, getLiteralInventoryProduct
from app.database.auth.update import updateInventoryProductCode, updateInventoryProductQuantityMain, updateInventoryProductMinStock
from PyQt5 import QtGui

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
        background: #7f5b5f;
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
        
        # Nueva lista de headers
        headers = ["Código", "Producto", "Proveedor", "Stock", "Stock Mínimo", "Acciones"]
        self.tableWidgetInventario.setColumnCount(len(headers))
        self.tableWidgetInventario.setHorizontalHeaderLabels(headers)
        
        header = self.tableWidgetInventario.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetInventario.setSortingEnabled(True)
        
    def load_data(self):
        # Obtenemos los datos: (Cod, Prod, Prov, Stock, StockMin)
        rows = getInventoryProducts()
        self.tableWidgetInventario.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):
            # Índices basados en tu BD: 3 es Stock Actual, 4 es Stock Mínimo
            stock_actual = int(row[3])
            stock_minimo = int(row[4]) if len(row) > 4 else 0
            
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Bloqueamos la edición directa en la celda
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                # Aplicamos Tooltip general del contenido
                item.setToolTip(str(value))
                
                # Lógica de colores para la celda de Stock (Columna 3)
                if col_idx == 3 and stock_minimo > 0:
                    if stock_actual < stock_minimo:
                        item.setForeground(QtGui.QColor("#ff4d4d")) # Rojo
                        item.setToolTip(f"Alerta: Stock actual ({stock_actual}) menor al mínimo ({stock_minimo})")
                    else:
                        item.setForeground(QtGui.QColor("#228c22")) # Verde
                        item.setToolTip("Nivel de stock saludable")
                
                self.tableWidgetInventario.setItem(row_idx, col_idx, item)
                
            # Insertamos los botones de acción en la última columna (índice 5)
            actions_widget = self.create_action_buttons(row_idx, row)
            self.tableWidgetInventario.setCellWidget(row_idx, 5, actions_widget)
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
        # row_data: (Codigo, Producto, Proveedor, Stock, StockMin)
        codigo_actual = row_data[0]
        producto_nombre = row_data[1]
        stock_actual = int(row_data[3])
        stock_min_actual = int(row_data[4]) if len(row_data) > 4 else 0

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar: {producto_nombre}")
        dialog.setMinimumWidth(300)
        layout = QVBoxLayout(dialog)

        # --- Campo: Código ---
        layout.addWidget(QLabel("Código del Producto:"))
        edit_codigo = QLineEdit()
        edit_codigo.setText(str(codigo_actual))
        layout.addWidget(edit_codigo)

        # --- Campo: Stock Disponible (RESTRINGIDO) ---
        layout.addWidget(QLabel("Cantidad en Stock:"))
        spin_stock = QSpinBox()
        
        # EL CAMBIO ESTÁ AQUÍ:
        # Mínimo 0 (no puede ser negativo)
        # Máximo 'stock_actual' (no puede subir del valor que ya tiene)
        spin_stock.setRange(0, stock_actual) 
        
        spin_stock.setValue(stock_actual)
        spin_stock.setAlignment(Qt.AlignCenter)
        layout.addWidget(spin_stock)

        # --- Campo: Stock Mínimo ---
        layout.addWidget(QLabel("Stock Mínimo:"))
        spin_min = QSpinBox()
        spin_min.setRange(0, 9999)
        spin_min.setValue(stock_min_actual)
        spin_min.setAlignment(Qt.AlignCenter)
        layout.addWidget(spin_min)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            nuevo_codigo_str = edit_codigo.text().strip()
            
            if not nuevo_codigo_str:
                QMessageBox.warning(self, "Error", "El código no puede estar vacío.")
                return

            try:
                nuevo_codigo_int = int(nuevo_codigo_str)
                nueva_cantidad = spin_stock.value()
                
                nuevo_minimo = spin_min.value()

                self.save_changes(codigo_actual, nuevo_codigo_int, nueva_cantidad, nuevo_minimo)
                
            except ValueError:
                QMessageBox.warning(self, "Error", "El código debe ser un valor numérico.")
    def save_changes(self, cod_viejo, cod_nuevo, cant_nueva, min_nuevo):
        # Aseguramos que los códigos sean tratados correctamente
        cod_viejo = int(cod_viejo)
        cod_nuevo = int(cod_nuevo)
        
        try:
            # 1. Lógica de cambio de CÓDIGO
            codigo_final = cod_viejo # Por defecto usamos el viejo para las queries
            
            if cod_nuevo != cod_viejo:
                # Verificar si el código nuevo ya existe para no duplicar
                if getLiteralInventoryProduct(cod_nuevo):
                    QMessageBox.critical(self, "Error", f"El código {cod_nuevo} ya está en uso por otro producto.")
                    return # Cancelamos toda la operación
                
                # Si no existe, procedemos a cambiar el código en la BD
                if updateInventoryProductCode(cod_viejo, cod_nuevo):
                    print(f"Código actualizado de {cod_viejo} a {cod_nuevo}")
                    codigo_final = cod_nuevo # Ahora las siguientes updates usarán el código nuevo
                else:
                    raise Exception("Error al actualizar el código en la base de datos.")

            res_stock = updateInventoryProductQuantityMain(codigo_final, cant_nueva)
            res_min = updateInventoryProductMinStock(codigo_final, min_nuevo)

            if res_stock and res_min:
                QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            else:
                QMessageBox.warning(self, "Advertencia", "Se actualizó el código pero hubo un problema con los valores de stock.")

        except Exception as e:
            QMessageBox.critical(self, "Error de Base de Datos", f"No se pudo completar la operación: {str(e)}")
        
        # Finalmente refrescamos la tabla para ver los cambios y colores (verde/rojo)
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