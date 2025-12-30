from PyQt5 import QtWidgets, QtCore
from app.windows.py.editproviderWds import Ui_Form
from app.views.management.providers.AddProviderView import AddProviderView
from app.database.auth.get import getProviderData, getProviderProducts
from app.database.auth.update import updateProduct, updateProvider
import re
from app.functions.tools.intFnt import NumericDelegate

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class EditProviderView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Editar Proveedor")
        
        self.rifProvider = 0
        self.provider = None
        
        # Estilos de tabla
        self.tableProducto.verticalHeader().setDefaultSectionSize(40)
        self.tableProducto.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        # Configuración de Columnas: ID(oculto) + 6 datos + Borrar = 8 columnas
        self.tableProducto.setColumnCount(8)
        self.setupHeaders()

        # Mascaras de entrada
        self.lineEditRIFEmpresa.setInputMask("J-99999999-9")
        self.lineEditTelefonoEmpresa.setInputMask("\\0999-9999-999")

        # Botones
        self.addBtn()
        self.btnAddProducto.clicked.connect(self.AddRow)
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
        # El RIF viene sin la 'J' y guiones de la tabla principal
        self.provider = getProviderData(self.rifProvider)
        
        if self.provider:
            self.setTextOnInputs(self.provider)
            self.loadProviderProducts()
            self.showMaximized()
            
    def setTextOnInputs(self, provider):
        # provider: (Nombre, Direccion, Telefono, Correo)
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
        
        products = self.getProductData()
        if products is not None:
            if updateProvider(BusinessRif_v2, NameBusiness, UbicationBusiness, BusinessPhone, BusinessEmail):
                for p in products:
                    if p['id']:
                        # Asegúrate de que updateProduct acepte estos nuevos 7 parámetros
                        updateProduct(p['id'], p['nombre'], p['precio'], p['stock'], p['minDesc'], p['desc'], p['stockMin'], p['update_param'])
                    else: 
                        from app.database.auth.insertNew import newProduct
                        newProduct(p['nombre'], p['precio'], p['stock'], BusinessRif_v2, p['minDesc'], p['desc'], p['stockMin'])

                QtWidgets.QMessageBox.information(self, "Éxito", "Datos actualizados correctamente.")
                self.cancelOperation() 

    def addBtn(self):
        self.btnAddProducto = QtWidgets.QPushButton(self.panelRegistro)
        self.btnAddProducto.setText("Agregar Producto (+)")
        self.verticalLayout_6.addWidget(self.btnAddProducto)
        self.btnAddProducto.setStyleSheet("font-weight: bold; font-size: 15px; background: transparent; border:none;")
              
    def setupHeaders(self):
        headers = ["ID", "Producto", "Stock", "Precio", "Cant. Min Desc", "Descuento", "Stock Min", "Borrar"]
        self.tableProducto.setHorizontalHeaderLabels(headers)
        self.tableProducto.setColumnHidden(0, True) # Ocultar ID
        
        header = self.tableProducto.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Aplicar Delegados Numéricos (ajustando índices por la columna ID oculta)
        self.tableProducto.setItemDelegateForColumn(2, NumericDelegate(self, is_int=True))   # Stock
        self.tableProducto.setItemDelegateForColumn(3, NumericDelegate(self, is_int=False))  # Precio
        self.tableProducto.setItemDelegateForColumn(4, NumericDelegate(self, is_int=True))   # Cant Min Desc
        self.tableProducto.setItemDelegateForColumn(5, NumericDelegate(self, is_int=False, min_val=0, max_val=99)) # %
        self.tableProducto.setItemDelegateForColumn(6, NumericDelegate(self, is_int=True))   # Stock Min
        
    def AddRow(self):
        self.AddDataRow(min_d=0, desc=0, s_min=0)
        
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
        for row in range(self.tableProducto.rowCount()):
            try:
                items = [self.tableProducto.item(row, i) for i in range(7)]
                if any(it is None or it.text().strip() == "" for it in items[1:]):
                    raise ValueError(f"Fila {row+1} incompleta")

                cantidad_stock = int(items[2].text())
                
                # DETERMINAR EL PARÁMETRO DE UPDATE
                # Si la cantidad es diferente a 0, enviamos 1, de lo contrario 0
                parametro_update = 1 if cantidad_stock != 0 else 0

                product_list.append({
                    "id": items[0].text() if items[0].text() else None,
                    "nombre": items[1].text().strip(),
                    "stock": cantidad_stock,
                    "precio": float(items[3].text()),
                    "minDesc": int(items[4].text()),
                    "desc": float(items[5].text()),
                    "stockMin": int(items[6].text()),
                    "update_param": parametro_update # Nuevo parámetro
                })
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))
                return None
        return product_list
    def loadProviderProducts(self):
        self.tableProducto.setRowCount(0)
        products = getProviderProducts(self.rifProvider)
        
        if products:
            for p in products:
                # p debe traer: (id, nombre, stock, precio, minDesc, desc, stockMin)
                self.AddDataRow(p[0], p[1], p[2], p[3], p[4], p[5], p[6])
        else:
            self.AddRow()
    
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

    def AddDataRow(self, id_p="", nom="", stock="", precio="", min_d=0, desc=0, s_min=0):
        row = self.tableProducto.rowCount()
        self.tableProducto.insertRow(row)
        
        values = [id_p, nom, stock, precio, min_d, desc, s_min]
        for col, val in enumerate(values):
            item = QtWidgets.QTableWidgetItem(str(val))
            if col == 0: item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.tableProducto.setItem(row, col, item)

        btn = QtWidgets.QPushButton("–")
        btn.setStyleSheet("color: red; font-weight: bold;")
        btn.clicked.connect(self.deleteRow)
        self.tableProducto.setCellWidget(row, 7, btn)
        
    def deleteRow(self):
        button = self.sender()
        index = self.tableProducto.indexAt(button.pos())
        if index.isValid():
            row = index.row()
            id_item = self.tableProducto.item(row, 0)
            p_id = id_item.text() if id_item else ""

            if p_id:
                confirm = QtWidgets.QMessageBox.question(self, "Eliminar", "¿Eliminar de la base de datos?", 
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if confirm == QtWidgets.QMessageBox.Yes:
                    from app.database.auth.delete import deleteProduct
                    if deleteProduct(p_id): self.tableProducto.removeRow(row)
            else:
                self.tableProducto.removeRow(row)
                