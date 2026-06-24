from dataclasses import dataclass
from typing import Any

class Node:
    prev: 'Node | None' = None
    next: 'Node | None' = None
    data: Any = None

    def __init__(self, data: Any):
        self.data = data



class LinkedList:
    head: Node | None
    tail: Node | None

    def __init__(self, data: Any = None):
        if data is not None:
            new_node = Node(data)
            self.head = new_node
            self.tail = new_node
        else:
            self.head = None
            self.tail = None
    
    def insert_back(self, data:Any):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node
            
    def insert_front(self, data:Any):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def remove_back(self):
        if self.head is None:
            return
        

        if self.head == self.tail:
            self.head = None
            self.tail = None
            return

        self.tail = self.tail.prev
        self.tail.next = None

    def remove_front(self):
        if self.head is None:
            return
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
            return


        self.head = self.head.next
        self.head.prev = None
        

    def get_nodes(self):
        if(self.head == None):
            return
        current = self.head
        while(current):
            print(current.data)
            current = current.next
        

    def get_node(self, index) -> Any:
        if(self.head == None):
            return
        
        if self.get_size() <= index:
            return
         
        current = self.head
        for i in range(index):
            current = current.next

        return current.data
    
    def get_size(self):
        if(self.head == None):
            return
        
        index = 0
        current = self.head
        while(current):
            index += 1
            print(current.data)
            current = current.next
         
        return index




