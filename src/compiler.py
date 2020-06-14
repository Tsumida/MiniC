"""
Author: 杨慧志
该模块是TinyC编译器的入口程序，包含了编译器的完整过程和命令行界面工具。
"""
from typing import List
import sys
import click


from PyQt5.QtWidgets import \
    QApplication, QMainWindow,QTableWidgetItem, \
    QFileDialog, QTreeWidgetItem, QHeaderView

from PyQt5.QtGui import QBrush, QColor

from sym_def import Token
from lexer import scan, pre_process
# from syntax_analysis import LRParse, LRParsingErr
from parser2 import LRParse
from tree_node import nTreeNode

from ui import *

# ==============================
COLOR_LIGHT_PINK = (255,182,193)
COLOR_PaleGreen = (152,251,152)

class MainWindowCtrl(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()

        # files
        self.text = ""
        self.src_path = ""

        # core
        self.tks = None
        self.syntax_tree = None

        # for ui
        self.root_item = None  # 保存起来, 不用每次都重新生成


    def prepare_ui(self):
        """
        用于初始化，令各个组件监听特定事件。
        :return:
        """
        self.main_ui.setupUi(self)
        self.main_ui.results.currentChanged.connect(self.slot_result_tab_changed)
        self.main_ui.actionOpenFile.triggered.connect(self.load_src)

        self.main_ui.results.setCurrentIndex(0)

    def load_src(self):
        """
        读取源代码文件，更新相关状态变量。
        :return:
        """
        self.reset_state()
        fdl = QFileDialog()
        path, _ = fdl.getOpenFileName(self, "load source", "../tests", "All Files (*)")
        print(path)
        with open(path, "r") as f:
            self.text = f.read()
            self.path = path

        if self.text:
            self.main_ui.source.setPlainText(self.text)
            self.result_lexer_update()

    def reset_state(self):
        """
        重置所有状态
        :return:
        """
        self.path = None
        self.text = None
        self.tks = None
        self.syntax_tree = None
        self.root_item = None
        print("state reset.")

    def result_lexer_update(self):
        """
        显示Token列表
        :return:
        """
        if not self.text:
            return
        self.tks = scan(pre_process(self.text))
        # print(self.tks)
        cnt = len(self.tks)
        tl = self.main_ui.token_list
        tl.setColumnCount(2)
        tl.setHorizontalHeaderLabels(["符号", "类型"])
        tl.setRowCount(cnt)
        for i, tk in enumerate(self.tks):
            tl.setItem(i, 0, QTableWidgetItem(f"{tk.name}"))
            tl.setItem(i, 1, QTableWidgetItem(f"{tk.type}"))
        tl.resizeColumnsToContents()

    def result_parser_update(self):
        """
        显示语法树
        :return:
        """
        # 点击某一项，显示其下面所有子节点
        if not self.tks or len(self.tks) == 0:
            return
        if not self.syntax_tree: # or tks changed.
            print("parsing tokens...")
            try:
                t = LRParse(self.tks)  # type = nTreeNode
                self.syntax_tree = t
            #except LRParsingErr as lre:
            except Exception as lre:
                print("catch LRParsingErr:\n", lre)
                print("miniC exited.")
                exit(-1)

        if not self.root_item:
            root_item = QTreeWidgetItem()
            root_item.setText(0, str(self.syntax_tree.root.character))
            root_item.setExpanded(False)
            self.show_childrens(self.syntax_tree.root, root_item)
            self.root_item = root_item

        stw = self.main_ui.stree_widget
        stw.setColumnCount(1)
        stw.setHeaderLabels(["符号"])

        # 添加水平滚动
        stw.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        stw.header().setStretchLastSection(False)

        stw.addTopLevelItem(self.root_item)
        stw.expandAll()
        # stw.show()

    def show_childrens(self, tree_node, tree_item: QTreeWidgetItem):
        """
        递归先序遍历构建QTreeWidgetItem树
        :return:
        """
        if not tree_node:
            return
        br = QBrush(QColor(*COLOR_PaleGreen))

        for child in tree_node.children:
            node_item = QTreeWidgetItem()
            node_item.setText(0, f"{child.character}")
            if isinstance(child.character, Token):
                node_item.setBackground(0, br)
            tree_item.addChild(node_item)
            self.show_childrens(child, node_item)


    def slot_result_tab_changed(self):
        """
        tab页面切换
        :return:
        """
        i = self.main_ui.results.currentIndex()
        if i == 0:
            self.result_lexer_update()
        elif i == 1:
            self.result_parser_update()
        else:
            pass


def gui():
    app = QApplication(sys.argv)
    ctrl = MainWindowCtrl()
    ctrl.prepare_ui()

    ctrl.show()
    sys.exit(app.exec_())


# cli()
gui()
