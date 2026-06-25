from typing import Any
from dataclasses import dataclass
from data_structure.linked_list import DoublyLinkedList, ListNode

@dataclass
class HashEntry:
    key: Any
    value: Any
    hash_value: int


class HashMap:
    capacity: int
    table: list[DoublyLinkedList] 
    _size: int
    load_factor: float
    threshold: int # 확장 임계치 

    def __init__(self):
        self.capacity = 16
        self.table = [
            DoublyLinkedList() for _ in range(self.capacity)
        ]
        self._size = 0
        self.load_factor = 0.75
        self.threshold = int(self.capacity * self.load_factor)
    
    
    def _get_hash(self, key:Any):
        key_str = str(key)

        hash_value = 0

        for char in key_str:
            hash_value = (hash_value << 5) - hash_value + ord(char) # 해시 충돌을 최소화하고 비트를 골고루 분산

            hash_value &= 0xFFFFFFFF # 오버플로우 막기

        return hash_value ^ (hash_value >> 16) # xor
    
    
    def _get_index(self, hash_value: int):
        return hash_value & (self.capacity - 1) #  정확히 방 개수 범위의 숫자를 남길 수 있음
    

    def _find_node(self, key: Any, hash_value: int) -> ListNode | None:
        idx = self._get_index(hash_value)
        bucket = self.table[idx]

        return bucket.find_node(
            lambda entry: entry.hash_value == hash_value and entry.key == key
        )


    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [DoublyLinkedList() for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.load_factor)

        old_size = self._size
        self._size = 0

        for bucket in old_table:
            for entry in bucket:
                idx = self._get_index(entry.hash_value)
                self.table[idx].insert_back(entry)
                self._size += 1

        assert self._size == old_size
                


    def put(self, key: Any, value: Any) -> None:
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)
        bucket = self.table[idx]

        node = bucket.find_node(
            lambda entry: entry.hash_value == hash_value and entry.key == key
        )

        if node is not None:
            node.data.value = value
            return

        bucket.insert_back(HashEntry(key, value, hash_value))
        self._size += 1

        if self._size > self.threshold:
            self._resize()


    def get(self, key: Any) -> Any:
        hash_value = self._get_hash(key)
        node = self._find_node(key, hash_value)

        if node is None:
            return None

        return node.data.value


    def remove(self, key: Any) -> Any:
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)
        bucket = self.table[idx]

        node = bucket.find_node(
            lambda entry: entry.hash_value == hash_value and entry.key == key
        )

        if node is None:
            return None

        removed_entry = bucket.remove_node(node)
        self._size -= 1

        return removed_entry.value

    def contains(self, key: Any) -> bool:
        hash_value = self._get_hash(key)
        node = self._find_node(key, hash_value)

        return node is not None

    
    def keys(self) -> list[Any]:
        result = []

        for bucket in self.table:
            for entry in bucket:
                result.append(entry.key)

        return result
    

    def values(self) -> list[Any]:
        result = []

        for bucket in self.table:
            for entry in bucket:
                result.append(entry.value)

        return result
    
    def items(self) -> list[tuple[Any, Any]]:
        result = []

        for bucket in self.table:
            for entry in bucket:
                result.append((entry.key, entry.value))

        return result
    

    def size(self) -> int:
        return self._size