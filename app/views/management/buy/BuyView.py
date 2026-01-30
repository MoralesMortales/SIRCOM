from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTableWidgetItem, QHeaderView, QSpinBox, QMessageBox, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from app.windows.py.buyWds import Ui_Form
from app.database.management.loadProducts import getAllProducts
from app.functions.tools.getIcon import getIcon

class BuyView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Comprar Recursos")
        
        self.setup_total_label()
        
        self.tableWidgetInventario.verticalHeader().setDefaultSectionSize(40)
        
        self.menuItemInventario.mousePressEvent = lambda event: self.tabLogic("Inventory")
        self.menuItemProveedores.mousePressEvent = lambda event: self.tabLogic("Provider")
        self.menuItemHistorial.mousePressEvent = lambda event: self.tabLogic("History")
        self.lineEditBuscar.textChanged.connect(self.filter_products)

        self.menuItemRecursos.setStyleSheet("#menu QWidget { background: #7f5b5f; }")
        for item in [self.menuItemHistorial, self.menuItemInventario, self.menuItemProveedores, self.menuItemRecursos]:
            item.setCursor(Qt.PointingHandCursor)
        
        self.btnComprar.clicked.connect(self.proceedPayment)
        
        self.adjust_table_settings()
        self.load_data()

    def setup_total_label(self):
        self.labelTotalGeneral = QLabel("TOTAL GENERAL: 0.00 $")
        self.labelTotalGeneral.setObjectName("labelTotalGeneral")
        self.labelTotalGeneral.setStyleSheet("""
            QLabel#labelTotalGeneral {
                font-weight: bold; 
                color: #2E7D32; 
                font-size: 20px;
                padding: 5px;
            }
        """)
        self.horizontalLayout_9.insertWidget(0, self.labelTotalGeneral)

    def adjust_table_settings(self):
        """Configura las columnas y el comportamiento de redimensionamiento"""
        self.tableWidgetInventario.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        headers = [
            "Oferta", "Código", "Artículo", "Proveedor", 
            "Cantidad", "Mín. Pedido", "Existencia", "Precio Unit.", "Total + IVA", "Acciones"
        ]
        
        self.tableWidgetInventario.setColumnCount(len(headers))
        self.tableWidgetInventario.setHorizontalHeaderLabels(headers)
        
        header = self.tableWidgetInventario.horizontalHeader()
        header.setStretchLastSection(False) 
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_data(self):
        rows = getAllProducts() 
        self.tableWidgetInventario.setRowCount(len(rows)) 
        
        for row_idx, row in enumerate(rows):

            txt_oferta = f"{row[0]}% desde {row[1]} un."
            item_desc = QTableWidgetItem(txt_oferta)
            item_desc.setData(Qt.UserRole, row[0])     
            item_desc.setData(Qt.UserRole + 1, row[1])  
            item_desc.setToolTip(f"Descuento especial: Reducción del {row[0]}% al comprar {row[1]} unidades o más.")
            item_desc.setTextAlignment(Qt.AlignCenter)
            self.tableWidgetInventario.setItem(row_idx, 0, item_desc)

            self.set_table_item(row_idx, 1, row[2]) # Código
            self.set_table_item(row_idx, 2, row[3]) # Artículo
            self.set_table_item(row_idx, 3, row[4]) # Proveedor

            stock_max = int(row[5])
            spin_qty = QSpinBox()
            spin_qty.setRange(0, stock_max)
            spin_qty.setAlignment(Qt.AlignCenter)
            spin_qty.setButtonSymbols(QSpinBox.NoButtons)
            spin_qty.setToolTip(f"Stock disponible del proveedor: {stock_max} unidades.")
            spin_qty.valueChanged.connect(lambda _, r=row_idx: self.calculate_row_total(r))
            self.tableWidgetInventario.setCellWidget(row_idx, 4, spin_qty)

            self.set_table_item(row_idx, 5, row[6]) 
            self.set_table_item(row_idx, 6, row[5])
            self.set_table_item(row_idx, 7, f"{row[7]} $") 
            
            item_total = QTableWidgetItem("0.00 $")
            item_total.setTextAlignment(Qt.AlignCenter)
            item_total.setToolTip("Costo total de esta fila incluyendo impuestos.")
            self.tableWidgetInventario.setItem(row_idx, 8, item_total)
            
            self.tableWidgetInventario.setCellWidget(row_idx, 9, self.create_action_buttons(row_idx))

    def set_table_item(self, row, col, value):
        text_value = str(value)
        item = QTableWidgetItem(text_value)
        item.setTextAlignment(Qt.AlignCenter)
        item.setToolTip(text_value) 
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidgetInventario.setItem(row, col, item)

    def calculate_row_total(self, row):
        """Calcula el subtotal con descuentos e IVA, actualizando tooltips"""
        spin_box = self.tableWidgetInventario.cellWidget(row, 4)
        qty = spin_box.value() if spin_box else 0
        
        try:
            price = float(self.tableWidgetInventario.item(row, 7).text().replace(" $", "").replace(",", ""))
        except: price = 0.0
            
        item_desc = self.tableWidgetInventario.item(row, 0)
        p_desc = item_desc.data(Qt.UserRole)
        min_qty_desc = item_desc.data(Qt.UserRole + 1)
        
        min_pedido = int(self.tableWidgetInventario.item(row, 5).text())
        if 0 < qty < min_pedido:
            spin_box.setStyleSheet("background-color: #ffebee; border: 1px solid #ef5350;")
            spin_box.setToolTip(f"¡Pedido Insuficiente! El proveedor exige al menos {min_pedido} unidades.")
        else:
            spin_box.setStyleSheet("")
            spin_box.setToolTip(f"Cantidad seleccionada: {qty}")

        subtotal_bruto = price * qty
        descuento_aplicado = 0.0
        
        if qty >= min_qty_desc and p_desc > 0:
            descuento_aplicado = subtotal_bruto * (p_desc / 100)
        
        subtotal_neto = subtotal_bruto - descuento_aplicado
        total_con_iva = subtotal_neto * 1.16 # IVA del 16%
        
        item_total = self.tableWidgetInventario.item(row, 8)
        item_total.setText(f"{total_con_iva:,.2f} $")
        
        detalle_tooltip = (
            f"<b>Desglose de Pago:</b><br>"
            f"Subtotal Base: {subtotal_bruto:,.2f} $<br>"
            f"Descuento ({p_desc}%): -{descuento_aplicado:,.2f} $<br>"
            f"IVA (16%): {(total_con_iva - subtotal_neto):,.2f} $<br>"
            f"<hr><b>Total Fila: {total_con_iva:,.2f} $</b>"
        )
        item_total.setToolTip(detalle_tooltip)

        self.update_general_total()

    def update_general_total(self):
        suma_total = 0.0
        for row in range(self.tableWidgetInventario.rowCount()):
            try:
                txt = self.tableWidgetInventario.item(row, 8).text()
                valor = float(txt.replace(" $", "").replace(",", ""))
                suma_total += valor
            except: continue
        self.labelTotalGeneral.setText(f"TOTAL GENERAL: {suma_total:,.2f} $")

    def create_action_buttons(self, row_idx):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        btnSum = QPushButton("+")
        btnMinus = QPushButton("-")
        for b in [btnSum, btnMinus]:
            b.setFixedSize(25, 25)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("font-weight: bold; background-color: #eee; border: 1px solid #ccc; border-radius: 3px;")
        
        btnSum.clicked.connect(lambda: self.update_quantity(row_idx, 1))
        btnMinus.clicked.connect(lambda: self.update_quantity_minus(row_idx, 1))
        
        layout.addWidget(btnMinus)
        layout.addWidget(btnSum)
        return widget

    def update_quantity(self, row, delta):
        spin_box = self.tableWidgetInventario.cellWidget(row, 4)
        if spin_box:
            spin_box.setValue(spin_box.value() + delta)
            
    def update_quantity_minus(self, row, delta):
        spin_box = self.tableWidgetInventario.cellWidget(row, 4)
        if spin_box:
            spin_box.setValue(spin_box.value() - delta)

    def filter_products(self):
        search = self.lineEditBuscar.text().lower()
        for r in range(self.tableWidgetInventario.rowCount()):
            item = self.tableWidgetInventario.item(r, 2)
            self.tableWidgetInventario.setRowHidden(r, search not in item.text().lower())

    def getPurchaseList(self):
        purchased_items = []
        invalid_items = []
        
        for row in range(self.tableWidgetInventario.rowCount()):
            spin_box = self.tableWidgetInventario.cellWidget(row, 4)
            if spin_box and spin_box.value() > 0:
                qty = spin_box.value()
                min_req = int(self.tableWidgetInventario.item(row, 5).text())
                
                if qty < min_req:
                    name = self.tableWidgetInventario.item(row, 2).text()
                    invalid_items.append(f"- {name} (Mínimo: {min_req})")
                else:
                    purchased_items.append({
                        "id": self.tableWidgetInventario.item(row, 1).text(), 
                        "quantity": qty
                    })
        
        if invalid_items:
            QMessageBox.warning(self, "Pedido Mínimo no Alcanzado", 
                                "Los siguientes artículos no cumplen con la cantidad mínima:\n\n" + "\n".join(invalid_items))
            return None
            
        return purchased_items

    def proceedPayment(self):
        purchase_list = self.getPurchaseList()
        if purchase_list is None or not purchase_list:
            if purchase_list == []: 
                QMessageBox.warning(self, "Atención", "No hay productos en el carrito.")
            return

        confirm_msg = f"¿Está seguro de realizar la compra?\n\n{self.labelTotalGeneral.text()}"
        reply = QMessageBox.question(self, 'Confirmar Compra', confirm_msg, QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.execute_purchase_logic(purchase_list)
                QMessageBox.information(self, "Éxito", "La compra se ha procesado correctamente.")
                self.load_data() 
                self.labelTotalGeneral.setText("TOTAL GENERAL: 0.00 $")
            except Exception as e:
                QMessageBox.critical(self, "Error de Sistema", f"No se pudo completar la operación: {str(e)}")

    def tabLogic(self, tab):
        if tab == "Inventory":
            from app.views.management.inventory.InventoryView import InventoryView
            self.view = InventoryView()
        elif tab == "Provider":
            from app.views.management.providers.ProvidersView import ProvidersView
            self.view = ProvidersView()
        elif tab == "History":
            from app.views.management.history.HistoryView import HistoryView
            self.view = HistoryView()
        else:
            return
            
        self.view.showMaximized()
        self.close()

    def execute_purchase_logic(self, purchaseData):

        from app.database.auth.get import getProduct, getLastCompra, geUserName, getInventoryProduct, getInventoryProductQuantity
        from app.database.auth.update import updateProductQuantity, updateHistoryTotalPurchase, updateInventoryProductQuantity
        from app.database.auth.delete import deleteProduct
        from app.database.auth.insertNew import newInventoryProduct, newcompra, newDetailCompra
        from app import session

        try:
            total_operacion = float(self.labelTotalGeneral.text().replace("TOTAL GENERAL: ", "").replace("$", "").replace(",", "").strip())
        except:
            total_operacion = 0.0

        preUsername = geUserName(session.currentUserCedula)
        nombre_usuario = f"{preUsername[0]} {preUsername[1]}"
        newcompra(total_operacion, nombre_usuario)
        id_compra = getLastCompra()

        for row in range(self.tableWidgetInventario.rowCount()):
            spin_box = self.tableWidgetInventario.cellWidget(row, 4)
            if spin_box and spin_box.value() > 0:
                id_producto = self.tableWidgetInventario.item(row, 1).text()
                cantidad = spin_box.value()
                
                total_fila_str = self.tableWidgetInventario.item(row, 8).text()
                total_fila_final = float(total_fila_str.replace("$", "").replace(",", "").strip())
                
                p = getProduct(id_producto)
                precio_unitario = float(p[4]) 
                stock_proveedor_actual = int(p[3])

                newDetailCompra(id_compra, id_producto, cantidad, precio_unitario, total_fila_final)
                
                if getInventoryProduct(id_producto):
                    current_inv = getInventoryProductQuantity(id_producto)
                    updateInventoryProductQuantity(id_producto, current_inv[0] + cantidad)
                else:
                    newInventoryProduct(id_producto, cantidad)
            
                nuevo_stock = stock_proveedor_actual - cantidad
                updateProductQuantity(id_producto, nuevo_stock)
                if nuevo_stock <= 0:
                    deleteProduct(id_producto)
            
        updateHistoryTotalPurchase(id_compra, total_operacion)
        
        