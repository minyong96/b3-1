
from typing import Any

class Node:
    key: Any
    value: Any
    hash_value: int # 충돌 났을때 빠르게 찾기 위함
    next: 'Node | None' = None

    def __init__(self, key, value, hash_value, next=None):
        self.key = key
        self.value = value
        self.hash_value = hash_value  
        self.next = next

class HashMap:
    capacity: int
    table: list[Node] 
    _size: int
    load_factor: float
    threshold: int # 확장 임계치 

    def __init__(self):
        self.capacity = 16
        self.table = [None] * self.capacity
        self._size = 0
        self.load_factor = 0.75
        self.threshold = int(self.capacity * self.load_factor)
    
    
    def _get_hash(self, key:Any):
        key_str = str(key)

        hash_value = 0

        for char in key_str:
            hash_value = (hash_value << 5) - hash_value + ord(char)

            hash_value &= 0xFFFFFFFF # 오버플로우 막기

        return hash_value ^ (hash_value >> 16) # xor
    

    def _get_index(self, hash_value: int):
        return hash_value & (self.capacity - 1) #  정확히 방 개수 범위의 숫자를 남길 수 있음
    

    def _check_and_resize(self):
        if self._size > self.threshold:
            old_table = self.table
            self.capacity *= 2

            self.table = [None] * self.capacity
            self.threshold = int(self.capacity * self.load_factor)

            self._size = 0  # 처음 부터 다시 해시분배 해야됨 

            for head_node in old_table:
                current = head_node
                while current is not None:
                    next_node = current.next # 기존 노드의 next를 끊고 새 table에 배치해야됨
                    new_idx = self._get_hash(current.hash_value)

                    current.next = self.table[new_idx]
                    self.table[new_idx] = current
                    self._size += 1

                    current = next_node
                    


    
    def put(self, key:Any, value: Any):
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)


        if self.table[idx] is None:
            self.table[idx] = Node(key, value, hash_value)
            self._size += 1
            self._check_and_resize()
            return
        
        current = self.table[idx]
        while True:
            if current.hash_value == hash_value and current.key == key:
                current.value = value
                return
            
            if current.next is None:
                break

            current = current.next
        
        current.next = Node(key, value, hash_value)
        self._size += 1
        self._check_and_resize()



    def get(self, key:Any):
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)

        if self.table[idx] is None:
            return
        
        current = self.table[idx]
        
        while True:
            if current.hash_value == hash_value and current.key == key:
                return current.value
            
            if current.next is None:
                break

            current = current.next



    def remove(self, key:Any):
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)

        if self.table[idx] is None:
            return
        
        current = self.table[idx]
        prev = None

        while current is not None:
            if current.hash_value == hash_value and current.key == key:
                if prev is None:
                    self.table[idx] = current.next
                else:
                    prev.next = current.next

                self._size -=1
                return 
        
                
            prev = current
            current = current.next



    def contains(self, key:Any)-> bool:
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)

        if self.table[idx] is None:
            return
        
        current = self.table[idx]
        
        while True:
            if current.hash_value == hash_value and current.key == key:
                return True
            
            if current.next is None:
                break

            current = current.next

    
    def keys(self) -> list:
        all_keys = []

        for head_node in self.table:
            current = head_node

            while current is not None:
                all_keys.append(current.key)

                current = current.next
        
        return all_keys

    def size(self) -> int:
        return self._size