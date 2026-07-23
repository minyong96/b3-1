from data_structure.bucket.bucket_interface import BucketInterface
from data_structure.bucket.linked_list_bucket import LinkedListBucket
from data_structure.bucket.red_black_tree_bucket import RedBlackTreeBucket
from data_structure.hash_entry import HashEntry
from typing import Any, Optional, Iterator


class HybridBucket(BucketInterface):
    TREEIFY_THRESHOLD = 8
    UNTREEIFY_THRESHOLD = 6

    def __init__(self):
        # 기본 상태: 연결 리스트로 출발
        self._delegate: BucketInterface = LinkedListBucket()
        self._is_tree = False

    def _treeify(self) -> None:
        """LinkedList -> RedBlackTree 승격"""
        tree_bucket = RedBlackTreeBucket()
        for entry in self._delegate:
            tree_bucket.insert_or_update(entry)
        
        self._delegate = tree_bucket
        self._is_tree = True

    def _untreeify(self) -> None:
        """RedBlackTree -> LinkedList 원복"""
        list_bucket = LinkedListBucket()
        for entry in self._delegate:
            list_bucket.insert_or_update(entry)
            
        self._delegate = list_bucket
        self._is_tree = False

    def search(self, key: Any, hash_value: int) -> Optional[HashEntry]:
        return self._delegate.search(key, hash_value)

    def insert_or_update(self, entry: HashEntry) -> Optional[Any]:
        old_val = self._delegate.insert_or_update(entry)
        
        # 신규 삽입이고, 연결 리스트 상태에서 8개를 넘어서면 RBT로 전환
        if old_val is None and not self._is_tree:
            if len(self._delegate) >= self.TREEIFY_THRESHOLD:
                self._treeify()

        return old_val

    def delete(self, key: Any, hash_value: int) -> Optional[Any]:
        removed_val = self._delegate.delete(key, hash_value)

        # 삭제가 일어났고, RBT 상태에서 6개 이하로 줄어들면 다시 연결 리스트로 전환
        if removed_val is not None and self._is_tree:
            if len(self._delegate) <= self.UNTREEIFY_THRESHOLD:
                self._untreeify()

        return removed_val

    def __iter__(self) -> Iterator[HashEntry]:
        return iter(self._delegate)

    def __len__(self) -> int:
        return len(self._delegate)