from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from app.windows.py.sidebarWds import Ui_Form
from PyQt5.QtCore import QEvent, Qt, QTimer

class sidebarView(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_sidebar()
        self.make_labels_clickable()
        
    def setup_sidebar(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        
    def show_sidebar(self):
        if self.parent():
            parent_rect = self.parent().geometry()
            self.resize(300, parent_rect.height())
            self.move(parent_rect.left(), parent_rect.top())
        
        self.show()
        
        QTimer.singleShot(100, self.install_event_filter)
        
    def install_event_filter(self):
        QApplication.instance().installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            click_pos = event.globalPos()
            if not self.rect().contains(self.mapFromGlobal(click_pos)):
                self.hide()
                QApplication.instance().removeEventFilter(self)
        return False
        
    def hideEvent(self, event):
        QApplication.instance().removeEventFilter(self)
        super().hideEvent(event)

    def make_labels_clickable(self):
        """Hacer que los labels sean clickeables y conectar sus señales"""
        # Lista de labels que queremos hacer clickeables
        clickable_labels = [
            self.labelInventario,
            self.labelNuevo,
            self.labelHistorial,
            self.labelEstadistica,
            self.label_13  # También el label "Salir"
        ]
        
        # Configurar cada label como clickeable
        for label in clickable_labels:
            label.setProperty("clickable", "true")
            label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            label.mousePressEvent = self.create_click_handler(label.objectName())

    def create_click_handler(self, label_name):
        """Crear un manejador de eventos para cada label"""
        def click_handler(event):
            print("hola")  # Esto se ejecutará en cada clic
            # También puedes imprimir el nombre del label que fue clickeado
            print(f"Label clickeado: {label_name}")
            
            # Aquí puedes agregar lógica específica para cada label si lo deseas
            if label_name == "labelInventario":
                print("Acción: Inventario")
            elif label_name == "labelNuevo":
                print("Acción: Nuevo producto")
            elif label_name == "labelHistorial":
                print("Acción: Historial")
            elif label_name == "labelEstadistica":
                print("Acción: Estadísticas")
            elif label_name == "label_13":
                print("Acción: Salir")
                
        return click_handler
