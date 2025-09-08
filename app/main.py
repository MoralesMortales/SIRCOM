import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from database.init.init import initialize_db
from views.auth.LoginView import LoginView 

initialize_db()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginView()
    ventana.show()
    sys.exit(app.exec())
