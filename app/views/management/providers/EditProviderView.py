from PyQt5 import QtWidgets, QtCore
from app.windows.py.editproviderWds import Ui_Form
from app.views.management.providers.AddProviderView import AddProviderView
from app.database.auth.get import getProviderData, getProviderProducts
from app.database.auth.update import updateProduct, updateProvider
import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class EditProviderView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Editar Proveedor")
        
        self.rifProvider = 0
        self.provider = None
        
        self.tableProducto.verticalHeader().setDefaultSectionSize(50)
        self.addBtn()
        self.btnAddProducto.clicked.connect(self.AddRow)
        
        self.lineEditRIFEmpresa.setInputMask("J-99999999-9")
        self.lineEditTelefonoEmpresa.setInputMask("\\0999-9999-999")

        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.validateInputs)
    
    def isValidEmail(self, email):
        if not email:
            return False
            
        if re.match(EMAIL_REGEX, email):
            return True
        else:
            return False
        
    def openWindow(self, rifProvider):
        self.rifProvider = rifProvider
        self.setupTable(self.rifProvider)
        
        self.provider = getProviderData(self.rifProvider)
        if self.provider:
            self.setTextOnInputs(self.provider)
            self.showMaximized()
    
    def setTextOnInputs(self, provider):
        self.lineEditNameEmpresa.setText(str(provider[0]))
        self.lineEditDireccionEmpresa.setText(str(provider[1]))
        self.lineEditTelefonoEmpresa.setText(str(provider[2]))    
        self.lineEditCorreoEmpresa.setText(str(provider[3]))
        
        self.lineEditRIFEmpresa.setText(str(self.rifProvider))
        self.lineEditRIFEmpresa.setReadOnly(True)
             
    def cancelOperation(self):
        from app.views.management.providers.ProvidersView import ProvidersView 
        self.ProviderView = ProvidersView()
        self.ProviderView.showMaximized()
        self.close()
        
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
            
            if updateProvider(BusinessRif_v2, NameBusiness, UbicationBusiness, BusinessPhone, BusinessEmail):
                product_data = self.getProductData()
                
                for i in product_data:
                    id_p = i['id']
                    nombre = i['nombre']
                    stock = i['stock']
                    precio = i['precioUnitario']
                    
                    if id_p:
                        updateProduct(id_p, nombre, precio, stock)
                    else: 
                        from app.database.auth.insertNew import newProduct
                        newProduct(nombre, precio, stock, BusinessRif_v2)

                QtWidgets.QMessageBox.information(self, "Éxito", "Proveedor y productos actualizados.")                
                self.cancelOperation()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Revisa que los datos sean correctos.")
                return 

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
          

    def AddRow(self):
        self.AddDataRow(id="", nombre="", stock="", precio="")
        self.tableProducto.scrollToBottom()

    def reloadRemoveBtns(self):
        for row in range(self.tableProducto.rowCount()):
            widget = self.tableProducto.cellWidget(row, 3)
            if isinstance(widget, QtWidgets.QPushButton):
                try:
                    widget.clicked.disconnect()
                except TypeError:
                    pass
                
                widget.clicked.connect(lambda _, r=row: self.deleteRow(r))
  
    def getProductData(self):

        product_list = []
        row_count = self.tableProducto.rowCount()
        
        if row_count == 0:
            return product_list

        for row in range(row_count):
            item_id = self.tableProducto.item(row, 0)
            item_name = self.tableProducto.item(row, 1)
            item_stock = self.tableProducto.item(row, 2)
            item_price = self.tableProducto.item(row, 3)
            
            id_val = item_id.text() if item_id else ""
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
                return None

            product_list.append({
                "id": id_val if id_val != "" else None,
                "nombre": name,
                "precioUnitario": price,
                "stock": stock
            })
            
        return product_list

    
    def setupTable(self, rifProvider):
        # 1. Definimos que la tabla tiene 5 columnas (0 a 4)
        self.tableProducto.setColumnCount(5)
        
        # 2. Ponemos los títulos (El primero es vacío porque el ID no se verá)
        self.tableProducto.setHorizontalHeaderLabels(["", "Producto", "Stock", "Precio", ""])
        
        # 3. OCULTAR LA COLUMNA 0 (ID)
        self.tableProducto.setColumnHidden(0, True)
        
        # 4. Ajustar anchos (Opcional, para que se vea mejor)
        header = self.tableProducto.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) # El nombre se estira
        self.tableProducto.setColumnWidth(2, 80)  # Stock fijo
        self.tableProducto.setColumnWidth(3, 100) # Precio fijo
        self.tableProducto.setColumnWidth(4, 50)  # Botón borrar fijo

        self.tableProducto.setRowCount(0)
        products = getProviderProducts(rifProvider)
        
        if products:
            for i in products:
                # i[0]=id, i[1]=nombre, i[2]=stock, i[3]=precio
                self.AddDataRow(i[0], i[1], i[2], i[3])
        else:
            self.AddRow()

    def AddDataRow(self, id="", nombre="", stock="", precio=""):
        row_count = self.tableProducto.rowCount()
        self.tableProducto.insertRow(row_count)
        
        # Columna 0: ID (Está oculta por el setupTable)
        item_id = QtWidgets.QTableWidgetItem(str(id) if id else "")
        # Quitamos la bandera de "Editable" por seguridad
        item_id.setFlags(item_id.flags() & ~QtCore.Qt.ItemIsEditable) 
        
        # Columna 1: Nombre
        item_producto = QtWidgets.QTableWidgetItem(str(nombre))
        
        # Columna 2: Stock
        item_stock = QtWidgets.QTableWidgetItem(str(stock))
        
        # Columna 3: Precio
        item_precio = QtWidgets.QTableWidgetItem(str(precio))
        
        # Asignar items
        self.tableProducto.setItem(row_count, 0, item_id)      
        self.tableProducto.setItem(row_count, 1, item_producto)
        self.tableProducto.setItem(row_count, 2, item_stock)
        self.tableProducto.setItem(row_count, 3, item_precio)
        
        # Botón eliminar en la columna 4
        delete_btn = QtWidgets.QPushButton("–")
        delete_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold; 
                font-size: 18px; 
                color: #cc3333; 
                background: transparent; 
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        # Conectamos directamente a la función que usa sender()
        delete_btn.clicked.connect(self.deleteRow)
        self.tableProducto.setCellWidget(row_count, 4, delete_btn)

    def deleteRow(self):
            button = self.sender()
            if button:
                index = self.tableProducto.indexAt(button.pos())
                if index.isValid():
                    row = index.row()
                    
                    item_id = self.tableProducto.item(row, 0)
                    product_id = item_id.text() if item_id else ""

                    if product_id:
                        confirm = QtWidgets.QMessageBox.question(
                            self, "Confirmar eliminación",
                            "¿Estás seguro de que deseas eliminar este producto de la base de datos?",
                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                        )

                        if confirm == QtWidgets.QMessageBox.Yes:
                            from app.database.auth.delete import deleteProduct
                            if deleteProduct(product_id):
                                self.tableProducto.removeRow(row)
                            else:
                                QtWidgets.QMessageBox.critical(self, "Error", "No se pudo eliminar el producto de la DB.")
                    else:
                        self.tableProducto.removeRow(row)