from PyQt5.QtWidgets import QWidget, QApplication
from app.windows.py.sidebar import Ui_Form
from PyQt5.QtCore import QEvent, Qt, QTimer

class sidebarView(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_sidebar()
        
    def setup_sidebar(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        
    def show_sidebar(self):
        if self.parent():
            parent_rect = self.parent().geometry()
            self.resize(300, parent_rect.height())
            self.move(parent_rect.left(), parent_rect.top())
        
        self.show()
        
        # Usar un timer para instalar el event filter después de mostrar
        QTimer.singleShot(100, self.install_event_filter)
        
    def install_event_filter(self):
        QApplication.instance().installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            # Verificar si el clic fue fuera de este widget
            click_pos = event.globalPos()
            if not self.rect().contains(self.mapFromGlobal(click_pos)):
                self.hide()
                QApplication.instance().removeEventFilter(self)
        return False
        
    def hideEvent(self, event):
        QApplication.instance().removeEventFilter(self)
        super().hideEvent(event)
