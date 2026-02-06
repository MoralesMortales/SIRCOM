# app/views/management/providers/ManageProductsView.py
from PyQt5 import QtWidgets, QtCore
from app.windows.py.providersRegisterProductsWds import Ui_Form
from app.database.auth.insertNew import newProduct
from app.database.auth.get import getProviderData, getProductsByProvider, checkProductExists
from PyQt5.QtWidgets import QHeaderView, QTextEdit, QDialog, QVBoxLayout, QPushButton, QHBoxLayout
from app.functions.tools.intFnt import NumericDelegate 
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon
from app.database.auth.delete import deleteProduct
from app.database.auth.update import updateProduct

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class DescriptionDialog(QDialog):
    """Diálogo personalizado para editar descripciones largas"""
    def __init__(self, initial_text="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Descripción")
        self.setModal(True)
        self.setMinimumSize(500, 300)
        
        layout = QVBoxLayout(self)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(initial_text)
        self.text_edit.setPlaceholderText("Escriba la descripción del producto aquí...")
        layout.addWidget(self.text_edit)
        
        button_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.btn_cancel)
        
        button_layout.addStretch()
        
        self.btn_ok = QPushButton("Aceptar")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        button_layout.addWidget(self.btn_ok)
        
        layout.addLayout(button_layout)
    
    def get_text(self):
        """Retorna el texto ingresado"""
        return self.text_edit.toPlainText().strip()

