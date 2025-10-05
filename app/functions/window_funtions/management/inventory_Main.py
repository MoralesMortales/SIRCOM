from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt

from app.database.management.loadInventory_Main import getDetatilsProduct, getAllProducts, searchProducts

class TableManager:
    def __init__(self, table_widget):
        self.table = table_widget

    def configTable(self):
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Interactive)
        header.geometriesChanged.connect(self.resize_columns)
        
        self.resize_columns()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

    def resize_columns(self):
        table_width = self.table.viewport().width()
        percentages = [10, 50, 25, 15]
        for i, percentage in enumerate(percentages):
            self.table.horizontalHeader().resizeSection(i, int(table_width * percentage / 100))

    def cargar_datos_inventario(self):
        productos = getAllProducts()
        self.updateTable(productos)
            
    def search_product(self, texto_busqueda):
        if texto_busqueda.strip():
            productos = searchProducts(texto_busqueda)
        else:
            productos = getAllProducts()
        self.updateTable(productos)
    
    def updateTable(self, productos):
        self.table.setRowCount(0)
        
        for fila_idx, producto in enumerate(productos):
            self.table.insertRow(fila_idx)
            
            item_id = QTableWidgetItem(str(producto[0]))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(fila_idx, 0, item_id)
            
            item_nombre = QTableWidgetItem(producto[1])
            self.table.setItem(fila_idx, 1, item_nombre)
            
            item_stock = QTableWidgetItem(str(producto[2]))
            item_stock.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(fila_idx, 2, item_stock)
            
            btn_ver_mas = QTableWidgetItem("🔍 Ver")
            btn_ver_mas.setTextAlignment(Qt.AlignCenter)
            btn_ver_mas.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(fila_idx, 3, btn_ver_mas)
    
    def on_cell_clicked(self, row, column, parent_window):
        if column == 3: 
            producto_id = self.table.item(row, 0).text()
            producto_nombre = self.table.item(row, 1).text()
            self.mostrar_detalles_producto(producto_id, producto_nombre, parent_window)
    
    def mostrar_detalles_producto(self, producto_id, producto_nombre, parent_window):
        producto = getDetatilsProduct(producto_id)
        
        if producto:
            mensaje = f"""
            <b>Detalles del Producto:</b><br><br>
            <b>ID:</b> {producto[0]}<br>
            <b>Nombre:</b> {producto[1]}<br>
            <b>Stock:</b> {producto[2]}<br>
            <b>Descripción:</b><br>{producto[3] if producto[3] else 'Sin descripción'}
            """
            
            QMessageBox.information(parent_window, "Detalles del Producto", mensaje)
        else:
            QMessageBox.warning(parent_window, "Error", "Producto no encontrado")
