from data_structure.bucket.bucket_interface import BucketInterface
from data_structure.linked_list import DoublyLinkedList
from data_structure.hash_entry import HashEntry
from typing import Any, Optional, Iterator

class LinkedListBucket(BucketInterface):
    def __init__(self):
        self._list = DoublyLinkedList()

    def search(self, key: Any, hash_value: int) -> Optional[HashEntry]:
        node = self._list.find_node(
            lambda e: e.hash_value == hash_value and e.key == key
        )
        return node.data if node else None

    def insert_or_update(self, entry: HashEntry) -> Optional[Any]:
        node = self._list.find_node(
            lambda e: e.hash_value == entry.hash_value and e.key == entry.key
        )
        if node:
            old_val = node.data.value
            node.data.value = entry.value
            return old_val
        
        self._list.insert_back(entry)
        return None

    def delete(self, key: Any, hash_value: int) -> Optional[Any]:
        node = self._list.find_node(
            lambda e: e.hash_value == hash_value and e.key == key
        )
        if not node:
            return None
        removed = self._list.remove_node(node)
        return removed.value

    def __iter__(self) -> Iterator[HashEntry]:
        return iter(self._list)

    def __len__(self) -> int:
        return len(self._list)