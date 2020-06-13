class SymIDNode:
    def __init__(self, name):
        self.name = name  # 变量名
        self.val = 0  # 暂时不知道干什么
        self.type = ''  # 变量类型
        self.size = 0  # 如果isarray是为True，那么表示数组长度大小
        self.isarray = False  # 是否未一个数组


class SymFun_IDNode:
    def __init__(self, name):
        self.name = name  # 函数名
        self.params = []  # 参数列表
        self.type = ''  # 返回值类型