class ManageProductsView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Gestionar Productos del Proveedor")
        
        # Variables para datos del proveedor
        self.nameBusiness = ""
        self.ubicationBusiness = ""
        self.fullRif = ""
        self.email = ""
        self.phone = ""
        
        # Cambiar texto del botón guardar
        self.btnGuardar.setText("Guardar Cambios")
        
        # Cambiar título de la ventana
        self.labelTituloProveedores.setText("Gestionar Productos")
        
        # Configurar la tabla
        self.setupTable()
        
        # Conectar señales
        self.connectSignals()
        
    def openWindow(self, nameBusiness, ubicationBusiness, fullRif, email, phone):
        """Abre la ventana con los datos del proveedor"""
        # Guardar datos del proveedor
        self.nameBusiness = nameBusiness
        self.ubicationBusiness = ubicationBusiness
        self.fullRif = fullRif
        self.email = email
        self.phone = phone
        
        # Actualizar título
        self.labelTituloProveedores.setText(f"Gestionar Productos: {nameBusiness}")
        
        # Verificar que el proveedor existe
        rif_clean = self.fullRif.replace('-', '').replace(' ', '').replace('J', '')
        provider_data = getProviderData(rif_clean)
        
        if not provider_data:
            QtWidgets.QMessageBox.warning(self, "Error", 
                "El proveedor no existe en la base de datos.")
            self.cancelOperation()
            return
        
        # Cargar productos existentes del proveedor
        self.loadExistingProducts(rif_clean)
        
        # Mostrar ventana maximizada
        self.showMaximized()
    
    def loadExistingProducts(self, rif_clean):
        """Carga los productos existentes del proveedor en la tabla"""
        try:
            # Obtener productos del proveedor
            products = getProductsByProvider(rif_clean)
            
            # Guardar códigos de productos existentes para comparación posterior
            self.existing_product_codes = [str(p[0]) for p in products]
            
            if products:
                # Limpiar tabla
                self.tableWidget.setRowCount(0)
                
                # Agregar cada producto a la tabla
                for product in products:
                    self.addExistingProduct(product)
            else:
                # Si no hay productos, agregar una fila vacía
                self.addRow()
                
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", 
                f"No se pudieron cargar los productos: {str(e)}")
            self.addRow()
    def addExistingProduct(self, product):
        """Añade un producto existente a la tabla"""
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        
        # Producto debe contener: (codigo, nombre, descripcion, existencia, stockMinimo, precio)
        for col in range(6):
            value = str(product[col]) if col < len(product) else ""
            item = QtWidgets.QTableWidgetItem(value)
            
            if col == 2:  # Columna de descripción
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setToolTip("Doble clic para editar la descripción")
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            
            item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row_count, col, item)
        
        # Widget de acciones
        actions_widget = self.create_action_buttons(row_count)
        self.tableWidget.setCellWidget(row_count, 6, actions_widget)
        self.tableWidget.setRowHeight(row_count, 50)
    
    def setupTable(self):
        """Configura la tabla de productos"""
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
        headers = ["Código", "Nombre", "Descripción", "Existencia", "Stock Mínimo", "Precio", "Eliminar"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.tableWidget.cellDoubleClicked.connect(self.onCellDoubleClicked)
        
        tooltips = [
            "Código único del producto",
            "Nombre del producto o servicio",
            "Descripción detallada del producto (doble clic para editar)",
            "Cantidad disponible inicial",
            "Cantidad mínima para alertas de stock",
            "Precio por unidad (Bs.)",
            "Eliminar este producto"
        ]
        
        for i, text in enumerate(tooltips):
            if i < self.tableWidget.columnCount():
                self.tableWidget.horizontalHeaderItem(i).setToolTip(text)
        
        self.tableWidget.setItemDelegateForColumn(3, NumericDelegate(self.tableWidget, is_int=True))
        self.tableWidget.setItemDelegateForColumn(4, NumericDelegate(self.tableWidget, is_int=True))
        self.tableWidget.setItemDelegateForColumn(5, NumericDelegate(self.tableWidget, is_int=False))
    
    def onCellDoubleClicked(self, row, column):
        """Maneja el doble clic en las celdas"""
        if column == 2:  # Columna de descripción
            self.openDescriptionEditor(row, column)
    
    def openDescriptionEditor(self, row, column):
        """Abre el editor de descripción"""
        current_item = self.tableWidget.item(row, column)
        current_text = current_item.text() if current_item else ""
        
        dialog = DescriptionDialog(current_text, self)
        dialog.move(
            self.geometry().center().x() - dialog.width() // 2,
            self.geometry().center().y() - dialog.height() // 2
        )
        
        if dialog.exec_() == QDialog.Accepted:
            new_text = dialog.get_text()
            
            if not current_item:
                current_item = QtWidgets.QTableWidgetItem(new_text)
                current_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                current_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget.setItem(row, column, current_item)
            else:
                current_item.setText(new_text)
    
    def connectSignals(self):
        """Conecta las señales de los botones"""
        if not hasattr(self, 'btnAddProducto'):
            self.btnAddProducto = QtWidgets.QPushButton("+ Agregar Producto")
            self.btnAddProducto.setObjectName("btnAddProducto")
            self.btnAddProducto.setStyleSheet("""
                QPushButton#btnAddProducto {
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    background: #487c7e;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    margin-bottom: 10px;
                }
            """)
            self.verticalLayout_4.insertWidget(1, self.btnAddProducto)
        
        self.btnAddProducto.clicked.connect(self.addRow)
        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.saveProducts)
    
    def addRow(self):
        """Añade una nueva fila a la tabla de productos"""
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        
        for col in range(6):
            item = QtWidgets.QTableWidgetItem("")
            
            if col == 2:  # Columna de descripción
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setToolTip("Doble clic para editar la descripción")
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            
            item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row_count, col, item)
        
        actions_widget = self.create_action_buttons(row_count)
        self.tableWidget.setCellWidget(row_count, 6, actions_widget)
        self.tableWidget.setRowHeight(row_count, 50)
        self.tableWidget.scrollToBottom()
    
    def create_action_buttons(self, row_idx):
        """Crea los botones de acción"""
        trash_icon_path = getIcon("Trash.png")
        
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        layout.addStretch()
        
        btn_delete = QtWidgets.QPushButton()
        btn_delete.setIcon(QIcon(trash_icon_path))
        btn_delete.setToolTip("Eliminar producto")
        btn_delete.setCursor(QtCore.Qt.PointingHandCursor)
        btn_delete.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
            }
            QPushButton:hover {
                background: #ffeaea;
                border-radius: 4px;
            }
        """)
        
        layout.addWidget(btn_delete)
        layout.addStretch()
        btn_delete.clicked.connect(lambda: self.deleteRow(row_idx))
        
        return widget

    def deleteRow(self, row):
        """Elimina una fila específica de la tabla"""
        if row < self.tableWidget.rowCount():
            confirm = QtWidgets.QMessageBox.question(
                self, 
                "Confirmar Eliminación", 
                "¿Estás seguro de que deseas eliminar este producto?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                QtWidgets.QMessageBox.No
            )
            
            if confirm == QtWidgets.QMessageBox.Yes:
                self.tableWidget.removeRow(row)
                
                for r in range(self.tableWidget.rowCount()):
                    widget = self.tableWidget.cellWidget(r, 6)
                    if widget:
                        btn_delete = widget.findChild(QtWidgets.QPushButton)
                        if btn_delete:
                            try:
                                btn_delete.clicked.disconnect()
                            except:
                                pass
                            btn_delete.clicked.connect(lambda checked, current_row=r: self.deleteRow(current_row))

    def getProductData(self):
        """Obtiene y valida los datos de los productos de la tabla"""
        product_list = []
        row_count = self.tableWidget.rowCount()
        
        if row_count == 0:
            QtWidgets.QMessageBox.warning(self, "Tabla vacía", 
                                         "Debe agregar al menos un producto.")
            return None

        for row in range(row_count):
            items = [self.tableWidget.item(row, col) for col in range(6)]
            
            required_fields = [0, 1, 3, 4, 5]  # Código, Nombre, Existencia, Stock Mínimo, Precio
            empty_fields = []
            
            for col in required_fields:
                item = items[col]
                if item is None or item.text().strip() == "":
                    field_name = self.tableWidget.horizontalHeaderItem(col).text()
                    empty_fields.append(field_name)
            
            if empty_fields:
                fields_str = ", ".join(empty_fields)
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Campos incompletos", 
                    f"Fila {row + 1}: Complete los campos requeridos: {fields_str}"
                )
                self.tableWidget.selectRow(row)
                return None

            try:
                codigo = items[0].text().strip()
                nombre = items[1].text().strip().capitalize()
                descripcion = items[2].text().strip() if items[2] and items[2].text().strip() else ""
                existencia = int(float(items[3].text().strip()))
                stock_min = int(float(items[4].text().strip()))
                precio = float(items[5].text().strip())

                if existencia < 0 or stock_min < 0 or precio < 0:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Valores inválidos", 
                        f"Fila {row + 1}: No se permiten valores negativos."
                    )
                    return None
                
                if len(codigo) == 0:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Validación",
                        f"Fila {row + 1}: El código del producto es requerido."
                    )
                    return None

            except ValueError as e:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error de datos", 
                    f"Fila {row + 1}: Ingrese valores numéricos válidos en Existencia, Stock Mínimo y Precio.\nError: {str(e)}"
                )
                return None

            product_list.append({
                "codigo": codigo,
                "nombre": nombre,
                "descripcion": descripcion,
                "existencia": existencia,
                "stockMinimo": stock_min,
                "precio": precio
            })
            
        return product_list
    
    def saveProducts(self):
        """Guarda, actualiza o elimina productos en la base de datos"""
        if not self.fullRif:
            QtWidgets.QMessageBox.warning(
                self, 
                "Error", 
                "No se encontraron datos del proveedor."
            )
            return
        
        rif_clean = self.fullRif.replace('-', '').replace(' ', '').replace('J', '')
        provider_data = getProviderData(rif_clean)
        
        if not provider_data:
            QtWidgets.QMessageBox.warning(self, "Error", "El proveedor no existe.")
            return
        
        # Obtener productos de la tabla
        table_products = self.getProductData()
        if table_products is None:  # Si hay error de validación
            return
        
        # 1. Verificar códigos duplicados en la tabla actual
        codigos_tabla = {}
        duplicados_tabla = []
        
        for idx, producto in enumerate(table_products):
            codigo = producto['codigo']
            if codigo in codigos_tabla:
                duplicados_tabla.append(codigo)
            codigos_tabla[codigo] = codigos_tabla.get(codigo, 0) + 1
        
        if duplicados_tabla:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                f"Los siguientes códigos están duplicados en la tabla:\n\n{', '.join(set(duplicados_tabla))}\n\nPor favor, corrija los códigos duplicados antes de guardar."
            )
            return
        
        # Obtener códigos de productos actualmente en la tabla
        current_codes = [p['codigo'] for p in table_products]
        
        try:
            success_count = 0
            failed_products = []
            updated_count = 0
            created_count = 0
            deleted_count = 0
            duplicate_db_count = 0  # Contador para códigos duplicados en DB
            error = False

            # 2. Verificar códigos duplicados con la base de datos
            for p in table_products:
                try:
                    # Verificar si el código ya existe en la base de datos
                    producto_existe = checkProductExists(p['codigo'], rif_clean)
                    
                    # También verificar si está en la lista de productos existentes originales
                    # (para detectar si alguien está intentando cambiar un código por uno existente)
                    is_new_in_table = (not hasattr(self, 'existing_product_codes') or 
                                    p['codigo'] not in self.existing_product_codes)
                    
                    if producto_existe and is_new_in_table:
                        # Este es un código que no estaba originalmente pero ya existe en DB
                        duplicate_db_count += 1
                        failed_products.append(
                            f"{p['nombre']} (código {p['codigo']} ya existe en la base de datos)"
                        )
                        continue
                    
                    if producto_existe:
                        # ACTUALIZAR producto existente
                        if updateProduct(
                            p['nombre'],
                            p['precio'],
                            p['existencia'],
                            p['stockMinimo'],
                            p['descripcion'],
                            rif_clean,
                            p['codigo']
                        ):
                            success_count += 1
                            updated_count += 1
                        else:
                            failed_products.append(f"{p['nombre']} (error al actualizar)")
                    else:
                        # CREAR nuevo producto
                        if newProduct(
                            p['nombre'],
                            p['precio'],
                            p['existencia'],
                            rif_clean,
                            0,
                            0,
                            p['stockMinimo'],
                            p['descripcion'],
                            p['codigo']
                        ):
                            success_count += 1
                            created_count += 1
                        else:
                            failed_products.append(f"{p['nombre']} Tiene un código ya en uso en la base de datos")
                            error = True
                            
                except Exception as e:
                    failed_products.append(f"{p['nombre']} (error: {str(e)})")
            
            # 3. Identificar productos eliminados (estaban en DB pero no en tabla)
            if hasattr(self, 'existing_product_codes') and not error:
                for old_code in self.existing_product_codes:
                    if old_code not in current_codes:
                        # Producto fue eliminado de la tabla
                        if deleteProduct(old_code, rif_clean):
                            deleted_count += 1
                            success_count += 1
                        else:
                            failed_products.append(f"Código {old_code} (error al eliminar)")
            
            # Mostrar resultados
            if duplicate_db_count > 0:
                # Si hay duplicados en la base de datos, mostrar advertencia específica
                # Extraer solo los códigos duplicados del mensaje de error
                codigos_duplicados = []
                for error in failed_products:
                    if 'ya existe' in error:
                        # Extraer el código del mensaje de error
                        # Formato esperado: "Nombre (código X ya existe en la base de datos)"
                        try:
                            # Buscar el código entre paréntesis
                            start_idx = error.find('código ') + 7
                            end_idx = error.find(' ya existe')
                            if start_idx != -1 and end_idx != -1:
                                codigo = error[start_idx:end_idx].strip()
                                codigos_duplicados.append(codigo)
                        except:
                            # Si no se puede extraer, mostrar el error completo
                            codigos_duplicados.append(error)
                
                if codigos_duplicados:
                    mensaje = f"Se encontraron {duplicate_db_count} código(s) que ya existen en la base de datos:\n\n"
                    mensaje += "• " + "\n• ".join(codigos_duplicados) + "\n\n"
                    mensaje += "Por favor, use códigos únicos para cada producto."
                else:
                    mensaje = f"Se encontraron {duplicate_db_count} código(s) duplicados en la base de datos."
                
                QtWidgets.QMessageBox.warning(
                    self,
                    "Códigos duplicados en base de datos",
                    mensaje
                )
            elif failed_products:
                # Si hay otros errores
                error_msg = "Se encontraron los siguientes errores:\n\n"
                error_msg += "• " + "\n• ".join(failed_products[:10])  # Mostrar solo los primeros 10 errores
                if len(failed_products) > 10:
                    error_msg += f"\n\n... y {len(failed_products) - 10} error(es) más"
                
                QtWidgets.QMessageBox.warning(self, "Error", error_msg)
            else:
                # Éxito completo
                summary = "Operación completada exitosamente"
                
                
                QtWidgets.QMessageBox.information(self, "Éxito", summary)
                self.cancelOperation()
                
                    
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"Error al procesar los productos:\n{str(e)}"
            )
    def cancelOperation(self):
        """Cancela la operación y regresa a la vista anterior"""
        try:
            from app.views.management.providers.ProvidersView import ProvidersView 
            self.ProviderView = ProvidersView()
            self.ProviderView.showMaximized()
            self.close()
        except ImportError as e:
            QtWidgets.QMessageBox.warning(
                self, 
                "Error", 
                f"No se pudo cargar la vista anterior: {str(e)}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self, 
                "Error", 
                f"Error al cambiar de ventana: {str(e)}"
            )