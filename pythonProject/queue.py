
class Queue:
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
        return self.items.pop(0)

    def peek(self):
        if self.size() == 0:
            return None
        return self.items[0]


queue = Queue()
queue.push(1)
queue.push(2)
queue.push(3)
print(queue.size())
print(queue.peek())
print(queue.pop())
print(queue.peek())
