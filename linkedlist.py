from dataclasses import dataclass
from typing import Any

class Node:
    prev: 'Node | None' = None
    next: 'Node | None' = None
    data: Any = None

    def __init__(self, data: Any):
        self.data = data



class LinkedList:

    def __init__(self, data: Any):
        new_node = Node(data)
        self.head = new_node
        self.tail = new_node        
    
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
            print("삭제할 노드가 없습니다.")
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
        
         




