from PyQt5 import QtWidgets, QtCore
from app.windows.py.providersRegistrationWds import Ui_Form # Assuming this is your original UI file
from app.database.auth.insertNew import newProduct, newProvider
import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class AddProviderView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Crear Proveedor")
        self.setupTable()
        
        # Styles        
        self.tableProducto.verticalHeader().setDefaultSectionSize(50)
        self.tableProducto.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableProducto.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
        #Masks
        self.lineEditRIFEmpresa.setInputMask("J-99999999-9")
        self.lineEditTelefonoEmpresa.setInputMask("\\0999-9999-999")

        # Add Product button
        self.addBtn()
        self.btnAddProducto.clicked.connect(self.AddRow)

        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.validateInputs)
        
    def addBtn(self):
        self.btnAddProducto = QtWidgets.QPushButton(self.panelRegistro)
        self.btnAddProducto.setObjectName("btnAddProducto")
        self.btnAddProducto.setText("Agregar Producto (+)")
        self.verticalLayout_6.addWidget(self.btnAddProducto)
        self.btnAddProducto.setStyleSheet("""
            QPushButton#btnAddProducto {
                font-size: 16px; 
                font-weight: bold; 
                background: transparent;
                border: none;
            }
            QPushButton#btnAddProducto:hover {
                color: #487c7e;
            }
        """)            
          
    def setupTable(self):
        self.AddRow()

    def getProductData(self):

        product_list = []
        row_count = self.tableProducto.rowCount()
        
        if row_count == 0:
            return product_list

        for row in range(row_count):
            item_name = self.tableProducto.item(row, 0) 
            item_stock = self.tableProducto.item(row, 1)
            item_price = self.tableProducto.item(row, 2)
            
            name = item_name.text().strip().capitalize()
            stock = item_stock.text().strip()
            price = item_price.text().strip()
            
            if not name or not stock or not price:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error de Producto",
                    f"La fila {row + 1} tiene campos vacíos. Por favor, completa el Nombre, Stock y Precio."
                )
                
                self.tableProducto.selectRow(row) 
                return None 
            

            try:
                stock = int(stock)
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error de Stock",
                    f"El valor de Stock en la fila {row + 1} no es un número entero válido."
                )
                self.tableProducto.setCurrentCell(row, 1)
                return None

            try:
                price = float(price)
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error de Precio",
                    f"El valor de Precio Unitario en la fila {row + 1} no es un número válido."
                )
                self.tableProducto.setCurrentCell(row, 2)
                return None
            if int(stock) < 0 or int(price) < 0:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error de Producto",
                    f"La fila {row + 1} El Stock y Precio no pueden contener valores negativos."
                )
                
                self.tableProducto.selectRow(row) 
                return None 

            product_list.append({
                "nombre": name,
                "precioUnitario": price,
                "stock": stock
            })
            
        return product_list

    def AddRow(self):
        row_count = self.tableProducto.rowCount()
        self.tableProducto.insertRow(row_count)
        
        item_producto = QtWidgets.QTableWidgetItem("")
        item_producto.setFlags(item_producto.flags() | QtCore.Qt.ItemIsEditable)
        self.tableProducto.setItem(row_count, 0, item_producto)
        
        item_stock = QtWidgets.QTableWidgetItem("")
        item_stock.setFlags(item_stock.flags() | QtCore.Qt.ItemIsEditable)
        self.tableProducto.setItem(row_count, 1, item_stock)

        item_precio = QtWidgets.QTableWidgetItem("")
        item_precio.setFlags(item_precio.flags() | QtCore.Qt.ItemIsEditable)
        self.tableProducto.setItem(row_count, 2, item_precio)
        
        delete_btn = QtWidgets.QPushButton(self.tableProducto)
        delete_btn.setText("–")
        delete_btn.setStyleSheet("font-weight: bold; font-size: 18px; color: #cc3333;")
        
        delete_btn.clicked.connect(lambda _, row=row_count: self.deleteRow(row))
        
        self.tableProducto.setCellWidget(row_count, 3, delete_btn)
        
        self.tableProducto.scrollToBottom()

    def deleteRow(self, row_index):
        delete_btn = self.sender()
        if delete_btn:
            index = self.tableProducto.indexAt(delete_btn.pos())
            if index.isValid():
                actual_row = index.row()
                self.tableProducto.removeRow(actual_row)
                
                self.reloadRemoveBtns()
                
    def reloadRemoveBtns(self):
        for row in range(self.tableProducto.rowCount()):
            widget = self.tableProducto.cellWidget(row, 3)
            if isinstance(widget, QtWidgets.QPushButton):
                try:
                    widget.clicked.disconnect()
                except TypeError:
                    pass
                
                widget.clicked.connect(lambda _, r=row: self.deleteRow(r))

    def isValidEmail(self, email):
        if not email:
            return False
            
        if re.match(EMAIL_REGEX, email):
            return True
        else:
            return False

    def validateInputs(self):
        
        NameBusiness = self.lineEditNameEmpresa.text().strip().capitalize()
        UbicationBusiness = self.lineEditDireccionEmpresa.text().strip().capitalize()
        BusinessEmail = self.lineEditCorreoEmpresa.text().strip()
        BusinessPhone = self.lineEditTelefonoEmpresa.text().strip() 
        
        BusinessRif = self.lineEditRIFEmpresa.text().strip()
     
        BusinessRif_v2 = BusinessRif.replace('-', '').replace(' ', '').replace('J', '')
        
        if not NameBusiness:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese el nombre de la empresa")
            self.lineEditNameEmpresa.setFocus()
            return
        
        if not UbicationBusiness:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese la ubicacion de la empresa")
            self.lineEditDireccionEmpresa.setFocus()
            return
        
        if not BusinessEmail:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese el correo de la empresa")
            self.lineEditCorreoEmpresa.setFocus()
            return
        
        if not self.isValidEmail(BusinessEmail):
            QtWidgets.QMessageBox.warning(self, "Error", "El correo no es válido")
            self.lineEditCorreoEmpresa.setFocus()
            return
        
        if not BusinessPhone:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese un numero de telefono de la empresa")
            self.lineEditTelefonoEmpresa.setFocus()
            return
        
        if not BusinessRif:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese el RIF de la empresa")
            self.lineEditRIFEmpresa.setFocus()
            return
        
        if len(BusinessRif_v2) != 9:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese un RIF valido")
            self.lineEditRIFEmpresa.setFocus()
            return
        
        if self.getProductData():
            
            if newProvider(BusinessRif_v2, NameBusiness, UbicationBusiness, BusinessPhone, BusinessEmail):
                product_data = self.getProductData()
                
                for i in product_data:
                    nombre = i.get('nombre', 'N/A')
                    precio = i.get('precioUnitario', 0.0)
                    stock = i.get('stock', 0)
                    
                    newProduct(nombre,precio,stock,BusinessRif_v2)
                    
                    print(f"Nombre: {nombre} y Precio: {precio} y Stock: {stock}")

                print(f"exito",product_data)
                QtWidgets.QMessageBox.information(self, "Exito", "Se ha creado el proveedor exitosamente.")
                self.cancelOperation()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Revisa que el RIF sea correcto.")
                return
        
    def cancelOperation(self):
        from app.views.management.providers.ProvidersView import ProvidersView 
        self.ProviderView = ProvidersView()
        self.ProviderView.showMaximized()
        self.close()