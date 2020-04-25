# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_parser.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Parser(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.syntax_tree = QtWidgets.QTreeView(Form)
        self.syntax_tree.setGeometry(QtCore.QRect(20, 10, 361, 271))
        self.syntax_tree.setObjectName("syntax_tree")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

