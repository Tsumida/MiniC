# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_lexer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Lexer(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.token_list = QtWidgets.QTableWidget(Form)
        self.token_list.setGeometry(QtCore.QRect(20, 0, 351, 291))
        self.token_list.setObjectName("token_list")
        self.token_list.setColumnCount(2)
        self.token_list.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.token_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.token_list.setHorizontalHeaderItem(1, item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.token_list.horizontalHeaderItem(0)
        item.setText(_translate("Form", "类型"))
        item = self.token_list.horizontalHeaderItem(1)
        item.setText(_translate("Form", "值"))

