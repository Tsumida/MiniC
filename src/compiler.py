"""
Author: 杨慧志
该模块是TinyC编译器的入口程序，包含了编译器的完整过程和命令行界面工具。
"""
from typing import List
import sys
import click

from PyQt5.QtWidgets import \
    QApplication, QMainWindow,QTableWidgetItem, QAbstractItemView

from sym_def import Token
from lexer import lex
import syntax_analysis
from syntax_analysis import LRParse


def scanner(src_path: str) -> List[Token]:
    print("scanning source...")
    return lex(src_path)


def syntax_checker(tks: List[Token]):
    print("parsing tokens...")
    try:
        t = LRParse(tks)
        t.dfs_print()
    except syntax_analysis.LRParsingErr as lre:
        print("catch LRParsingErr:\n", lre)
        print("miniC exited.")
        exit(-1)


@click.command()
@click.option("--path", help="path of source.", required=True)
def cli(path: str):
    """
    命令行接口， 使用click工具构建
    scanning + parsing
        python ./src/compiler.py -s --path=./tests/test_regular.txt

    :return:
    """

    tks = scanner(path)
    syntax_checker(tks)

from ui.main_body import *
from ui.ui_parser import *
from ui.ui_lexer import *


class MainWindowCtrl(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.tks_ui = Ui_Lexer()
        self.parser_ui = Ui_Parser()

        # files
        self.text = ""
        self.src_path = ""

        # core
        self.tks = None
        self.syntax_tree = None


    def prepare_ui(self):
        self.main_ui.setupUi(self)
        self.main_ui.results.currentChanged.connect(self.slot_result_tab_changed)

    def result_lexer_update(self):
        """
        显示Token列表
        :return:
        """
        if not self.tks or len(self.tks) == 0:
            self.tks = lex("../tests/test_regular.txt")

        cnt = len(self.tks)
        tl = self.main_ui.token_list
        tl.setRowCount(cnt)
        for i, tk in enumerate(self.tks):
            tl.setItem(i, 0, QTableWidgetItem(f"{tk.name}"))
            tl.setItem(i, 1, QTableWidgetItem(f"{tk.type}"))
        # tl.setEditTriggers(QTableWidgetItem.NoEditTriggers)

    def result_parser_update(self):
        """
        显示语法树
        :return:
        """
        # 点击某一项，显示其下面所有子节点
        if not self.tks or len(self.tks) == 0:
            return
        if not self.syntax_tree: # or tks changed.
            self.syntax_tree = LRParse(self.tks)


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
