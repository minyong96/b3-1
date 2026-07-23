from data_structure.bucket.bucket_interface import BucketInterface
from data_structure.hash_entry import HashEntry
from typing import Any, Optional, Iterator
from data_structure.red_black_tree import RedBlackTree

class RedBlackTreeBucket(BucketInterface):
    def __init__(self):
        self._tree = RedBlackTree() # 직접 구현하신 RBT 클래스

    def search(self, key: Any, hash_value: int) -> Optional[HashEntry]:
        # RBT 내부에서 hash_value 및 key 기반 검색
        return self._tree.search(hash_value, key)

    def insert_or_update(self, entry: HashEntry) -> Optional[Any]:
        # RBT에 삽입 및 밸런싱
        return self._tree.insert(entry)

    def delete(self, key: Any, hash_value: int) -> Optional[Any]:
        # RBT에서 삭제 및 밸런싱
        return self._tree.delete(hash_value, key)

    def __iter__(self) -> Iterator[HashEntry]:
        # 트리 중위 순회(In-order Traversal)로 노드들 yield
        return iter(self._tree.inorder())

    def __len__(self) -> int:
        return self._tree.size