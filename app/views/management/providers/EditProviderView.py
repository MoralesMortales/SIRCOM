# app/views/management/providers/EditProviderView.py
from PyQt5 import QtWidgets, QtCore
from app.windows.py.providersRegistrationWds import Ui_Form 
import re
from app.database.auth.update import updateProvider
from app.database.auth.get import getProviderData

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class EditProviderView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Editar Proveedor")
        
        # Variables para datos del proveedor
        self.original_rif = ""
        self.provider_name = ""
        
        # Configuración inicial
        self.lineEditTelefonoEmpresa.setText("0")
        self.lineEditTelefonoEmpresa_2.setEnabled(False)
        self.lineEditTelefonoEmpresa.setInputMask("9999-9999999;_")
        self.lineEditTelefonoEmpresa.setPlaceholderText("ej: 0412-1234567")
        
        # DESHABILITAR y estilizar el campo RIF
        self.lineEditRIFEmpresa.setEnabled(False)
        self.lineEditRIFEmpresa.setStyleSheet("""
            QLineEdit:disabled {
                background-color: #f5f5f5;
                color: #666;
                border: 1px solid #ddd;
            }
        """)
        
        self.comboBox.setEnabled(False)
        self.comboBox.setStyleSheet("""
            QComboBox:disabled {
                background-color: #f5f5f5;
                color: #666;
                border: 1px solid #ddd;
            }
        """)
        
        # Cambiar texto de botones
        self.btnGuardar.setText("Actualizar")
        
        # Crear botón adicional para gestionar productos
        self.btnGestionarProductos = QtWidgets.QPushButton("Gestionar Productos")
        self.btnGestionarProductos.setObjectName("btnGestionarProductos")
        self.btnGestionarProductos.setStyleSheet("""
            QPushButton#btnGestionarProductos {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 40px;
                background: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton#btnGestionarProductos:hover {
                background: #5a6268;
            }
        """)
        
        # Insertar el botón en el layout
        self.horizontalLayout_5.insertWidget(1, self.btnGestionarProductos)
        
        # Conexiones
        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.validateInputs)
        self.btnGestionarProductos.clicked.connect(self.manageProducts)

    def isValidEmail(self, email):
        return bool(re.match(EMAIL_REGEX, email))
   
    def updateRIFPlaceholder(self, tipo_rif):
        """Actualiza la máscara según el tipo de RIF"""
        self.lineEditRIFEmpresa.clear()
        if tipo_rif == "J":
            self.lineEditRIFEmpresa.setInputMask("99999999-9;_")
        else:  # V o G
            self.lineEditRIFEmpresa.setInputMask("99999999;_")
    
    def openWindow(self, rif):
        """Abre la ventana con los datos del proveedor para editar"""
        self.original_rif = rif  # Guardar el RIF original
        
        # Obtener datos del proveedor de la base de datos
        provider_data = getProviderData(rif)
        
        if not provider_data:
            QtWidgets.QMessageBox.warning(self, "Error", "No se encontraron datos del proveedor.")
            self.cancelOperation()
            return
        
        # provider_data contiene: (nombreEmpresa, direccionEmpresa, telefono, correo)
        nombre, direccion, telefono, correo = provider_data
        self.provider_name = nombre  # Guardar nombre para uso posterior
        
        # Extraer tipo de RIF y número
        if rif[0] in ['J', 'V', 'G']:
            tipo_rif = rif[0]
            numero_rif = rif[2:] if len(rif) > 2 else ""  # Quitar "J-" o "V-" o "G-"
        else:
            tipo_rif = "J"
            numero_rif = rif
        
        # Configurar comboBox según tipo de RIF
        self.comboBox.setCurrentText(tipo_rif)
        self.updateRIFPlaceholder(tipo_rif)
        
        # Rellenar campos con los datos del proveedor
        self.lineEditRIFEmpresa.setText(numero_rif)
        self.lineEditNameEmpresa.setText(nombre)
        self.lineEditDireccionEmpresa.setText(direccion)
        
        # Formatear teléfono (asegurar que tenga el formato correcto)
        telefono = str(telefono)
        if telefono:
            if len(telefono) >= 11:
                telefono_formateado = f"{telefono[:4]}-{telefono[4:]}"
            else:
                telefono_formateado = telefono
            self.lineEditTelefonoEmpresa.setText(telefono_formateado)
        
        self.lineEditCorreoEmpresa.setText(correo)
        
        # Mostrar ventana
        self.showMaximized()
    
    def manageProducts(self):
        """Abre la ventana para gestionar productos del proveedor"""
        from app.views.management.providers.ManageProductsView import ManageProductsView
        
        # Obtener datos actuales del formulario
        nombre = self.lineEditNameEmpresa.text().strip().capitalize()
        direccion = self.lineEditDireccionEmpresa.text().strip().capitalize()
        email = self.lineEditCorreoEmpresa.text().strip()
        telefono = self.lineEditTelefonoEmpresa.text().replace('-', '').replace('_', '').strip()
        
        # Validar datos antes de continuar
        if not nombre or not direccion or not email or len(telefono) < 11:
            QtWidgets.QMessageBox.warning(self, "Error", 
                "Complete todos los campos correctamente antes de gestionar productos.")
            return
        
        # Crear y abrir ventana de gestión de productos
        self.manageProductsView = ManageProductsView()
        self.manageProductsView.openWindow(
            nombre, 
            direccion, 
            self.original_rif, 
            email, 
            telefono
        )
        self.close()
    
    def validateInputs(self):
        # Obtener y limpiar datos
        NameBusiness = self.lineEditNameEmpresa.text().strip().capitalize()
        UbicationBusiness = self.lineEditDireccionEmpresa.text().strip().capitalize()
        BusinessEmail = self.lineEditCorreoEmpresa.text().strip()
        
        # Limpieza de datos
        raw_phone = self.lineEditTelefonoEmpresa.text().replace('-', '').replace('_', '').strip()
        
        # El RIF no se modifica, usar el original
        BusinessFullRif = self.original_rif
        
        # --- VALIDACIONES ---
        
        # 1. Validación de Nombre y Ubicación
        if not NameBusiness or not UbicationBusiness:
            QtWidgets.QMessageBox.warning(self, "Error", "Nombre y ubicación son obligatorios")
            return
        
        # 2. Validación de Email
        if not self.isValidEmail(BusinessEmail):
            QtWidgets.QMessageBox.warning(self, "Error", "El correo electrónico no es válido")
            return
        
        # 3. Validación de Teléfono
        if len(raw_phone) < 11:
            QtWidgets.QMessageBox.warning(self, "Error", "Número de teléfono incompleto (ej: 04241234567)")
            return
        
        if raw_phone[0] != '0':
            QtWidgets.QMessageBox.warning(self, "Error", "Número de teléfono inválido (debe comenzar con 0)")
            return
        
        # Actualizar el proveedor en la base de datos
        self.updateProvider(NameBusiness, UbicationBusiness, BusinessFullRif, BusinessEmail, raw_phone)
    
    def updateProvider(self, NameBusiness, UbicationBusiness, BusinessFullRif, BusinessEmail, raw_phone):
        """Actualiza el proveedor en la base de datos"""
        try:
            # Limpiar RIF para almacenar (usar el original)
            rif_clean = BusinessFullRif.replace('-', '').replace(' ', '').replace('J', '')
            
            # Llamar a la función de actualización
            success = updateProvider(
                rif_clean,  # RIF original (no cambia)
                NameBusiness,
                UbicationBusiness,
                raw_phone,
                BusinessEmail
            )
            
            if success:
                QtWidgets.QMessageBox.information(
                    self,
                    "Proveedor Actualizado",
                    f"Proveedor '{NameBusiness}' actualizado exitosamente.\n\n"
                    f"¿Desea gestionar los productos de este proveedor?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.Yes
                )
                
                # Si el usuario quiere gestionar productos
                if QtWidgets.QMessageBox.Yes:
                    self.manageProducts()
                else:
                    self.cancelOperation()
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo actualizar el proveedor."
                )
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Error al actualizar el proveedor:\n{str(e)}"
            )
    
    def cancelOperation(self):
        """Cancela la operación y regresa a la vista anterior"""
        from app.views.management.providers.ProvidersView import ProvidersView 
        self.ProviderView = ProvidersView()
        self.ProviderView.showMaximized()
        self.close()