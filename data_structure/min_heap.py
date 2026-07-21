from typing import Any, Tuple, Optional

class MinHeap:
    def __init__(self):
        self.heap: list[Tuple[int, Any]] = []

    def size(self) -> int:
        return len(self.heap)

    def peek(self) -> Optional[Tuple[int, Any]]:
        if self.size() == 0:
            return None
        return self.heap[0]

    def push(self, element: Tuple[int, Any]) -> None:
        expire_at, key = element

        if not isinstance(expire_at, int):
            raise TypeError("expire_at은 int 타입이어야 합니다.")

        self.heap.append(element)
        # 부모와 비교하면서 위로 이동
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> Optional[tuple[int, Any]]:
        if self.size() == 0:
            return None

        minimum = self.heap[0]

        if self.size() == 1:
            return self.heap.pop()

        self.heap[0] = self.heap.pop()

        self._heapify_down(0)

        return minimum

    def _heapify_up(self, index: int) -> None:
        while index > 0:
            parent_index = (index - 1) // 2

            if self.heap[parent_index][0] <= self.heap[index][0]:
                break

            self.heap[parent_index], self.heap[index] = (
                self.heap[index],
                self.heap[parent_index],
            )

            index = parent_index

    def _heapify_down(self, index: int) -> None:
        size = self.size()

        while True:
            left = 2 * index + 1   
            right = 2 * index + 2  

            smallest = index 

            # 왼쪽 자식 비교
            if (
                left < size
                and self.heap[left][0] < self.heap[smallest][0]   
            ):
                smallest = left   

            # 오른쪽 자식 비교
            if (
                right < size
                and self.heap[right][0] < self.heap[smallest][0]
            ):
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = (
                self.heap[smallest],
                self.heap[index],
            )

            index = smallest


