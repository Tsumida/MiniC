class TreeNode:
    def __init__(self, character=None):
        self.character = character
        self.children = []


class nTreeNode:
    def __init__(self, kind=None, character=None):
        self.kind = kind
        self.character = character
        self.children = []
        self.sibling = []
