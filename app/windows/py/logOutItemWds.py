from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(879, 640)
        Form.setStyleSheet("QWidget {\n"
"    background-color: #f6f5b2;\n"
"    font-family: Arial, Helvetica, sans-serif;\n"
"    color: #000000;\n"
"}\n"
"\n"
"QLabel#labelTitulo {\n"
"    font-weight: bold;\n"
"    color: #000000;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-weight: bold;\n"
"    color: #000;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #eeeeee;\n"
"    border: 1px solid #aaa;\n"
"    border-radius: 4px;\n"
"    padding: 6px;\n"
"    font-size: 14px;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 1px solid #5a8dee;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QPushButton#btnRegistrar {\n"
"    background-color: #aee6a4;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 8px 20px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color: #000000;\n"
"}\n"
"QPushButton#btnRegistrar:hover {\n"
"    background-color: #94d98a;\n"
"}\n"
"\n"
"QPushButton#btnLateral {\n"
"    background-color: #dcdcdc;\n"
"    border: 1px solid #aaa;\n"
"    border-radius: 12px;\n"
"    padding: 4px;\n"
"}\n"
"QPushButton#btnLateral:hover {\n"
"    background-color: #c6c6c6;\n"
"}\n"
"")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_5.setContentsMargins(50, 50, 50, 50)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnLateral = QtWidgets.QPushButton(Form)
        self.btnLateral.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.btnLateral.setFont(font)
        self.btnLateral.setObjectName("btnLateral")
        self.horizontalLayout.addWidget(self.btnLateral)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitulo = QtWidgets.QLabel(Form)
        self.labelTitulo.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitulo.setFont(font)
        self.labelTitulo.setObjectName("labelTitulo")
        self.verticalLayout.addWidget(self.labelTitulo)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.labelNombre = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelNombre.setFont(font)
        self.labelNombre.setObjectName("labelNombre")
        self.verticalLayout_4.addWidget(self.labelNombre)
        self.lineEditNom = QtWidgets.QLineEdit(Form)
        self.lineEditNom.setObjectName("lineEditNom")
        self.verticalLayout_4.addWidget(self.lineEditNom)
        self.labelProveedor = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelProveedor.setFont(font)
        self.labelProveedor.setObjectName("labelProveedor")
        self.verticalLayout_4.addWidget(self.labelProveedor)
        self.lineEditDesc = QtWidgets.QLineEdit(Form)
        self.lineEditDesc.setObjectName("lineEditDesc")
        self.verticalLayout_4.addWidget(self.lineEditDesc)
        self.labelCantidad = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelCantidad.setFont(font)
        self.labelCantidad.setObjectName("labelCantidad")
        self.verticalLayout_4.addWidget(self.labelCantidad)
        self.lineEditCod = QtWidgets.QLineEdit(Form)
        self.lineEditCod.setObjectName("lineEditCod")
        self.verticalLayout_4.addWidget(self.lineEditCod)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.btnRegistrar = QtWidgets.QPushButton(Form)
        self.btnRegistrar.setMinimumSize(QtCore.QSize(200, 0))
        self.btnRegistrar.setObjectName("btnRegistrar")
        self.verticalLayout_3.addWidget(self.btnRegistrar)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnLateral.setText(_translate("Form", "➔"))
        self.labelTitulo.setText(_translate("Form", "Registrar salida"))
        self.labelNombre.setText(_translate("Form", "Nombre"))
        self.labelProveedor.setText(_translate("Form", "Proveedor"))
        self.labelCantidad.setText(_translate("Form", "Cantidad"))
        self.btnRegistrar.setText(_translate("Form", "Registrar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
