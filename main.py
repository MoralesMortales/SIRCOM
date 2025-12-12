import sys
from PyQt5.QtWidgets import QApplication
from app.database.init.init import initialize_db
from app.views.auth.LoginView import LoginView

if "--ci-test" in sys.argv:
    initialize_db() 
    print("CI Test flag detected. Exiting successfully without launching GUI.")
    sys.exit(0)

initialize_db()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    base = LoginView()
    base.showMaximized()
    sys.exit(app.exec())
