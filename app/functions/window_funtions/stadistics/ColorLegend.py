from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

class ColorLegendWidget(QWidget):
    def __init__(self, color, text, parent=None):
        super().__init__(parent)
        self.color = color
        self.text = text
        self.setup_ui()
    
    def setup_ui(self):
        # Crear layout horizontal
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Cuadro de color (podría ser círculo también)
        color_label = QtWidgets.QLabel()
        color_label.setFixedSize(20, 20)
        color_label.setStyleSheet(f"""
            background-color: {self.color}; 
            border-radius: 3px; 
            border: 1px solid #666;
        """)
        
        # Texto del material
        text_label = QtWidgets.QLabel(self.text)
        text_label.setStyleSheet("font-weight: bold; color: #000000;")
        
        layout.addWidget(color_label)
        layout.addWidget(text_label)
        layout.addStretch()
        
        self.setLayout(layout)


