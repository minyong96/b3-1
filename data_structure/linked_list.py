from dataclasses import dataclass
from typing import Any, Iterator, Callable


class ListNode:
    def __init__(self, data: Any):
        self.prev: "ListNode | None" = None
        self.next: "ListNode | None" = None
        self.data: Any = data


class DoublyLinkedList:
    def __init__(self):
        self.head: ListNode | None = None
        self.tail: ListNode | None = None
        self._size = 0

    def insert_front(self, data: Any) -> ListNode:
        new_node = ListNode(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self._size += 1
        return new_node

    def insert_back(self, data: Any) -> ListNode:
        new_node = ListNode(data)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1
        return new_node

    def remove_front(self) -> Any:
        if self.head is None:
            return None

        return self.remove_node(self.head)

    def remove_back(self) -> Any:
        if self.tail is None:
            return None

        return self.remove_node(self.tail)

    def remove_node(self, node: ListNode) -> Any:
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        removed_data = node.data

        node.prev = None
        node.next = None

        self._size -= 1
        return removed_data

    def move_to_front(self, node: ListNode) -> None:
        if node is self.head:
            return

        if node.prev is not None:
            node.prev.next = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = self.head

        if self.head is not None:
            self.head.prev = node

        self.head = node

        if self.tail is None:
            self.tail = node

    def find_node(self, predicate: Callable[[Any], bool]) -> ListNode | None:
        current = self.head

        while current is not None:
            if predicate(current.data):
                return current

            current = current.next

        return None

    def size(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head

        while current is not None:
            yield current.data
            current = current.next