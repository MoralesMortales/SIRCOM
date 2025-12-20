from app.windows.py.purchaseWds import Ui_Form
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from app.database.auth.get import getAllSpecificCompras, getProduct

class PurchaseView(QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Factura de Operación")
        
        self.adjust_tables()
        
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
                background-color: transparent;
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
        
        item_monto = QTableWidgetItem(total)
        item_monto.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = item_monto.font()
        font.setBold(True)
        item_monto.setFont(font)
        item_monto.setForeground(QtGui.QColor("#487c7e"))
        self.tableWidget.setItem(0, 1, item_monto)
        
        self.load_products_details(code)
        
        self.showMaximized()

    def load_products_details(self, code):
        
        raw_rows = getAllSpecificCompras(code)
        
        new_rows = []
        
        for row in raw_rows:
            code = row[0]
            print(row)
            
            print(row[1])
            
            productData = getProduct(row[1])
            
            provider = productData[2]
            productName = productData[1]
            quantity = int(row[2])
            unitaryPrice = str(row[3])
            unitaryPrice += " $"
            subTotal = str(row[4])
            subTotal += " $"
            
            new_rows.append((provider, productName, quantity, unitaryPrice, subTotal))
            
        self.tableProducto.setRowCount(len(new_rows))
        
        for row_idx, row_data in enumerate(new_rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableProducto.setItem(row_idx, col_idx, item)

    def close_window(self):
        from app.views.management.history.HistoryView import HistoryView
        self.history = HistoryView()
        self.history.showMaximized()
        self.close()