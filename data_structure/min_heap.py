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
        # 1. 배열 끝에 추가
        # 2. _heapify_up 호출
        pass

    def pop(self) -> Optional[Tuple[int, Any]]:
        # 1. 예외 처리 (빈 경우, 1개인 경우)
        # 2. 루트 백업 후 맨 끝 원소를 루트로 이동
        # 3. _heapify_down 호출
        pass

    def _heapify_up(self, index: int) -> None:
        # 부모 인덱스: (index - 1) // 2
        pass

    def _heapify_down(self, index: int) -> None:
        # 왼쪽 자식: 2 * index + 1
        # 오른쪽 자식: 2 * index + 2
        pass