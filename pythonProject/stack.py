
class Stack:
    items: list

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.size() == 0:
            return None
        return self.items.pop()

    def peek(self):
        if self.size() == 0:
            return None
        return self.items[-1]


stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)

print(stack.size())
print(stack.peek())
print(stack.pop())
print(stack.peek())
