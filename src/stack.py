class stack:
    def __init__(self):
        self._st = []

    def push(self, obj):
        self._st.append(obj)

    def pop(self):
        if self.empty():
            print("Stack is Empty!")  # ERROR
        else:
            self._st.pop()

    def empty(self):
        return not bool(self._st)

    def top(self):
        if self.empty():
            print("Stack is Empty!")  # ERROR
        else:
            return self._st[-1]