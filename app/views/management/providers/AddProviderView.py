from PyQt5 import QtWidgets, QtCore
from app.windows.py.providersRegistrationWds import Ui_Form # Assuming this is your original UI file
from app.database.auth.insertNew import newProduct, newProvider
import re
from app.functions.tools.intFnt import NumericDelegate 

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class AddProviderView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Crear Proveedor")
        
        # Styles        
        self.tableProducto.verticalHeader().setDefaultSectionSize(50)
        self.tableProducto.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableProducto.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        # Definir el número de columnas (6 de datos + 1 de botón)
        self.tableProducto.setColumnCount(7)
        self.setupTable()

        # Ponerle nombres a las cabeceras para que sepas qué escribir en cada una
        self.tableProducto.setHorizontalHeaderLabels([
            "Producto", "Stock", "Precio", "Cant. Min Desc", "Descuento", "Stock Min", "Borrar"
        ])

        # Ajustar el tamaño para que se vean todas
        header = self.tableProducto.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        tooltips = [
            "Nombre del producto o servicio",
            "Cantidad disponible actualmente",
            "Precio por unidad de producto",
            "Cantidad mínima de compra para aplicar el descuento",
            "Monto o porcentaje de descuento aplicable",
            "Cantidad mínima permitida antes de reponer inventario",
            "Eliminar esta fila de la lista"
        ]

        # Aplicar los tooltips a cada sección del header
        header = self.tableProducto.horizontalHeader()
        for i, text in enumerate(tooltips):
            self.tableProducto.horizontalHeaderItem(i).setToolTip(text)
        
        # --- RESTRICCIONES DE COLUMNAS ---
        
        self.tableProducto.setItemDelegateForColumn(1, NumericDelegate(self, is_int=True))
        
        self.tableProducto.setItemDelegateForColumn(2, NumericDelegate(self, is_int=False))
        
        self.tableProducto.setItemDelegateForColumn(3, NumericDelegate(self, is_int=True))
        
        self.tableProducto.setItemDelegateForColumn(4, NumericDelegate(self, is_int=False, min_val=0, max_val=99))
        
        self.tableProducto.setItemDelegateForColumn(5, NumericDelegate(self, is_int=True))
        
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
        self.tableProducto.setRowCount(0)
        self.AddRow()
        
    def getProductData(self):
        product_list = []
        row_count = self.tableProducto.rowCount()
        
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self, "Tabla vacía", "Debe agregar al menos un producto.")
            return None

        for row in range(row_count):
            # Recogemos todos los items de la fila
            items = [self.tableProducto.item(row, col) for col in range(6)]
            
            # Verificamos que los objetos QTableWidgetItem existan y no estén vacíos
            if any(item is None or item.text().strip() == "" for item in items):
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Campos incompletos", 
                    f"La fila {row + 1} tiene celdas vacías. Por favor, complete todos los datos."
                )
                self.tableProducto.selectRow(row)
                return None

            try:
                # Extracción y limpieza
                name = items[0].text().strip().capitalize()
                stock = int(items[1].text().strip())
                price = float(items[2].text().strip())
                min_desc = int(items[3].text().strip())
                descuento = float(items[4].text().strip())
                stock_min = int(items[5].text().strip())

                # Validaciones lógicas de negocio
                if any(val < 0 for val in [stock, price, min_desc, descuento, stock_min]):
                    raise ValueError("Valores negativos no permitidos")
                
                if stock_min > stock:
                    QtWidgets.QMessageBox.warning(self, "Validación", f"Fila {row+1}: El Stock Mínimo no puede ser mayor al Stock actual.")
                    return None

            except ValueError as e:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error de datos", 
                    f"Fila {row + 1}: Asegúrese de ingresar números válidos.\nError: {str(e)}"
                )
                return None

            product_list.append({
                "nombre": name,
                "precioUnitario": price,
                "stock": stock,
                "minDescuento": min_desc,
                "descuento": descuento,
                "stockMin": stock_min
            })
            
        return product_list
    
    def AddRow(self):
        row_count = self.tableProducto.rowCount()
        self.tableProducto.insertRow(row_count)
        
        # Columnas 0 a 5: Datos del producto
        for col in range(6):
            item = QtWidgets.QTableWidgetItem("")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.tableProducto.setItem(row_count, col, item)
        
        # Columna 6: Botón eliminar
        delete_btn = QtWidgets.QPushButton("–")
        delete_btn.setStyleSheet("font-weight: bold; font-size: 18px; color: #cc3333;")
        
        # IMPORTANTE: No pasamos el index aquí, lo calculamos dentro de deleteRow
        delete_btn.clicked.connect(self.deleteRow)
        
        self.tableProducto.setCellWidget(row_count, 6, delete_btn)
        self.tableProducto.scrollToBottom()

    def deleteRow(self):
        button = self.sender()
        if button:
            # Buscamos el índice basándonos en la posición del botón dentro de la tabla
            endpoint = button.mapToParent(QtCore.QPoint(0, 0))
            index = self.tableProducto.indexAt(endpoint)
            
            if index.isValid():
                self.tableProducto.removeRow(index.row())
                # Ya no es estrictamente necesario reloadRemoveBtns con esta lógica,
                # pero ayuda a mantener la integridad si usas otros métodos.
                self.reloadRemoveBtns()

    def reloadRemoveBtns(self):
        # Reconectamos los botones para asegurar que el 'sender' sea rastreable
        for row in range(self.tableProducto.rowCount()):
            widget = self.tableProducto.cellWidget(row, 6)
            if isinstance(widget, QtWidgets.QPushButton):
                try:
                    widget.clicked.disconnect()
                except TypeError:
                    pass
                widget.clicked.connect(self.deleteRow)
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

        if len(BusinessPhone) != 13:
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
        
        products = self.getProductData()
        if products:
            if newProvider(BusinessRif_v2, NameBusiness, UbicationBusiness, BusinessPhone, BusinessEmail):
                for p in products:
                    # Pasamos los nuevos argumentos a tu función de base de datos
                    newProduct(
                        p['nombre'], 
                        p['precioUnitario'], 
                        p['stock'], 
                        BusinessRif_v2,
                        p['minDescuento'],
                        p['descuento'],
                        p['stockMin']
                    )
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Proveedor y productos registrados.")
                self.cancelOperation()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Revisa que el RIF sea correcto.")
                return
        
    def cancelOperation(self):
        from app.views.management.providers.ProvidersView import ProvidersView 
        self.ProviderView = ProvidersView()
        self.ProviderView.showMaximized()
        self.close()