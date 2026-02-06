# app/views/management/buy/BuyView.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTableWidgetItem, QHeaderView, QSpinBox, QMessageBox, QLabel, QSpacerItem, QSizePolicy, QDialog, QVBoxLayout, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from app.windows.py.buyWds import Ui_Form
from app.database.management.loadProducts import getAllProducts
from app.functions.tools.getIcon import getIcon
from app.database.auth.get import getProduct, getLastCompra, geUserName, getInventoryProduct, getInventoryProductQuantity, getProviderData
from app.database.auth.update import updateProductQuantity, updateHistoryTotalPurchase, updateInventoryProductQuantity
from app.database.auth.delete import deleteProduct
from app.database.auth.insertNew import newInventoryProduct, newcompra, newDetailCompra
from app import session
from app.database.connect import connectDB
import requests 
import json
from datetime import datetime, timedelta

class DescriptionDialog(QDialog):
    def __init__(self, description, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Descripción del Producto")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout()
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(description)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class BuyView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Orden de Compra")
        # Inicializar como diccionario vacío
        self.pending_orders = {}
        self.tasa_bcv = 0.0
        self.iva = 0.0
        # Cargar tasa BCV al iniciar
        self.load_bcv_rate()
        
        self.setup_total_labels() 
        
        self.tableWidgetInventario.verticalHeader().setDefaultSectionSize(40)
        
        self.menuItemInventario.mousePressEvent = lambda event: self.tabLogic("Inventory")
        self.menuItemProveedores.mousePressEvent = lambda event: self.tabLogic("Provider")
        self.menuItemHistorial.mousePressEvent = lambda event: self.tabLogic("History")
        
        # Conectar la búsqueda y el evento Enter
        self.lineEditBuscar.textChanged.connect(self.filter_products)
        self.lineEditBuscar.returnPressed.connect(self.handle_search_enter)
        
        self.menuItemRecursos.setStyleSheet("#menu QWidget { background: #7f5b5f; }")
        for item in [self.menuItemHistorial, self.menuItemInventario, self.menuItemProveedores, self.menuItemRecursos]:
            item.setCursor(Qt.PointingHandCursor)
        
        self.btnComprar.clicked.connect(self.proceedPayment)
        
        self.adjust_table_settings()
        self.load_data()
        
        # Conectar doble click en la columna de descripción
        self.tableWidgetInventario.cellDoubleClicked.connect(self.handle_cell_double_click)

    def setup_total_labels(self):
        """Configura todos los labels de totales en disposición vertical"""
        # Layout vertical principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)  # Reducir espacio entre elementos
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Total General en Bolívares
        self.labelTotalGeneral = QLabel("TOTAL GENERAL (Bs): 0.00 Bs")
        self.labelTotalGeneral.setObjectName("labelTotalGeneral")
        self.labelTotalGeneral.setStyleSheet("""
            QLabel#labelTotalGeneral {
                font-weight: bold; 
                color: #000; 
                font-size: 18px;
                padding: 2px 5px;
            }
        """)
        main_layout.addWidget(self.labelTotalGeneral)
        
        # 3. Total General en Dólares
        self.labelTotalDolares = QLabel("TOTAL GENERAL (USD): 0.00 $")
        self.labelTotalDolares.setObjectName("labelTotalDolares")
        self.labelTotalDolares.setStyleSheet("""
            QLabel#labelTotalDolares {
                font-weight: bold; 
                color: #000; 
                font-size: 18px;
                padding: 2px 5px;
            }
        """)
        main_layout.addWidget(self.labelTotalDolares)
        
        # 2. Tasa BCV
        self.labelTasaBCV = QLabel(f"TASA BCV: {self.tasa_bcv:,.2f} Bs/$")
        self.labelTasaBCV.setObjectName("labelTasaBCV")
        self.labelTasaBCV.setStyleSheet("""
            QLabel#labelTasaBCV {
                font-weight: bold; 
                color: #000; 
                font-size: 18px;
                padding: 2px 5px;
            }
        """)
        self.labelTasaBCV.setToolTip("Tasa del Banco Central de Venezuela")
        main_layout.addWidget(self.labelTasaBCV)
        
        # Crear un widget contenedor para el layout
        container = QWidget()
        container.setLayout(main_layout)
        
        # Insertar el widget en el layout horizontal_9
        self.horizontalLayout_9.insertWidget(0, container)
        
    def adjust_table_settings(self):
        """Configura las columnas y el comportamiento de redimensionamiento"""
        self.tableWidgetInventario.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        headers = [
            "RIF", "Proveedor", "Código", "Producto", 
            "Descripción", "Cantidad", "Precio Unit.", "IVA", "Total + IVA", "Estado", "Acciones"
        ]
        
        self.tableWidgetInventario.setColumnCount(len(headers))
        self.tableWidgetInventario.setHorizontalHeaderLabels(headers)
        
        header = self.tableWidgetInventario.horizontalHeader()
        header.setStretchLastSection(False) 
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_bcv_rate(self):
        """Carga la tasa BCV desde la API o usa una caché"""
        try:
            # Intentar obtener la tasa desde la API
            response = requests.get('https://ve.dolarapi.com/v1/dolares/oficial/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.tasa_bcv = float(data.get('promedio', 0.0))
                print(f"Tasa BCV cargada desde API: {self.tasa_bcv}")
            else:
                # Si falla la API, usar un valor por defecto
                self.tasa_bcv = 0  # Valor por defecto aproximado
                print(f"API no disponible. Usando tasa BCV por defecto: {self.tasa_bcv}")
        except Exception as e:
            print(f"Error cargando tasa BCV: {e}")
            # Valor por defecto si falla todo
            self.tasa_bcv = 0
            
    def load_data(self):
        """Carga productos disponibles y pedidos pendientes"""
        try:
            # Primero cargar pedidos pendientes (fase 2)
            self.load_pending_orders()
            
            # Verificar que pending_orders sea un diccionario
            if not isinstance(self.pending_orders, dict):
                print(f"ADVERTENCIA: pending_orders no es un diccionario, es: {type(self.pending_orders)}")
                self.pending_orders = {}
            
            # Luego cargar productos disponibles
            rows = getAllProducts() 
            
            # Calcular cuántas filas agregar (pendientes + disponibles)
            total_pending_rows = 0
            for order_id, order_data in self.pending_orders.items():
                total_pending_rows += len(order_data.get('details', []))
            
            total_rows = total_pending_rows + len(rows)
            self.tableWidgetInventario.setRowCount(total_rows)
            
            current_row = 0
            
            # 1. Mostrar primero los pedidos pendientes (fase 2)
            for order_id, order_data in self.pending_orders.items():
                rows_added = self.display_pending_order(current_row, order_id, order_data)
                current_row += rows_added
            
            # 2. Mostrar productos disponibles (fase 1)
            for row_idx, row in enumerate(rows):
                actual_row = current_row + row_idx
                try:
                    # row contiene: [codigo, nombreProducto, descripcion, stock, rif, nombreEmpresa, precioUnitario, descuento, descuentoDesde, stockMinimo]
                    
                    # 0: RIF del proveedor (formateado)
                    rif = row[4] if len(row) > 4 else ""
                    rif_formateado = self.format_rif(rif)
                    self.set_table_item(actual_row, 0, rif_formateado)
                    
                    # 1: Nombre del proveedor
                    nombre_proveedor = row[5] if len(row) > 5 else ""
                    self.set_table_item(actual_row, 1, nombre_proveedor)
                    
                    # 2: Código del producto
                    codigo_producto = row[0] if len(row) > 0 else ""
                    self.set_table_item(actual_row, 2, str(codigo_producto))
                    
                    # 3: Nombre del producto
                    nombre_producto = row[1] if len(row) > 1 else ""
                    self.set_table_item(actual_row, 3, nombre_producto)
                    
                    # 4: Descripción
                    descripcion = row[2] if len(row) > 2 else ""
                    self.set_table_item(actual_row, 4, descripcion)
                    
                    # 5: Cantidad (SpinBox)
                    stock_disponible = int(row[3]) if len(row) > 3 and row[3] else 0
                    spin_qty = QSpinBox()
                    spin_qty.setRange(0, stock_disponible)
                    spin_qty.setAlignment(Qt.AlignCenter)
                    spin_qty.setButtonSymbols(QSpinBox.NoButtons)
                    spin_qty.valueChanged.connect(lambda _, r=actual_row: self.calculate_row_total(r))
                    
                    # Estilo inicial para cantidad mínima
                    stock_minimo = int(row[9]) if len(row) > 9 and row[9] else 0
                    self.tableWidgetInventario.setCellWidget(actual_row, 5, spin_qty)
                    
                    # 6: Precio Unitario
                    precio = float(row[6]) if len(row) > 6 and row[6] else 0.0
                    self.set_table_item(actual_row, 6, f"{precio:,.2f} Bs")
                    
                    # 7: IVA (16%)
                    iva = self.iva
                    self.set_table_item(actual_row, 7, f"{iva:,.2f} Bs")
                    
                    # 8: Total + IVA (se calculará dinámicamente)
                    item_total = QTableWidgetItem("0.00 Bs")
                    item_total.setTextAlignment(Qt.AlignCenter)
                    item_total.setToolTip("Total.")
                    self.tableWidgetInventario.setItem(actual_row, 8, item_total)
                    
                    # 9: Estado - ComboBox con opciones
                    combo_estado = QComboBox()
                    combo_estado.addItems(["Pendiente", "En Curso", "Recibido"])
                    combo_estado.setCurrentIndex(0)  # Por defecto Disponible
                    combo_estado.setEnabled(False)  # Deshabilitado para productos disponibles
                    combo_estado.currentTextChanged.connect(lambda text, r=actual_row: self.handle_status_change(r, text))
                    self.tableWidgetInventario.setCellWidget(actual_row, 9, combo_estado)
                    

                    # 10: Acciones
                    self.tableWidgetInventario.setCellWidget(actual_row, 10, self.create_action_buttons(actual_row))
                    
                except Exception as e:
                    print(f"Error cargando fila {actual_row}: {e}")
                    import traceback
                    traceback.print_exc()
                    
        except Exception as e:
            print(f"Error general cargando datos: {e}")
            import traceback
            traceback.print_exc()

    def load_pending_orders(self):
        """Carga pedidos pendientes de la base de datos"""
        try:
            # Asegurar que pending_orders sea un diccionario
            if not isinstance(self.pending_orders, dict):
                self.pending_orders = {}
            
            # Limpiar diccionario actual
            self.pending_orders.clear()
            
            # Obtener compras pendientes
            pending_purchases = self.getPendingPurchases()
            
            for purchase in pending_purchases:
                purchase_id = purchase[0]
                # Obtener detalles de la compra
                details = self.getPurchaseDetails(purchase_id)
                
                self.pending_orders[purchase_id] = {
                    'id': purchase_id,
                    'total': purchase[1] if len(purchase) > 1 else 0.0,
                    'fecha': purchase[2] if len(purchase) > 2 else '',
                    'usuario': purchase[3] if len(purchase) > 3 else '',
                    'details': details if details else []
                }
                
        except Exception as e:
            print(f"Error cargando pedidos pendientes: {e}")
            # Asegurar que sea diccionario incluso en caso de error
            self.pending_orders = {}

    def getPendingPurchases(self):
        """Obtiene todas las compras con estado 'En Curso'"""
        connection = connectDB()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    SELECT idCompra, totalCompra, fechaCompra, nombreUsuario
                    FROM compra 
                    WHERE estado = 'En Curso'
                    ORDER BY fechaCompra DESC
                    """
                )
                purchases = cursor.fetchall()
                return purchases
            except Exception as e:
                print(f"Error getting pending purchases: {e}")
                return []
            finally:
                connection.close()
        return []

    def getPurchaseDetails(self, purchase_id):
        """Obtiene los detalles de una compra específica"""
        connection = connectDB()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    SELECT 
                        dc.codigoProducto,
                        p.nombre as nombre_producto,
                        p.descripcion,
                        dc.cantidad,
                        dc.precioUnitario,
                        dc.subTotal,
                        pr.rif,
                        pr.nombreEmpresa
                    FROM detalleCompra dc
                    JOIN producto p ON dc.codigoProducto = p.codigo
                    JOIN proveedor pr ON p.rifProveedor = pr.rif
                    WHERE dc.idCompra = ?
                    """
                    , (purchase_id,)
                )
                details = cursor.fetchall()
                
                # Convertir a lista de diccionarios
                result = []
                for detail in details:
                    result.append({
                        'codigo_producto': detail[0],
                        'nombre_producto': detail[1],
                        'descripcion': detail[2],
                        'cantidad': detail[3],
                        'precio_unitario': float(detail[4]),
                        'total': float(detail[5]),
                        'rif': detail[6],
                        'proveedor': detail[7]
                    })
                return result
            except Exception as e:
                print(f"Error getting purchase details: {e}")
                return []
            finally:
                connection.close()
        return []

    def display_pending_order(self, start_row, order_id, order_data):
        """Muestra un pedido pendiente en la tabla y retorna cuántas filas agregó"""
        try:
            details = order_data.get('details', [])
            rows_added = 0
            
            # Para cada detalle del pedido, crear una fila
            for detail in details:
                current_row = start_row + rows_added
                
                # 0: RIF
                rif = detail.get('rif', '')
                rif_formateado = self.format_rif(rif)
                self.set_table_item(current_row, 0, rif_formateado)
                
                # 1: Proveedor
                proveedor = detail.get('proveedor', '')
                self.set_table_item(current_row, 1, proveedor)
                
                # 2: Código del producto
                codigo = detail.get('codigo_producto', '')
                self.set_table_item(current_row, 2, str(codigo))
                
                # 3: Producto
                producto = detail.get('nombre_producto', '')
                self.set_table_item(current_row, 3, producto)
                
                # 4: Descripción
                descripcion = detail.get('descripcion', '')
                self.set_table_item(current_row, 4, descripcion)
                
                # 5: Cantidad (label en lugar de spinbox)
                cantidad = detail.get('cantidad', 0)
                cantidad_label = QLabel(str(cantidad))
                cantidad_label.setAlignment(Qt.AlignCenter)
                cantidad_label.setStyleSheet("font-weight: bold; color: #000;")
                self.tableWidgetInventario.setCellWidget(current_row, 5, cantidad_label)
                
                # 6: Precio Unitario
                precio = detail.get('precio_unitario', 0.0)
                
                self.set_table_item(current_row, 6, f"{precio:,.2f} Bs")
                
                # 7: IVA
                iva = precio * 0.16
                self.set_table_item(current_row, 7, f"{iva:,.2f} Bs")
                
                # 8: Total + IVA
                total = detail.get('total', 0.0)
                self.set_table_item(current_row, 8, f"{total:,.2f} Bs")
                
                # 9: Estado - ComboBox habilitado
                combo_estado = QComboBox()
                combo_estado.addItems(["En Curso", "Recibido"])
                combo_estado.setCurrentIndex(0)  # Por defecto "En Curso"
                combo_estado.currentTextChanged.connect(lambda text, r=current_row, oid=order_id, pid=codigo: 
                                                       self.handle_pending_order_status(r, text, oid, pid))
                self.tableWidgetInventario.setCellWidget(current_row, 9, combo_estado)
                
                # Estilo especial para filas de pedidos pendientes
                for col in range(self.tableWidgetInventario.columnCount()):
                    item = self.tableWidgetInventario.item(current_row, col)
                    if item:
                        item.setBackground(QtGui.QColor(255, 255, 204))  # Fondo amarillo claro
                
                # 10: Acciones (solo botón para cancelar pedido)
                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(5, 2, 5, 2)
                
                btnCancelar = QPushButton("✕")
                btnCancelar.setFixedSize(25, 25)
                btnCancelar.setCursor(Qt.PointingHandCursor)
                btnCancelar.setStyleSheet("background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; border-radius: 3px;")
                btnCancelar.setToolTip("Cancelar pedido")
                btnCancelar.clicked.connect(lambda _, oid=order_id: self.cancel_pending_order(oid))
                
                layout.addWidget(btnCancelar)
                layout.setAlignment(Qt.AlignCenter)
                self.tableWidgetInventario.setCellWidget(current_row, 10, widget)
                
                rows_added += 1
                
            return rows_added
                
        except Exception as e:
            print(f"Error mostrando pedido pendiente: {e}")
            return 0

    def format_rif(self, rif):
        """Formatea el RIF según su tipo (G-, V-, J-)"""
        if not rif:
            return ""
        
        # Convertir a string y limpiar
        value_str = str(rif).strip()
        
        # Si ya tiene formato (comienza con G-, V-, J-)
        if len(value_str) > 1 and value_str[0] in ['G', 'V', 'J'] and value_str[1] == '-':
            return value_str
        
        # Si comienza con letra pero no tiene guión
        if len(value_str) > 0 and value_str[0] in ['G', 'V', 'J']:
            if '-' not in value_str:
                # Añadir guión después de la letra
                return f"{value_str[0]}-{value_str[1:]}"
            return value_str
        
        # Si es solo número, determinar tipo basado en longitud
        # Eliminar cualquier guión o espacio
        rif_limpio = value_str.replace("-", "").replace(" ", "")
        
        if not rif_limpio.isdigit():
            return value_str  # No es numérico, devolver como está
        
        # Formatear según tipo
        if len(rif_limpio) == 9:  # RIF Jurídico: J-XXXXXXXX-X
            return f"J-{rif_limpio[:8]}-{rif_limpio[8:]}"
        elif len(rif_limpio) == 8:  # RIF Personal/Gubernamental
            # Determinar tipo basado en el primer dígito
            primer_digito = rif_limpio[0]
            if primer_digito in ['1', '2', '3', '4']:  # Personas naturales
                return f"V-{rif_limpio}"
            elif primer_digito in ['8', '9']:  # Personas jurídicas (menos común)
                return f"J-{rif_limpio}"
            elif primer_digito in ['5', '6', '7']:  # Gobierno
                return f"G-{rif_limpio}"
            else:
                return f"J-{rif_limpio}"
        else:
            # Para longitudes diferentes, formatear simple
            return f"J-{rif_limpio}"
    
    def set_table_item(self, row, col, value):
        text_value = str(value)
        item = QTableWidgetItem(text_value)
        item.setTextAlignment(Qt.AlignCenter)
        item.setToolTip(text_value) 
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidgetInventario.setItem(row, col, item)

    def calculate_row_total(self, row):
        """Calcula el subtotal con descuentos e IVA"""
        # Verificar si es una fila de pedido pendiente (no tiene spinbox)
        cell_widget = self.tableWidgetInventario.cellWidget(row, 5)
        if not isinstance(cell_widget, QSpinBox):
            return
            
        spin_box = cell_widget
        qty = spin_box.value() if spin_box else 0
        
        try:
            # Precio unitario está en columna 6
            price_item = self.tableWidgetInventario.item(row, 6)
            if price_item:
                price_text = price_item.text()
                price = float(price_text.replace(" Bs", "").replace(",", ""))
            else:
                price = 0.0
        except: 
            price = 0.0
        
        # Obtener información del estado (combo box)
        combo_estado = self.tableWidgetInventario.cellWidget(row, 9)
        estado_tooltip = combo_estado.toolTip() if combo_estado else ""
        
        # Extraer información del tooltip
        stock_minimo = 0
        descuento = 0
        desde_unidades = 0
        
        # Buscar stock mínimo en el tooltip
        if "Stock mínimo:" in estado_tooltip:
            import re
            match = re.search(r'Stock mínimo:\s*(\d+)', estado_tooltip)
            if match:
                stock_minimo = int(match.group(1))
        
        # Buscar descuento en el tooltip
        if "Descuento del" in estado_tooltip:
            import re
            match = re.search(r'Descuento del\s*(\d+)%\s*aplicable al comprar\s*(\d+)', estado_tooltip)
            if match:
                descuento = float(match.group(1))
                desde_unidades = int(match.group(2))
        
        # Calcular subtotal base
        subtotal_base = price * qty
        
        # Aplicar descuento si aplica
        descuento_aplicado = 0.0
        if qty >= desde_unidades and descuento > 0:
            descuento_aplicado = subtotal_base * (descuento / 100)
        
        subtotal_neto = subtotal_base - descuento_aplicado
        
        # Calcular IVA (16%)
        iva = subtotal_neto * 0.16
        self.iva = iva
        total_con_iva = subtotal_neto + iva
        
        
        item_iva = self.tableWidgetInventario.item(row, 7)
        if item_iva:
            item_iva.setText(f"{iva:,.2f} Bs")
        
        # Actualizar columna 8 (Total + IVA)
        item_total = self.tableWidgetInventario.item(row, 8)
        if item_total:
            item_total.setText(f"{total_con_iva:,.2f} Bs")
            
            # Actualizar tooltip con desglose
            detalle_tooltip = (
                f"<b>Desglose de Pago:</b><br>"
                f"Precio unitario: {price:,.2f} Bs<br>"
                f"Cantidad: {qty} unidades<br>"
                f"Subtotal base: {subtotal_base:,.2f} Bs<br>"
            )
            
            if descuento_aplicado > 0:
                detalle_tooltip += f"Descuento ({descuento}%): -{descuento_aplicado:,.2f} Bs<br>"
                detalle_tooltip += f"Subtotal neto: {subtotal_neto:,.2f} Bs<br>"
            
            detalle_tooltip += (
                f"IVA (16%): {iva:,.2f} Bs<br>"
                f"<hr><b>Total Fila: {total_con_iva:,.2f} Bs</b>"
            )
            
            item_total.setToolTip(detalle_tooltip)
        
        # Actualizar color del spin box según cantidad mínima
        if 0 < qty < stock_minimo and stock_minimo > 0:
            spin_box.setStyleSheet("background-color: #fff3cd; border: 1px solid #ffc107;")
        else:
            spin_box.setStyleSheet("")
        
        self.update_general_total()


    def update_general_total(self):
        suma_total = 0.0
        for row in range(self.tableWidgetInventario.rowCount()):
            try:
                # Solo sumar productos en fase 1 (con spinbox)
                cell_widget = self.tableWidgetInventario.cellWidget(row, 5)
                if isinstance(cell_widget, QSpinBox) and cell_widget.value() > 0:
                    item = self.tableWidgetInventario.item(row, 8)
                    if item:
                        txt = item.text()
                        valor = float(txt.replace(" Bs", "").replace(",", ""))
                        suma_total += valor
            except Exception as e:
                print(f"Error calculando total fila {row}: {e}")
                continue
        
        # Actualizar total en Bolívares
        self.labelTotalGeneral.setText(f"TOTAL GENERAL (Bs): {suma_total:,.2f} Bs")
        
        # Calcular total en Dólares
        if self.tasa_bcv > 0:
            total_dolares = suma_total / self.tasa_bcv
            self.labelTotalDolares.setText(f"TOTAL GENERAL (USD): {total_dolares:,.2f} $")
        else:
            self.labelTotalDolares.setText("TOTAL GENERAL (USD): 0.00 $")
        
        # Actualizar tooltip con desglose
        tooltip_text = f"<b>Desglose:</b><br>"
        tooltip_text += f"Total en Bolívares: {suma_total:,.2f} Bs<br>"
        if self.tasa_bcv > 0:
            total_dolares = suma_total / self.tasa_bcv
            tooltip_text += f"Tasa BCV: {self.tasa_bcv:,.2f} Bs/$<br>"
            tooltip_text += f"Total en Dólares: {total_dolares:,.2f} $"
        
        self.labelTotalGeneral.setToolTip(tooltip_text)
    
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
        btnMinus.clicked.connect(lambda: self.update_quantity(row_idx, -1))
        
        layout.addWidget(btnMinus)
        layout.addWidget(btnSum)
        return widget

    def update_quantity(self, row, delta):
        spin_box = self.tableWidgetInventario.cellWidget(row, 5)
        if spin_box and isinstance(spin_box, QSpinBox):
            new_value = spin_box.value() + delta
            if new_value >= 0 and new_value <= spin_box.maximum():
                spin_box.setValue(new_value)

    def filter_products(self):
        search = self.lineEditBuscar.text().lower()
        for r in range(self.tableWidgetInventario.rowCount()):
            visible = False
            # Buscar en RIF (col 0), Proveedor (col 1), Código (col 2), Producto (col 3)
            for col in [0, 1, 2, 3]:
                item = self.tableWidgetInventario.item(r, col)
                if item and search in item.text().lower():
                    visible = True
                    break
            self.tableWidgetInventario.setRowHidden(r, not visible)

    def handle_search_enter(self):
        """Maneja cuando se presiona Enter en el buscador"""
        search_text = self.lineEditBuscar.text().strip()
        if not search_text:
            return
        
        # Verificar si el texto parece un RIF
        if any(search_text.upper().startswith(prefix) for prefix in ['G-', 'V-', 'J-', 'G', 'V', 'J']):
            try:
                # Intentar obtener el proveedor por RIF
                print(f"Buscando proveedor con RIF: {search_text}")
                if(search_text[0] == 'J'):
                    search_text = search_text.replace("J-", "").replace("-", "")
                    print(f"Buscando proveedor cone RIF: {search_text}")
                
                else:
                    search_text2 = ''
                    search_text2 += search_text.replace("-", "")
                    search_text = search_text2
                    print(f"Buscando proveedor cone RIF: {search_text}")
                    

                provider = getProviderData(search_text)
                print(provider)
                if provider:
                    # Abrir ventana de editar proveedor
                    self.open_edit_provider(search_text)
                else:
                    QMessageBox.warning(self, "Proveedor no encontrado", 
                                       f"No se encontró un proveedor con RIF: {search_text}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo buscar el proveedor: {str(e)}")

    def open_edit_provider(self, provider_data):
        """Abre la ventana de editar proveedor"""
        try:
            from app.views.management.providers.EditProviderView import EditProviderView
            print('bf print')
            self.edit_view = EditProviderView()
            self.edit_view.openWindow(provider_data)  # provider_data[0] es el RIF
            self.edit_view.showMaximized()
            print('af print')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la ventana de edición: {str(e)}")

    def handle_cell_double_click(self, row, column):
        """Maneja el doble clic en celdas"""
        if column == 4:  # Columna de descripción
            item = self.tableWidgetInventario.item(row, column)
            if item:
                description = item.text()
                dialog = DescriptionDialog(description, self)
                dialog.exec_()

    def handle_status_change(self, row, status):
        """Maneja el cambio de estado en el ComboBox para productos disponibles"""
        # Solo para productos en fase 1 (disponibles)
        combo_box = self.tableWidgetInventario.cellWidget(row, 9)
        if combo_box and combo_box.currentText() != "Pendiente":
            combo_box.setCurrentText("Pendiente")  # Forzar a permanecer en "Disponible"

    def handle_pending_order_status(self, row, status, order_id, product_id):
        """Maneja el cambio de estado para pedidos pendientes"""
        if status == "Recibido":
            reply = QMessageBox.question(self, "Confirmar Recepción",
                                        f"¿Confirmar recepción completa del pedido #{order_id}?\n\n"
                                        f"Esto añadirá los productos al inventario y completará la compra.",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.complete_pending_order(order_id, product_id, row)
            else:
                print("cambio")
                combo_box = self.tableWidgetInventario.cellWidget(row, 9)
                combo_box.blockSignals(True)
                combo_box.setCurrentText("En Curso")
                combo_box.blockSignals(False)
        
        elif status == "En Curso":

            # IMPORTANTE: Restablecer el ComboBox a "En Curso" si el usuario dice No
    
            self.updatePurchaseStatus(order_id, "En Curso")

    def updatePurchaseStatus(self, order_id, status):
        """Actualiza el estado de una compra en la base de datos"""
        connection = connectDB()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE compra SET estado = ? WHERE idCompra = ?",
                    (status, order_id)
                )
                connection.commit()
                return True
            except Exception as e:
                print(f"Error updating purchase status: {e}")
                return False
            finally:
                connection.close()
        return False

    def complete_pending_order(self, order_id, product_id, row):
        """Completa un pedido pendiente y lo añade al inventario"""
        try:
            # Obtener la cantidad del pedido
            cantidad_label = self.tableWidgetInventario.cellWidget(row, 5)
            cantidad_text = cantidad_label.text() if cantidad_label else "0"
            
            # Convertir a float primero y luego a int (para manejar decimales)
            try:
                cantidad = int(float(cantidad_text))
            except ValueError:
                cantidad = int(cantidad_text) if cantidad_text.isdigit() else 0
            
            if cantidad <= 0:
                QMessageBox.warning(self, "Cantidad inválida", "La cantidad debe ser mayor que 0.")
                return
            
            # Obtener el total de la compra
            connection = connectDB()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT totalCompra FROM compra WHERE idCompra = ?",
                (order_id,)
            )
            total_compra_result = cursor.fetchone()
            
            if total_compra_result:
                total_compra = total_compra_result[0]
            else:
                total_compra = 0.0
            
            # Añadir al inventario
            inventory_product = getInventoryProduct(product_id)
            if inventory_product:
                current_inv = getInventoryProductQuantity(product_id)
                if current_inv and current_inv[0] is not None:
                    current_qty = int(current_inv[0]) if isinstance(current_inv[0], (int, float, str)) else 0
                    updateInventoryProductQuantity(product_id, current_qty + cantidad)
                else:
                    newInventoryProduct(product_id, cantidad)
            else:
                newInventoryProduct(product_id, cantidad)
            
            # Actualizar estado de la compra en la base de datos a "Recibido"
            self.updatePurchaseStatus(order_id, "Recibido")
            
            # ¡AHORA SÍ guardar en el historial!
            updateHistoryTotalPurchase(order_id, total_compra)
            
            # Actualizar la fila en la tabla
            combo_box = self.tableWidgetInventario.cellWidget(row, 9)
            if combo_box:
                combo_box.setEnabled(False)
                combo_box.setStyleSheet("background-color: #d4edda; color: #155724;")
            
            # Cambiar color de fondo de toda la fila
            for col in range(self.tableWidgetInventario.columnCount()):
                item = self.tableWidgetInventario.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor(209, 231, 221))  # Verde claro
            
            # También cambiar el texto del estado
            estado_item = QTableWidgetItem("Recibido")
            estado_item.setTextAlignment(Qt.AlignCenter)
            estado_item.setBackground(QtGui.QColor(209, 231, 221))
            self.tableWidgetInventario.removeCellWidget(row, 9)
            self.tableWidgetInventario.setItem(row, 9, estado_item)
            
            connection.close()
            
            QMessageBox.information(self, "Compra Completada", 
                                f"Pedido #{order_id} completado.\n"
                                f"Total registrado: {total_compra:,.2f} Bs")
            
            # Recargar los datos para actualizar la vista
            QtCore.QTimer.singleShot(1000, self.load_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo completar el pedido: {str(e)}")
            import traceback
            traceback.print_exc()
    def cancel_pending_order(self, order_id):
        """Cancela un pedido pendiente y RESTAURA el stock del proveedor"""
        reply = QMessageBox.question(self, "Cancelar Pedido",
                                    f"¿Está seguro de cancelar el pedido #{order_id}?\n\n"
                                    f"Esta acción restaurará el stock del proveedor y eliminará el pedido.",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                connection = connectDB()
                if connection:
                    cursor = connection.cursor()
                    
                    # 1. PRIMERO: Obtener todos los productos y cantidades de este pedido
                    cursor.execute(
                        """
                        SELECT dc.codigoProducto, dc.cantidad, p.stock
                        FROM detalleCompra dc
                        JOIN producto p ON dc.codigoProducto = p.codigo
                        WHERE dc.idCompra = ?
                        """,
                        (order_id,)
                    )
                    
                    productos = cursor.fetchall()
                    
                    # 2. SEGUNDO: Restaurar el stock del proveedor para cada producto
                    for producto in productos:
                        codigo_producto = producto[0]
                        cantidad = int(producto[1])
                        stock_actual = int(producto[2])
                        
                        # Restaurar el stock (sumar la cantidad que fue reservada)
                        nuevo_stock = stock_actual + cantidad
                        
                        cursor.execute(
                            "UPDATE producto SET stock = ? WHERE codigo = ?",
                            (nuevo_stock, codigo_producto)
                        )
                    
                    # 3. TERCERO: Eliminar detalles de compra
                    cursor.execute("DELETE FROM detalleCompra WHERE idCompra = ?", (order_id,))
                    
                    # 4. CUARTO: Eliminar la compra
                    cursor.execute("DELETE FROM compra WHERE idCompra = ?", (order_id,))
                    
                    connection.commit()
                    connection.close()
                    
                    # Recargar datos
                    self.load_data()
                    QMessageBox.information(self, "Pedido Cancelado", 
                                        f"Pedido #{order_id} cancelado correctamente.\n"
                                        f"Stock del proveedor restaurado.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cancelar el pedido: {str(e)}")
                import traceback
                traceback.print_exc()
    def proceedPayment(self):
        """FASE 1: Procesa la SOLICITUD DE COMPRA"""
        # Primero verificar si hay productos seleccionados
        selected_items = []
        selected_codes = set()  # Para detectar duplicados
        
        for row in range(self.tableWidgetInventario.rowCount()):
            spin_box = self.tableWidgetInventario.cellWidget(row, 5)
            if isinstance(spin_box, QSpinBox) and spin_box.value() > 0:
                codigo_item = self.tableWidgetInventario.item(row, 2)
                if codigo_item:
                    codigo = codigo_item.text()
                    if codigo in selected_codes:
                        QMessageBox.warning(self, "Producto duplicado", 
                                        f"El producto {codigo} ya está seleccionado.")
                        return
                    selected_codes.add(codigo)
                    selected_items.append(row)

        if not selected_items:
            QMessageBox.warning(self, "Atención", "No hay productos en el carrito.")
            return

        confirm_msg = f"¿Confirmar solicitud de compra?\n\n{self.labelTotalGeneral.text()}\n\n"
        confirm_msg += f"Total de productos: {len(selected_items)}\n"
        
        reply = QMessageBox.question(self, 'Confirmar Solicitud de Compra', confirm_msg, 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # Crear la compra principal (estado inicial: "En Curso")
                total_text = self.labelTotalGeneral.text()
                total_text = total_text.replace("TOTAL GENERAL (Bs): ", "").replace("Bs", "").replace(",", "").strip()
                total_operacion = float(total_text)
                
                preUsername = geUserName(session.currentUserCedula)
                nombre_usuario = f"{preUsername[0]} {preUsername[1]}"
                
                # Crear nueva compra con estado "En Curso"
                connection = connectDB()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        """
                        INSERT INTO compra (totalCompra, nombreUsuario, fechaCompra, estado)
                        VALUES (?, ?, datetime('now'), ?)
                        """,
                        (total_operacion, nombre_usuario, "En Curso")
                    )
                    connection.commit()
                    connection.close()
                
                id_compra = getLastCompra()
                
                # Procesar cada producto seleccionado
                for row in selected_items:
                    item_codigo = self.tableWidgetInventario.item(row, 2)
                    if not item_codigo:
                        continue
                    
                    id_producto = item_codigo.text()
                    spin_box = self.tableWidgetInventario.cellWidget(row, 5)
                    cantidad = spin_box.value()
                    
                    item_total = self.tableWidgetInventario.item(row, 8)
                    if not item_total:
                        continue
                    
                    total_fila_str = item_total.text()
                    total_fila_final = float(total_fila_str.replace("Bs", "").replace(",", "").strip())
                    
                    p = getProduct(id_producto)
                    if p and len(p) > 4:
                        precio_unitario = float(p[4])
                        tasaBCV=self.tasa_bcv
                        
                        # Crear detalle de compra
                        newDetailCompra(id_compra, id_producto, cantidad, precio_unitario, total_fila_final, tasaBCV)
                        
                        # Actualizar stock del proveedor (reservar)
                        if len(p) > 3:
                            stock_proveedor_actual = int(p[3])
                            nuevo_stock = stock_proveedor_actual - cantidad
                            updateProductQuantity(id_producto, nuevo_stock)
                            
                            if nuevo_stock <= 0:
                                deleteProduct(id_producto)
                
                # ¡IMPORTANTE! NO guardar en historial todavía
                # updateHistoryTotalPurchase(id_compra, total_operacion)  # <-- COMENTAR O ELIMINAR
                
                QMessageBox.information(self, "Solicitud Creada", 
                                    f"Solicitud de compra #{id_compra} creada correctamente.\n"
                                    f"Estado: En Curso\n\n"
                                    f"Los productos ahora aparecerán en la sección superior "
                                    f"como pedidos pendientes.")
                
                # Recargar datos para mostrar el nuevo pedido pendiente
                self.load_data()
                self.labelTotalGeneral.setText("TOTAL GENERAL (Bs): 0.00 Bs")
                
            except Exception as e:
                QMessageBox.critical(self, "Error de Sistema", 
                                f"No se pudo completar la solicitud: {str(e)}")
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