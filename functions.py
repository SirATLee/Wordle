class Stack:
    def __init__(self):
        self.items = []
        self.size = 0

    def is_empty(self):
        if self.size == 0: return True
        return False
    
    def push(self,value):
        self.items.append(value)
        self.size += 1

    def pop(self):
        if not self.is_empty():
            self.items.pop()
            self.size -= 1
        return

    def clear(self):
        self.items = []
        self.size = 0

    