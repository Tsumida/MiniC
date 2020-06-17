
'''
Copyright: 
Author: 黄涛
Version: 1.0
Date: 2020-06-01
No history version
符号表的节点定义
'''
# 符号表节点定义
class SymIDNode:
    def __init__(self, name):
        self.name = name  # 变量名
        self.val = 0  # 暂时不知道干什么
        self.type = ''  # 变量类型
        self.size = 0  # 如果isarray是为True，那么表示数组长度大小
        self.isarray = False  # 是否未一个数组
        self.offset = 0

# 函数表节点定义
class SymFun_IDNode:
    def __init__(self, name):
        self.name = name  # 函数名
        self.params = []  # 参数列表
        self.type = ''  # 返回值类型


# 函数表，符号表，全局变量符号表
class SymbolTable:
    def __init__(self, fun_information_table, fun_sym_table, extern_sym_table):
        self.fun_information_table = fun_information_table
        self.fun_sym_table = fun_sym_table
        self.extern_sym_table = extern_sym_table

    def look_up(self):
        return self.fun_information_table, self.fun_sym_table, self.extern_sym_table
