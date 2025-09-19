from PyQt5.QtWidgets import QWidget

from app.functions.window_funtions.management.inventory_Main import TableManager
from app.windows.py.inventoryWds import Ui_Form

class inventoryMainView(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inventario")
        self.table_manager = TableManager(self.tableInventario)
        self.table_manager.configurar_tabla()
        self.table_manager.cargar_datos_inventario()
        self.inputBuscar.textChanged.connect(self.buscar_producto)
        self.btnLateral.clicked.connect(self.mostrar_menu_lateral)
        self.tableInventario.cellClicked.connect(self.on_cell_clicked)

    def buscar_producto(self, texto_busqueda):
        self.table_manager.buscar_producto(texto_busqueda)
    
    def on_cell_clicked(self, row, column):
        self.table_manager.on_cell_clicked(row, column, self)
    
    def mostrar_menu_lateral(self):
        print("Botón lateral clickeado")

