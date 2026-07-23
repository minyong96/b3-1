from abc import ABC, abstractmethod
from typing import Any, Optional, Iterator, Tuple
from data_structure.hash_entry import HashEntry

class BucketInterface(ABC):
    @abstractmethod
    def search(self, key: Any, hash_value: int) -> Optional[HashEntry]:
        """해시값과 key가 일치하는 Entry 조회"""
        pass

    @abstractmethod
    def insert_or_update(self, entry: HashEntry) -> Optional[Any]:
        """Entry 삽입. 기존 키 존재 시 value 업데이트 후 old_value 반환"""
        pass

    @abstractmethod
    def delete(self, key: Any, hash_value: int) -> Optional[Any]:
        """Entry 삭제 후 removed value 반환"""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[HashEntry]:
        """버킷 내 모든 HashEntry 순회 (keys, values, items, resize용)"""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """버킷 내 노드 개수"""
        pass