class SymIDNode:
    def __init__(self, name):
        self.name = name
        self.val = 0
        self.type = 0
        self.size = 0
        self.isarray = False


class SymFun_IDNode:
    def __init__(self, name):
        self.name = name
        self.params = []
        self.type = ''


