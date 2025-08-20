import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
    
    def inicializar_ui(self):
        self.setWindowTitle("Mi Primera App PyQt")
        self.setGeometry(100, 100, 400, 300)
        
        etiqueta = QLabel("¡Hola PyQt!", self)
        etiqueta.move(150, 100)
        
        boton = QPushButton("Haz clic", self)
        boton.move(150, 150)
        boton.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        print("¡Botón clickeado!")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())
