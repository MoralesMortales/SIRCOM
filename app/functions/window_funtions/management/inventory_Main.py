from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
import sys
from pathlib import Path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
sys.path.append(str(project_root))
from app.database.management.loadInventory_Main import buscar_productos, obtener_detalles_producto, obtener_todos_productos

class TableManager:
    def __init__(self, table_widget):
        self.table = table_widget
    
    def configurar_tabla(self):
        """Configurar propiedades de la tabla"""
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
    
    def cargar_datos_inventario(self):
        """Cargar datos del inventario"""
        productos = obtener_todos_productos()
        self.actualizar_tabla(productos)
    
    def buscar_producto(self, texto_busqueda):
        """Filtrar productos según el texto de búsqueda"""
        if texto_busqueda.strip():
            productos = buscar_productos(texto_busqueda)
        else:
            productos = obtener_todos_productos()
        self.actualizar_tabla(productos)
    
    def actualizar_tabla(self, productos):
        self.table.setRowCount(0)
        
        for fila_idx, producto in enumerate(productos):
            self.table.insertRow(fila_idx)
            
            # ID
            item_id = QTableWidgetItem(str(producto[0]))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(fila_idx, 0, item_id)
            
            # Nombre
            item_nombre = QTableWidgetItem(producto[1])
            self.table.setItem(fila_idx, 1, item_nombre)
            
            # Stock
            item_stock = QTableWidgetItem(str(producto[2]))
            item_stock.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(fila_idx, 2, item_stock)
            
            # Botón "Ver más"
            btn_ver_mas = QTableWidgetItem("🔍 Ver")
            btn_ver_mas.setTextAlignment(Qt.AlignCenter)
            btn_ver_mas.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(fila_idx, 3, btn_ver_mas)
    
    def on_cell_clicked(self, row, column, parent_window):
        if column == 3:  # Columna "Ver más"
            producto_id = self.table.item(row, 0).text()
            producto_nombre = self.table.item(row, 1).text()
            self.mostrar_detalles_producto(producto_id, producto_nombre, parent_window)
    
    def mostrar_detalles_producto(self, producto_id, producto_nombre, parent_window):
        """Mostrar detalles del producto seleccionado"""
        producto = obtener_detalles_producto(producto_id)
        
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
