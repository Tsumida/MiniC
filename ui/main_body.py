# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_body.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1009, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 451, 741))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.results = QtWidgets.QTabWidget(self.centralwidget)
        self.results.setGeometry(QtCore.QRect(480, 10, 511, 781))
        self.results.setObjectName("results")
        self.tab_lexer = QtWidgets.QWidget()
        self.tab_lexer.setObjectName("tab_lexer")
        self.token_list = QtWidgets.QTableWidget(self.tab_lexer)
        self.token_list.setGeometry(QtCore.QRect(10, 20, 471, 741))
        self.token_list.setObjectName("token_list")
        self.token_list.setColumnCount(2)
        self.token_list.setRowCount(0)
        self.token_list.setHorizontalHeaderLabels(["符号", "类型"])
        self.results.addTab(self.tab_lexer, "")
        self.tab_parser = QtWidgets.QWidget()
        self.tab_parser.setObjectName("tab_parser")
        self.results.addTab(self.tab_parser, "")
        self.tab_code_gen = QtWidgets.QWidget()
        self.tab_code_gen.setObjectName("tab_code_gen")
        self.results.addTab(self.tab_code_gen, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.file = QtWidgets.QMenuBar(MainWindow)
        self.file.setGeometry(QtCore.QRect(0, 0, 1009, 26))
        self.file.setObjectName("file")
        self.menuFile = QtWidgets.QMenu(self.file)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.file)
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionClean_Source = QtWidgets.QAction(MainWindow)
        self.actionClean_Source.setObjectName("actionClean_Source")
        self.menuFile.addAction(self.actionOpenFile)
        self.file.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.results.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "int gcd(int a , int b){\n"
"    if ( b != 0)\n"
"        return gcd( b , a - a / b * b);\n"
"    else\n"
"        return a;\n"
"}\n"
""))
        self.results.setTabText(self.results.indexOf(self.tab_lexer), _translate("MainWindow", "词法分析"))
        self.results.setTabText(self.results.indexOf(self.tab_parser), _translate("MainWindow", "语法分析"))
        self.results.setTabText(self.results.indexOf(self.tab_code_gen), _translate("MainWindow", "代码生成"))
        self.menuFile.setTitle(_translate("MainWindow", "文件"))
        self.actionOpenFile.setText(_translate("MainWindow", "Open Source"))
        self.actionClean_Source.setText(_translate("MainWindow", "Clean Source"))

