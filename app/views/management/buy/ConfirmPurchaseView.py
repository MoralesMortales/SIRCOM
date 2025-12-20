from app.windows.py.confirmPurchaseWds import Ui_Form
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from app.database.auth.get import getProduct, getLastCompra, geUserName, getInventoryProduct, getInventoryProductQuantity
from app.database.auth.update import updateProductQuantity, updateHistoryTotalPurchase, updateInventoryProductQuantity
from app.database.auth.delete import deleteProduct
from app.database.auth.insertNew import newInventoryProduct, newcompra, newDetailCompra


class ConfirmPurchaseView(QWidget, Ui_Form):
    
    def __init__(self, purchaseData=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Confirmar Compra")
        
        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.purchaseConfirmed)
        self.purchaseData = purchaseData
        
        
        self.format_tables()
        
        if purchaseData:
            self.load_data(purchaseData)

    def format_tables(self):
            header = self.tableProducto.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            self.tableProducto.setEditTriggers(self.tableProducto.NoEditTriggers)
            
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(1)
            
            self.tableWidget.horizontalHeader().setVisible(False)
            self.tableWidget.verticalHeader().setVisible(False)
            
            self.tableWidget.setShowGrid(False)
            self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
            
            self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            self.tableWidget.setStyleSheet("""
                QTableWidget {
                    background-color: transparent;
                    border: none;
                    font-size: 20px;
                    color: #222;
                }
            """)
            
    def load_data(self, purchaseData):
        self.tableProducto.setRowCount(0)
        purchaseTotal = 0.0
        
        for data in purchaseData:
            print(data)
            productBase = getProduct(data.get('id', 'N/A'))
            print(productBase[0])
            productBase += (data.get('quantity', 0),)
            print(productBase)
            row_idx = self.tableProducto.rowCount()
            self.tableProducto.insertRow(row_idx)
            
            product = productBase[1]
            provider = productBase[2]
            quantity = int(productBase[5])
            unitaryPrice = float(productBase[4])
            subtotal = quantity * unitaryPrice
            purchaseTotal += subtotal
            
            self.tableProducto.setItem(row_idx, 0, self.create_item(provider))
            self.tableProducto.setItem(row_idx, 1, self.create_item(product))
            self.tableProducto.setItem(row_idx, 2, self.create_item(str(quantity)))
            self.tableProducto.setItem(row_idx, 3, self.create_item(f"{unitaryPrice:.2f} $"))
            self.tableProducto.setItem(row_idx, 4, self.create_item(f"{subtotal:.2f} $"))

        item_label = QTableWidgetItem("Total: ")
        item_label.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font_label = item_label.font()
        font_label.setBold(True)
        item_label.setFont(font_label)
        self.tableWidget.setItem(0, 0, item_label)

        item_monto = QTableWidgetItem(f"{purchaseTotal:.2f} $")
        item_monto.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font_monto = item_monto.font()
        font_monto.setBold(True)
        item_monto.setFont(font_monto)
        item_monto.setForeground(QtGui.QColor("#487c7e")) 
        
        self.tableWidget.setItem(0, 1, item_monto)

    def create_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def openWindow(self, purchaseData):
        self.purchaseData = purchaseData
        self.load_data(purchaseData)
        self.showMaximized()
        
    def cancelOperation(self):
        from app.views.management.buy.BuyView import BuyView 
        self.BuyView = BuyView()
        self.BuyView.showMaximized()
        self.close()
        
    def purchaseConfirmed(self):
        counter = 0
        purchaseTotal = 0.0
        
        for data in self.purchaseData:
            productBase = getProduct(data.get('id', 'N/A'))
            productBase += (data.get('quantity', 0),)
            
            quantity = int(productBase[5])
            
            unitaryPrice = float(productBase[4])
            subtotal = quantity * unitaryPrice
            purchaseTotal += subtotal 
            
            if counter == 0:        
                from app import session
                preUsername = geUserName(session.currentUserCedula)
                username = preUsername[0] + " " + preUsername[1]
                newcompra(purchaseTotal,username)
                counter += 1
            
            newDetailCompra(getLastCompra(), productBase[0],quantity, unitaryPrice,subtotal)
            
            if getInventoryProduct(productBase[0]):
                currentQuantity = getInventoryProductQuantity(productBase[0])
                newQuantity = currentQuantity[0] + quantity
                updateInventoryProductQuantity(productBase[0], newQuantity)
            else:
                newInventoryProduct(productBase[0], quantity)
        
            if quantity == productBase[3]:
                deleteProduct(productBase[0])
            else:
                newStock = productBase[3] - quantity
                updateProductQuantity(productBase[0], newStock)
            
        updateHistoryTotalPurchase(getLastCompra(), purchaseTotal)
        QMessageBox.information(self, "Éxito", "Compra realizada exitosamente.")
        self.cancelOperation()
