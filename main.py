import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from app.database.init.init import initialize_db
from app.views.auth.LoginView import LoginView

if "--ci-test" in sys.argv:
    initialize_db() 
    print("CI Test flag detected. Exiting successfully without launching GUI.")
    sys.exit(0)

initialize_db()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = LoginView()
    ventana.show()
    # Usamos app.exec() como en tu original
    sys.exit(app.exec())
