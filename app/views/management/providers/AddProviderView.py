import re
from PyQt5 import QtWidgets, QtCore
from app.windows.py.providersRegistrationWds import Ui_Form 
from app.views.management.providers.RegisterProductsView import RegisterProducts
from app.database.auth.get import getProviderData

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class AddProviderView(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Crear Proveedor")

        # Configuración inicial
        self.comboBox.setCurrentText("J")
        self.updateRIFPlaceholder("J")
        
        # Teléfono: Permitimos que el usuario escriba el código de área libremente o lo fijamos
        # Configurar el teléfono con una máscara que muestre guiones bajos
        self.lineEditTelefonoEmpresa.setText("0")
        self.lineEditTelefonoEmpresa_2.setEnabled(False)
        self.lineEditTelefonoEmpresa.setInputMask("9999-9999999;_")

        # Opcional: poner un placeholder text para mayor claridad
        self.lineEditTelefonoEmpresa.setPlaceholderText("ej: 0412-1234567")


        # Conexiones
        self.btnCancelar.clicked.connect(self.cancelOperation)
        self.btnGuardar.clicked.connect(self.validateInputs)            
        self.comboBox.currentTextChanged.connect(self.updateRIFPlaceholder)

    def isValidEmail(self, email):
        return bool(re.match(EMAIL_REGEX, email))
   
    def updateRIFPlaceholder(self, tipo_rif):
        """Actualiza la máscara según el tipo de RIF"""
        self.lineEditRIFEmpresa.clear()
        if tipo_rif == "J":
            # Máscara para 9 dígitos + 1 verificador: 10 dígitos en total
            self.lineEditRIFEmpresa.setInputMask("99999999-9;_")
        else:  # V o G
            # Máscara para 8 dígitos
            self.lineEditRIFEmpresa.setInputMask("99999999;_")
    
    def validateInputs(self):
        # Usamos .strip() pero recordamos que la máscara puede dejar guiones
        NameBusiness = self.lineEditNameEmpresa.text().strip().capitalize()
        UbicationBusiness = self.lineEditDireccionEmpresa.text().strip().capitalize()
        BusinessEmail = self.lineEditCorreoEmpresa.text().strip()
        
        # Limpieza de datos (Quitar guiones y underscores de la máscara)
        raw_rif = self.lineEditRIFEmpresa.text().replace('-', '').replace('_', '').strip()
        raw_phone = self.lineEditTelefonoEmpresa.text().replace('-', '').replace('_', '').strip()
        
        BusinessTipoRif = self.comboBox.currentText()
        BusinessFullRif = f"{BusinessTipoRif}-{self.lineEditRIFEmpresa.text()}"

        # --- VALIDACIONES ---

        # 1. Validación de RIF
        if not raw_rif:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor ingrese el RIF")
            return

        if BusinessTipoRif == "J":
            # Jurídico debe tener 10 dígitos numéricos
            if len(raw_rif) != 9:
                QtWidgets.QMessageBox.warning(self, "Error", "RIF Jurídico incompleto (deben ser 10 dígitos)")
                return
        else:
            # Personal/Gubernamental suele tener 8 o 9
            if len(raw_rif) < 8:
                QtWidgets.QMessageBox.warning(self, "Error", "El RIF debe tener al menos 8 dígitos")
                return

        # 2. Validación de Nombre y Ubicación
        if not NameBusiness or not UbicationBusiness:
            QtWidgets.QMessageBox.warning(self, "Error", "Nombre y ubicación son obligatorios")
            return

        # 3. Validación de Email
        if not self.isValidEmail(BusinessEmail):
            QtWidgets.QMessageBox.warning(self, "Error", "El correo electrónico no es válido")
            return

        # 4. Validación de Teléfono (Venezuela: 11 dígitos ej. 04241234567)
        if len(raw_phone) < 11:
            QtWidgets.QMessageBox.warning(self, "Error", "Número de teléfono incompleto (ej: 04241234567)")
            return
        
        if raw_phone[0] != '0':
            QtWidgets.QMessageBox.warning(self, "Error", "Número de teléfono inválido (debe comenzar con 0)")
            return
        
        print("rif:", BusinessFullRif)
        
        rif_clean = BusinessFullRif.replace('-', '').replace(' ', '').replace('J', '')
        
        # Buscar el proveedor en la base de datos
        provider_data = getProviderData(rif_clean)
        
        if provider_data:
            QtWidgets.QMessageBox.warning(self, "Error", f"El proveedor con RIF '{BusinessFullRif}' ya está registrado.")
            return

        self.openRegisterProducts(NameBusiness, UbicationBusiness, BusinessFullRif, BusinessEmail, raw_phone)
        
    def openRegisterProducts(self, NameBusiness, UbicationBusiness, BusinessFullRif, BusinessEmail, raw_phone):
        self.providerView = RegisterProducts()
        self.providerView.openWindow(NameBusiness, UbicationBusiness, BusinessFullRif, BusinessEmail, raw_phone)
        self.close()
        
     
    def cancelOperation(self):
        from app.views.management.providers.ProvidersView import ProvidersView 
        self.ProviderView = ProvidersView()
        self.ProviderView.showMaximized()
        self.close()