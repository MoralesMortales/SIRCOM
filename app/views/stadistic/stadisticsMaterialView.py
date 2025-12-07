from app.views.management.sidebarView import sidebarView
from app.windows.py.stadisticsMaterialWds import Ui_Form
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from app.functions.window_funtions.stadistics.ColorLegend import ColorLegendWidget
from app.views.management.sidebarView import sidebarView
from app.windows.py.stadisticsMaterialWds import Ui_Form
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidgetItem


class stadisticMaterialView(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Estadísticas 1")
        self.btnLateral.clicked.connect(self.showSidebar)
        
        # Configurar matplotlib en el frame
        self.setup_matplotlib()
        
        # Configurar la lista de materiales
        self.setup_materiales_list()
        self.mostrar_grafica_materiales()
        
        self.entradasysalidasBtn.clicked.connect(self.showEntradaSalida)
    
    def setup_matplotlib(self):
        self.figure = plt.figure(figsize=(8, 6), facecolor='#f6f5b2')
        self.canvas = FigureCanvas(self.figure)
        
        # Añadir al frame que ya tienes en el designer
        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
    
    def setup_materiales_list(self):
        self.listWidget.clear()
        
        # Datos de ejemplo - puedes cambiar por tus datos reales
        self.materiales_data = [
            {"nombre": "Extensiones de hierro", "color": "#FF6B6B", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
            {"nombre": "Extensiones de hierro", "color": "#FF6B6B", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
            {"nombre": "Extensiones de hierro", "color": "#FF6B6B", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
            {"nombre": "Extensiones de hierro", "color": "#FF6B6B", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
            {"nombre": "Extensiones de hierro", "color": "#FF6B6B", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
            {"nombre": "Extensiones de hierro", "color": "#FF6B6B", "porcentaje": 5},
            {"nombre": "Extensiones de piedra", "color": "#4ECDC4", "porcentaje": 5},
            {"nombre": "Cemento en saco", "color": "#45B7D1", "porcentaje": 5},
        ]        
        # Añadir cada material a la lista
        for material in self.materiales_data:
            texto = f"{material['nombre']} - {material['porcentaje']}%"
            color_widget = ColorLegendWidget(material['color'], texto)
            
            item = QListWidgetItem(self.listWidget)
            item.setSizeHint(color_widget.sizeHint())
            
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, color_widget)
    
    def mostrar_grafica_materiales(self):
        self.figure.clear()
        
        # Preparar datos para la gráfica
        nombres = [mat['nombre'] for mat in self.materiales_data]
        porcentajes = [mat['porcentaje'] for mat in self.materiales_data]
        colores = [mat['color'] for mat in self.materiales_data]
        
        # Crear gráfica de torta
        ax = self.figure.add_subplot(111)
        ax.pie(porcentajes, labels=nombres, colors=colores, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución de Materiales', pad=20, fontsize=14, fontweight='bold')
        
        # Actualizar canvas
        self.canvas.draw()

    def showEntradaSalida(self):
        from app.views.stadistic.stadisticsEntradaSalidaView import stadisticEntradaSalidaView
        self.entradaSalidaView = stadisticEntradaSalidaView()
        self.entradaSalidaView.showMaximized()
        self.close()

    def showSidebar(self):
        
        if hasattr(self, 'sidebar') and self.sidebar and self.sidebar.isVisible():
            self.sidebar.hide()
            return
        
        if not hasattr(self, 'sidebar') or self.sidebar is None:
            self.sidebar = sidebarView(self)
        
        self.sidebar.show_sidebar()
    
    def actualizar_datos(self, nuevos_materiales):
        """Método para actualizar los datos desde fuera de la clase"""
        self.materiales_data = nuevos_materiales
        self.setup_materiales_list()
        self.mostrar_grafica_materiales()  # Actualizar gráfica automáticamente


