import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from views.auth.login import LoginView 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginView()
    ventana.show()
    sys.exit(app.exec())
