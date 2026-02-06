class Node:
  def __init__(self, data):
    self.data = data
    self.next = None

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

class Queue:
  def __init__(self):
    self.queue = []
    
  def enqueue(self, element):
    self.queue.append(element)

  def dequeue(self):
    if self.isEmpty():
      return "Queue is empty"
    return self.queue.pop(0)

  def peek(self):
    if self.isEmpty():
      return "Queue is empty"
    return self.queue[0]

  def isEmpty(self):
    return len(self.queue) == 0

  def size(self):
    return len(self.queue)
  
class LinkedList:
    def __init__(self):
        self.head = None 

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def delete_node(self, key):
        current = self.head
        prev = None

        if current and current.data == key:
            self.head = current.next
            current = None
            return

        while current and current.data != key:
            prev = current
            current = current.next

        if current is None:
            print(f"Không tìm thấy giá trị {key} trong danh sách.")
            return

        prev.next = current.next
        current = None

    def traverse_and_print(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def find_lowest_value(self):
        if not self.head:
            return None
        
        min_value = self.head.data
        current = self.head.next
        while current:
            if current.data < min_value:
                min_value = current.data
            current = current.next
        return min_value

    def sort(self):
        if self.head is None:
            return

        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next