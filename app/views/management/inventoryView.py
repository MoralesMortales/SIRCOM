from PyQt5.QtWidgets import QWidget

from app.functions.window_funtions.management.inventory_Main import TableManager
from app.views.management.sidebarView import sidebarView
from app.windows.py.inventoryWds import Ui_Form

class inventoryMainView(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inventario")
        self.table_manager = TableManager(self.tableInventario, self)
        self.table_manager.configTable()
        self.table_manager.cargar_datos_inventario()
        self.inputBuscar.textChanged.connect(self.search_product)
        self.btnLateral.clicked.connect(self.showSidebar)
        self.tableInventario.cellClicked.connect(self.on_cell_clicked)

    def search_product(self, text_search):
        self.table_manager.search_product(text_search)
    
    def on_cell_clicked(self, row, column):
        self.table_manager.on_cell_clicked(row, column, self)
    
    def showSidebar(self):
        
        if hasattr(self, 'sidebar') and self.sidebar and self.sidebar.isVisible():
            self.sidebar.hide()
            return
        
        if not hasattr(self, 'sidebar') or self.sidebar is None:
            self.sidebar = sidebarView(self)
        
        self.sidebar.show_sidebar()
