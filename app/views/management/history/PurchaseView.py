from app.windows.py.purchaseWds import Ui_Form
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from app.database.auth.get import getAllSpecificCompras, getProduct
from PyQt5 import QtWidgets

class PurchaseView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Factura de Operación")
        
        self.adjust_tables()
        self.tableWidget.setStyleSheet("padding-left: 8px; padding-right: 8px;")
        self.btnCancelar.clicked.connect(self.close_window)

    def adjust_tables(self):
        header_producto = self.tableProducto.horizontalHeader()
        header_producto.setSectionResizeMode(QHeaderView.Stretch)
        self.tableProducto.setEditTriggers(self.tableProducto.NoEditTriggers)
        
        self.tableProducto.verticalHeader().setVisible(False)
        self.tableProducto.setSelectionMode(self.tableProducto.NoSelection) # Evita el azul al hacer click

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setSelectionMode(self.tableWidget.NoSelection)

        header_total = self.tableWidget.horizontalHeader()
        header_total.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_total.setSectionResizeMode(1, QHeaderView.Stretch)

        # INSERTAR EL TEXTO FIJO AQUÍ
        label_item = QTableWidgetItem("TOTAL OPERACIÓN: ")
        label_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font = label_item.font()
        font.setBold(True)
        label_item.setFont(font)
        self.tableWidget.setItem(0, 0, label_item) 
        
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #EDEDED;
                gridline-color: transparent;
                border: none;
                font-size: 20px;
                font-weight: bold;
                color: #222;
            }
        """)

    def openWindow(self, purchaseData):
        print("mira", purchaseData)
        code, username, fecha, hora, total = purchaseData
        
        self.label_2.setText(f"{fecha} / {hora}")
        self.label.setText(f"Compra realizada por: {username}")
        
        self.labelTitulo.setText(f"Factura N° {code}")
        
        item_monto = QTableWidgetItem(total)
        item_monto.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = item_monto.font()
        font.setBold(True)
        item_monto.setFont(font)
        item_monto.setForeground(QtGui.QColor("#487c7e"))
        self.tableWidget.setItem(0, 1, item_monto)
        
        self.load_products_details(code)
        
        self.showMaximized()

    def format_rif(self, rif_raw):
        rif = str(rif_raw).upper().replace("-", "").strip()
        if len(rif) >= 9:
            return f"J-{rif[0:8]}-{rif[8:]}"
        return rif

    def load_products_details(self, code):
        raw_rows = getAllSpecificCompras(code)
        self.tableProducto.setRowCount(0)
        
        if not raw_rows:
            return

        self.tableProducto.setRowCount(len(raw_rows))
        
        for row_idx, row in enumerate(raw_rows):
            # Obtener data extra del producto
            p_data = getProduct(row[1]) 
            
            # --- 1. EXTRACCIÓN DE DATOS ---
            id_producto = str(row[1])
            # Ajusta estos índices según tu tabla de productos (comúnmente 1 y 2)
            nombre_producto = str(p_data[1]) if p_data else "N/A"
            nombre_proveedor = str(p_data[2]) if p_data else "N/A"
            
            rif_sucio = p_data[5]
            print("RIF", p_data[5])
            rif_formateado = self.format_rif(rif_sucio)
            
            cantidad = str(row[2])
            
            print("data:",p_data)
            
            # --- 2. CÁLCULOS Y FORMATEO DE MONTOS ---
            total_con_iva = float(row[4])
            precio_unitario = float(row[3])
        
            
            print("row: ", row)
            
            # Fórmulas para desglose
            monto_iva = (total_con_iva * 0.16 / 1.16)
            
            subtotal_base = (row[2]*row[3])
            
            if (row[2] >= p_data[7]):
                descuento = subtotal_base * (p_data[6]/100)
            else:
                descuento = 0
            # --- 3. ASIGNACIÓN POR COLUMNA (ORDEN UI) ---
            # Col 0: Código
            self.tableProducto.setItem(row_idx, 0, QTableWidgetItem(id_producto))
            # Col 1: Producto
            self.tableProducto.setItem(row_idx, 1, QTableWidgetItem(nombre_producto))
            # Col 2: Proveedor
            self.tableProducto.setItem(row_idx, 2, QTableWidgetItem(nombre_proveedor))
            # Col 3: RIF
            self.tableProducto.setItem(row_idx, 3, QTableWidgetItem(rif_formateado))
            # Col 4: Cantidad
            self.tableProducto.setItem(row_idx, 4, QTableWidgetItem(cantidad))
            # Col 5: Precio Unitario
            self.tableProducto.setItem(row_idx, 5, QTableWidgetItem(f"{precio_unitario:,.2f} $"))
            # Col 6: IVA (16%)
            self.tableProducto.setItem(row_idx, 6, QTableWidgetItem(f"{monto_iva:,.2f} $"))
            # Col 7: Descuento
            self.tableProducto.setItem(row_idx, 7, QTableWidgetItem(f"{descuento:,.2f} $"))
            # Col 8: Subtotal (Base)
            self.tableProducto.setItem(row_idx, 8, QTableWidgetItem(f"{subtotal_base:,.2f} $"))
            # Col 9: Total
            self.tableProducto.setItem(row_idx, 9, QTableWidgetItem(f"{total_con_iva:,.2f} $"))

            # --- 4. ALINEACIÓN ---
            for col in range(10):
                item = self.tableProducto.item(row_idx, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    def close_window(self):
        from app.views.management.history.HistoryView import HistoryView
        self.history = HistoryView()
        self.history.showMaximized()
        self.close()