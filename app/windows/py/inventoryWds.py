from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(831, 568)
        Form.setStyleSheet("QWidget {\n"
"    background-color: #f6f5b2;\n"
"}\n"
"\n"
"QLabel#labelTitulo {\n"
"    font-weight: bold;\n"
"    color: #000000;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"#inputBuscar {\n"
"    background-color: #dcdcdc;\n"
"    border: 1px solid #999;\n"
"    border-radius: 4px;\n"
"    padding: 4px 10px;\n"
"}\n"
"#inputBuscar:hover {\n"
"    background-color: #c0c0c0;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    background-color: #c6d8b6; \n"
"    border: 1px solid #666;\n"
"    border-radius: 8px;\n"
"    gridline-color: #444;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #e8e8e8;\n"
"    color: #000;\n"
"    font-weight: bold;\n"
"    border: 1px solid #666;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    background-color: #d2e3c6;\n"
"    border: 1px solid #555;\n"
"    padding: 6px;\n"
"}\n"
"QTableWidget::item:selected {\n"
"    background-color: #a4c686;\n"
"    color: #000;\n"
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(50, 50, 50, 50)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setSpacing(36)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelTitulo = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitulo.sizePolicy().hasHeightForWidth())
        self.labelTitulo.setSizePolicy(sizePolicy)
        self.labelTitulo.setSizeIncrement(QtCore.QSize(2, 2))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitulo.setFont(font)
        self.labelTitulo.setObjectName("labelTitulo")
        self.horizontalLayout.addWidget(self.labelTitulo)
        self.inputBuscar = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputBuscar.setFont(font)
        self.inputBuscar.setInputMask("")
        self.inputBuscar.setText("")
        self.inputBuscar.setObjectName("inputBuscar")
        self.horizontalLayout.addWidget(self.inputBuscar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setSpacing(36)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnLateral = QtWidgets.QPushButton(Form)
        self.btnLateral.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnLateral.setFont(font)
        self.btnLateral.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnLateral.setObjectName("btnLateral")
        self.horizontalLayout_3.addWidget(self.btnLateral)
        self.tableInventario = QtWidgets.QTableWidget(Form)
        self.tableInventario.setStyleSheet("color:\"#000\";")
        self.tableInventario.setLineWidth(0)
        self.tableInventario.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableInventario.setObjectName("tableInventario")
        self.tableInventario.setColumnCount(4)
        self.tableInventario.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableInventario.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableInventario.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableInventario.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableInventario.setHorizontalHeaderItem(3, item)
        self.tableInventario.horizontalHeader().setVisible(True)
        self.tableInventario.horizontalHeader().setCascadingSectionResizes(True)
        self.tableInventario.horizontalHeader().setDefaultSectionSize(100)
        self.tableInventario.horizontalHeader().setHighlightSections(True)
        self.tableInventario.horizontalHeader().setMinimumSectionSize(100)
        self.tableInventario.horizontalHeader().setSortIndicatorShown(False)
        self.tableInventario.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_3.addWidget(self.tableInventario)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.labelTitulo.setText(_translate("Form", "Inventario"))
        self.inputBuscar.setPlaceholderText(_translate("Form", "BUSCAR"))
        self.btnLateral.setText(_translate("Form", "➔"))
        item = self.tableInventario.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID"))
        item = self.tableInventario.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Nombre"))
        item = self.tableInventario.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Stock"))
        item = self.tableInventario.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Ver más"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
