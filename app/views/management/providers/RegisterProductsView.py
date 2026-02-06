from PyQt5 import QtWidgets, QtCore
from app.windows.py.providersRegisterProductsWds import Ui_Form
from app.database.auth.insertNew import newProduct, newProvider
import re
from PyQt5.QtWidgets import QHeaderView, QTextEdit, QDialog, QVBoxLayout, QPushButton, QHBoxLayout
from app.functions.tools.intFnt import NumericDelegate 
from app.functions.tools.getIcon import getIcon
from PyQt5.QtGui import QIcon

# Importar función para verificar si el proveedor existe
from app.database.auth.get import getProviderData

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class DescriptionDialog(QDialog):
    """Diálogo personalizado para editar descripciones largas"""
    def __init__(self, initial_text="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Descripción")
        self.setModal(True)
        self.setMinimumSize(500, 300)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Área de texto para la descripción
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(initial_text)
        self.text_edit.setPlaceholderText("Escriba la descripción del producto aquí...")
        layout.addWidget(self.text_edit)
        
        # Botones
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


class RegisterProducts(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Registrar Pedidos")
        
        # Variables para datos del proveedor (se llenarán desde openWindow)
        self.nameBusiness = ""
        self.ubicationBusiness = ""
        self.fullRif = ""
        self.email = ""
        self.phone = ""
        
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
        self.labelTituloProveedores.setText(f"Registro de proveedores")
        
        # Primero verificar si el proveedor ya existe
        if self.checkProviderExists():
            # Si ya existe, preguntar si quiere continuar
            if not self.askContinueWithExistingProvider():
                # Si el usuario dijo NO, salir sin mostrar la ventana
                return  # ← ESTA ES LA CLAVE: retornar aquí
        
        else:
            # Si no existe, crear el proveedor primero
            if not self.createProvider():
                # Si no se pudo crear el proveedor, salir
                return
        
        # Solo mostrar ventana maximizada si todo está bien
        self.showMaximized()
    
    def checkProviderExists(self):
        """Verifica si el proveedor ya existe en la base de datos"""
        # Limpiar RIF para consulta (sin la 'J' inicial)
        rif_clean = self.fullRif.replace('-', '').replace(' ', '').replace('J', '')
        
        # Buscar el proveedor en la base de datos
        provider_data = getProviderData(rif_clean)
        
        if provider_data:
            return True
        return False
    
    def askContinueWithExistingProvider(self):
        """Pregunta al usuario si quiere continuar con un proveedor existente"""
        response = QtWidgets.QMessageBox.question(
            self,
            "Proveedor Existente",
            f"El proveedor '{self.nameBusiness}' ya está registrado.\n"
            f"¿Desea agregar productos a este proveedor existente?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes
        )
        
        if response == QtWidgets.QMessageBox.No:
            # Si no quiere continuar, regresar a la vista anterior
            self.cancelOperation()
            return False
        return True
    
    def createProvider(self):
        """Crea el proveedor en la base de datos"""
        # Limpiar RIF (remover la 'J' inicial y guiones para almacenar)
        print(self.fullRif, "AAAAAAAAAAAAAA")
        rif_clean = self.fullRif.replace('-', '').replace(' ', '').replace('J', '')
        
        try:
            # Intentar crear el proveedor
            success = newProvider(
                rif_clean,           # RIF (sin formato)
                self.nameBusiness,   # nombreEmpresa
                self.ubicationBusiness,  # DireccionEmpresa
                self.phone,          # telefono
                self.email           # correo
            )
            
            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Proveedor Registrado",
                    f"Proveedor '{self.nameBusiness}' registrado exitosamente."
                )
                return True
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo registrar el proveedor. Puede que el RIF ya exista."
                )
                self.cancelOperation()
                return False
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Error al registrar el proveedor:\n{str(e)}"
            )
            self.cancelOperation()
            return False
    
    def setupTable(self):
        """Configura la tabla de productos"""
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
        # Configurar encabezados
        headers = ["Código", "Nombre", "Descripción", "Existencia", "Stock Mínimo", "Precio Bs", "Eliminar"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Conectar la señal de doble clic para abrir el editor de descripción
        self.tableWidget.cellDoubleClicked.connect(self.onCellDoubleClicked)
        
        # Tooltips para las columnas
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
        
        # Aplicar delegates para validación
        self.tableWidget.setItemDelegateForColumn(3, NumericDelegate(self.tableWidget, is_int=True))
        self.tableWidget.setItemDelegateForColumn(4, NumericDelegate(self.tableWidget, is_int=True))
        self.tableWidget.setItemDelegateForColumn(5, NumericDelegate(self.tableWidget, is_int=False))
        
        # Añadir una fila inicial vacía
        self.addRow()
    
    def onCellDoubleClicked(self, row, column):
        """Maneja el doble clic en las celdas"""
        # Solo abrir el editor para la columna de descripción (columna 2)
        if column == 2:
            self.openDescriptionEditor(row, column)
    
    def openDescriptionEditor(self, row, column):
        """Abre el editor de descripción"""
        # Obtener el texto actual de la celda
        current_item = self.tableWidget.item(row, column)
        current_text = ""
        if current_item:
            current_text = current_item.text()
        
        # Crear y mostrar el diálogo
        dialog = DescriptionDialog(current_text, self)
        
        # Mostrar el diálogo en el centro de la ventana principal
        dialog.move(
            self.geometry().center().x() - dialog.width() // 2,
            self.geometry().center().y() - dialog.height() // 2
        )
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener el nuevo texto
            new_text = dialog.get_text()
            
            # Actualizar la celda
            if not current_item:
                current_item = QtWidgets.QTableWidgetItem(new_text)
                current_item.setFlags(current_item.flags() | QtCore.Qt.ItemIsEditable)
                current_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget.setItem(row, column, current_item)
            else:
                current_item.setText(new_text)

    def connectSignals(self):
        """Conecta las señales de los botones"""
        # Crear botón para agregar productos (si no existe en el UI)
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
            # Insertar el botón antes de la tabla
            # Buscar el layout correcto para insertar
            self.verticalLayout_4.insertWidget(1, self.btnAddProducto)
        
        # Conectar señales
        self.btnAddProducto.clicked.connect(self.addRow)
        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.saveProducts)
    
    def addRow(self):
        """Añade una nueva fila a la tabla de productos"""
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        
        # Crear items editables para las primeras 6 columnas (0-5)
        for col in range(6):
            item = QtWidgets.QTableWidgetItem("")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            # CENTRAR EL TEXTO EN LAS CELDAS
            item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            
            # Hacer que la descripción sea de solo lectura en la celda (se edita con doble clic)
            if col == 2:  # Columna de descripción
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # No editable directamente
                item.setToolTip("Doble clic para editar la descripción")
            
            self.tableWidget.setItem(row_count, col, item)
        
        # Crear el widget de acciones igual que en ProvidersView
        actions_widget = self.create_action_buttons(row_count)
        self.tableWidget.setCellWidget(row_count, 6, actions_widget)
        
        # Ajustar altura de la fila
        self.tableWidget.setRowHeight(row_count, 50)
        
        # Desplazar a la nueva fila
        self.tableWidget.scrollToBottom()
    
    def create_action_buttons(self, row_idx):
        """Crea los botones de acción (solo eliminar) igual que en ProvidersView"""
        # Obtener el ícono de eliminar
        trash_icon_path = getIcon("Trash.png")
        
        # Crear widget contenedor
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) 
        
        # Agregar espaciadores para centrar
        layout.addStretch() 
        
        # Botón eliminar con ícono
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
        
        # Agregar otro espaciador para centrar
        layout.addStretch() 
        
        # Conectar la señal
        btn_delete.clicked.connect(lambda: self.deleteRow(row_idx))
        
        return widget

    def deleteRow(self, row):
        """Elimina una fila específica de la tabla"""
        if row < self.tableWidget.rowCount():
            # Preguntar confirmación igual que en ProvidersView
            confirm = QtWidgets.QMessageBox.question(
                self, 
                "Confirmar Eliminación", 
                "¿Estás seguro de que deseas eliminar este producto?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                QtWidgets.QMessageBox.No
            )
            
            if confirm == QtWidgets.QMessageBox.Yes:
                self.tableWidget.removeRow(row)
                
                # Actualizar las conexiones de los botones restantes
                for r in range(self.tableWidget.rowCount()):
                    widget = self.tableWidget.cellWidget(r, 6)
                    if widget:
                        # Buscar el botón dentro del widget
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
            # Obtener todos los items de la fila (columnas 0-5)
            items = [self.tableWidget.item(row, col) for col in range(6)]
            
            # Verificar campos vacíos
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
                # Extraer y limpiar datos
                codigo = items[0].text().strip()
                nombre = items[1].text().strip().capitalize()
                descripcion = items[2].text().strip() if items[2] and items[2].text().strip() else ""
                existencia = int(float(items[3].text().strip()))
                stock_min = int(float(items[4].text().strip()))
                precio = float(items[5].text().strip())

                # Validaciones de negocio
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
        """Guarda los productos en la base de datos"""
        # Verificar que tenemos datos del proveedor
        if not self.fullRif:
            QtWidgets.QMessageBox.warning(
                self, 
                "Error", 
                "No se encontraron datos del proveedor. Vuelva a iniciar el proceso."
            )
            return
        
        # Verificar que el proveedor existe en la base de datos
        rif_clean = self.fullRif.replace('-', '').replace(' ', '').replace('J', '')
        provider_data = getProviderData(rif_clean)
        
        if not provider_data:
            # Si el proveedor no existe, intentar crearlo primero
            if not self.createProvider():
                return  # Si no se pudo crear, salir
        
        # Obtener datos de productos
        products = self.getProductData()
        if not products:
            return
        
        # Intentar guardar productos en la base de datos
        try:
            success_count = 0
            failed_products = []
            
            for p in products:
                try:
                    if newProduct(
                        p['nombre'],           # nombre
                        p['precio'],           # precioUnitario
                        p['existencia'],       # stock
                        rif_clean,             # rifProveedor
                        0,                     # minDescuento (valor por defecto)
                        0,                     # descuento (valor por defecto)
                        p['stockMinimo'],          # stockMinimo
                        p['descripcion'],        # descripcion
                        p['codigo']           # codigo
                    ):
                        success_count += 1
                    else:
                        failed_products.append(p['nombre'])
                except Exception as e:
                    failed_products.append(f"{p['nombre']} (error: {str(e)})")
            
            # Mostrar resultados
            if success_count == len(products):
                QtWidgets.QMessageBox.information(
                    self, 
                    "Éxito", 
                    f"Se registraron {success_count} producto(s) exitosamente para el proveedor {self.nameBusiness}."
                )
            result = QtWidgets.QMessageBox.information(
                self,
                "¿Crear otro Proveedor?",
                "¿Desea crear otro proveedor?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes
            )

            if result == QtWidgets.QMessageBox.Yes:
                from app.views.management.providers.AddProviderView import AddProviderView
                
                self.AddProviderView = AddProviderView()
                self.AddProviderView.showMaximized()
                self.close()

            elif result == QtWidgets.QMessageBox.No:
                self.cancelOperation()
                    
            elif success_count > 0:
                message = f"Se registraron {success_count} de {len(products)} productos.\n"
                if failed_products:
                    message += f"\nProductos no registrados:\n"
                    for prod in failed_products:
                        message += f"- {prod}\n"
                message += "\nLos productos no registrados pueden tener códigos duplicados."
                
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Resultado Parcial", 
                    message
                )
                self.cancelOperation()
            else:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error", 
                    "No se pudo registrar ningún producto. Verifique que los códigos no estén duplicados."
                )
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"Ocurrió un error al guardar los productos:\n{str(e)}"
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