from PyQt5.QtWidgets import QWidget
from windows.py.loginWindow import Ui_container
from views.management.addProductView import addProductView  # ← Importar directamente

class LoginView(QWidget, Ui_container):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Autenticación")
        self.accessButtom.clicked.connect(self.openWindow)
        self.product_window = None  # ← Referencia a la ventana

    def openWindow(self):
        if self.product_window is None:
            self.product_window = addProductView()
            self.product_window.showMaximized()
        else:
            self.product_window.showMaximized()  # Mostrar si ya existe
            self.product_window.raise_()  # Traer al frente
            self.product_window.activateWindow()  # Activar
