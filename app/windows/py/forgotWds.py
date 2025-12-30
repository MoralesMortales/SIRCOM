
from PyQt5 import QtCore, QtGui, QtWidgets
from app.functions.tools.getIcon import getIcon
UserIcon = getIcon("User.png")
LogoIcon = getIcon("Logo.png")

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(994, 710)
        Form.setStyleSheet("QWidget {\n"
"    font-family: Arial;\n"
"}\n"
"\n"
"#login {\n"
"    background: #F0F6F9;\n"
"}\n"
"\n"
"\n"
"#panelIzquierdo {\n"
"    background: #487c7e;\n"
"    border-top-left-radius: 20px;\n"
"    border-bottom-left-radius: 20px;\n"
"}\n"
"\n"
"#labelTitulo {\n"
"    color: white;\n"
"    font-size: 40px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#panelDerecho{\n"
"    background: #d1d2d4;\n"
"    border-top-right-radius: 20px;\n"
"    border-bottom-right-radius: 20px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background: white;\n"
"    border-radius: 4px;\n"
"    padding: 6px;\n"
"    border: 1px solid #c4c4c4;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #487c7e;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #333;\n"
"    font-size: 24px;\n"
"}\n"
"\n"
"#labelLink{\n"
"    color: #4054d6;\n"
"    font-size: 13px;\n"
"}\n"
"#labelLink:hover {\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background: #dedede;\n"
"    color: #333;\n"
"    border-radius: 6px;\n"
"    padding: 7px;\n"
"    border: none;\n"
"    font-size: 18px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: #cacaca;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: #b5b5b5;\n"
"}")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.panelIzquierdo = QtWidgets.QWidget(Form)
        self.panelIzquierdo.setObjectName("panelIzquierdo")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.panelIzquierdo)
        self.verticalLayout_2.setContentsMargins(20, 20, 50, 40)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.labelLogo = QtWidgets.QLabel(self.panelIzquierdo)
        self.labelLogo.setMaximumSize(QtCore.QSize(200, 200))
        self.labelLogo.setText("")
        self.labelLogo.setPixmap(QtGui.QPixmap(LogoIcon))
        self.labelLogo.setScaledContents(True)
        self.labelLogo.setObjectName("labelLogo")
        self.verticalLayout_5.addWidget(self.labelLogo, 0, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.panelIzquierdo)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.labelTitulo = QtWidgets.QLabel(self.panelIzquierdo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitulo.sizePolicy().hasHeightForWidth())
        self.labelTitulo.setSizePolicy(sizePolicy)
        self.labelTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitulo.setObjectName("labelTitulo")
        self.verticalLayout_2.addWidget(self.labelTitulo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.panelIzquierdo)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 3)
        self.verticalLayout_2.setStretch(3, 3)
        self.horizontalLayout.addWidget(self.panelIzquierdo)
        self.panelDerecho = QtWidgets.QWidget(Form)
        self.panelDerecho.setObjectName("panelDerecho")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.panelDerecho)
        self.verticalLayout.setContentsMargins(50, 40, 50, 40)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.labelIconUser = QtWidgets.QLabel(self.panelDerecho)
        self.labelIconUser.setMaximumSize(QtCore.QSize(100, 100))
        self.labelIconUser.setText("")
        self.labelIconUser.setTextFormat(QtCore.Qt.AutoText)
        self.labelIconUser.setPixmap(QtGui.QPixmap(UserIcon))
        self.labelIconUser.setScaledContents(True)
        self.labelIconUser.setObjectName("labelIconUser")
        self.verticalLayout.addWidget(self.labelIconUser, 0, QtCore.Qt.AlignHCenter)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(16)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.labelCedula = QtWidgets.QLabel(self.panelDerecho)
        self.labelCedula.setObjectName("labelCedula")
        self.verticalLayout_4.addWidget(self.labelCedula)
        self.lineEditCedula = QtWidgets.QLineEdit(self.panelDerecho)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditCedula.sizePolicy().hasHeightForWidth())
        self.lineEditCedula.setSizePolicy(sizePolicy)
        self.lineEditCedula.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEditCedula.setBaseSize(QtCore.QSize(0, -3968))
        self.lineEditCedula.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEditCedula.setObjectName("lineEditCedula")
        self.verticalLayout_4.addWidget(self.lineEditCedula)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(16)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.buttonCorreo = QtWidgets.QPushButton(self.panelDerecho)
        self.buttonCorreo.setMinimumSize(QtCore.QSize(250, 0))
        self.buttonCorreo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonCorreo.setObjectName("buttonCorreo")
        self.verticalLayout_3.addWidget(self.buttonCorreo, 0, QtCore.Qt.AlignHCenter)
        self.buttonCrear = QtWidgets.QPushButton(self.panelDerecho)
        self.buttonCrear.setMinimumSize(QtCore.QSize(250, 0))
        self.buttonCrear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonCrear.setObjectName("buttonCrear")
        self.verticalLayout_3.addWidget(self.buttonCrear, 0, QtCore.Qt.AlignHCenter)
        self.buttonVolver = QtWidgets.QPushButton(self.panelDerecho)
        self.buttonVolver.setMinimumSize(QtCore.QSize(250, 0))
        self.buttonVolver.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonVolver.setObjectName("buttonVolver")
        self.verticalLayout_3.addWidget(self.buttonVolver, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout.addWidget(self.panelDerecho)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">J 4121977-4</span></p></body></html>"))
        self.labelTitulo.setText(_translate("Form", "<html><head/><body><p>Bienvenido</p><p>a SIRCOM</p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">Copyright ©️ todos los derechos reservados</span></p></body></html>"))
        self.labelCedula.setText(_translate("Form", "Ingrese su usuario"))
        self.buttonCorreo.setText(_translate("Form", "Enviar correo"))
        self.buttonCrear.setText(_translate("Form", "Crear cuenta"))
        self.buttonVolver.setText(_translate("Form", "Volver"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
