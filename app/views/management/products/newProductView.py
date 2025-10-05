from PyQt5.QtWidgets import QWidget
from app.views.management.sidebarView import sidebarView
from app.windows.py.newProductWds import Ui_Form

class newProductView(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Nuevo Producto")
        self.btnLateral.clicked.connect(self.showSidebar)
    def showSidebar(self):
        
        if hasattr(self, 'sidebar') and self.sidebar and self.sidebar.isVisible():
            self.sidebar.hide()
            return
        
        if not hasattr(self, 'sidebar') or self.sidebar is None:
            self.sidebar = sidebarView(self)
        
        self.sidebar.show_sidebar()

