# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_score.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(513, 549)
        Form.setStyleSheet("background-color: rgb(64, 42, 21);")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(120, 210, 261, 331))
        self.tableWidget.setStyleSheet("background-color: rgb(249, 228, 211);\n"
"")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.Cow = QtWidgets.QLabel(Form)
        self.Cow.setGeometry(QtCore.QRect(10, 240, 101, 101))
        self.Cow.setText("")
        self.Cow.setObjectName("Cow")
        self.Cat = QtWidgets.QLabel(Form)
        self.Cat.setGeometry(QtCore.QRect(10, 410, 101, 101))
        self.Cat.setText("")
        self.Cat.setObjectName("Cat")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 30, 401, 167))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pics/rate.png"))
        self.label.setObjectName("label")
        self.Dog = QtWidgets.QLabel(Form)
        self.Dog.setGeometry(QtCore.QRect(390, 410, 101, 101))
        self.Dog.setText("")
        self.Dog.setObjectName("Dog")
        self.Goose = QtWidgets.QLabel(Form)
        self.Goose.setGeometry(QtCore.QRect(390, 240, 101, 101))
        self.Goose.setText("")
        self.Goose.setObjectName("Goose")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Шахматисты"))
