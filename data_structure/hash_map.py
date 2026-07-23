from typing import Any, Optional
from dataclasses import dataclass
from data_structure.linked_list import ListNode
from data_structure.bucket.hybrid_bucket import HybridBucket
from data_structure.bucket.bucket_interface import BucketInterface
from data_structure.hash_entry import HashEntry

class HashMap:
    capacity: int
    bucket_factory: BucketInterface 
    table: list[BucketInterface]
    _size: int
    load_factor: float
    threshold: int # 확장 임계치 

    def __init__(self, bucket_factory=HybridBucket):
        self.capacity = 16
        self.bucket_factory = bucket_factory
        self.table = [
            self.bucket_factory() for _ in range(self.capacity)
        ]
        self._size = 0
        self.load_factor = 0.75
        self.threshold = int(self.capacity * self.load_factor)
    
    
    def _get_hash(self, key:Any):
        key_str = str(key)

        hash_value = 0

        for char in key_str:
            hash_value = (hash_value << 5) - hash_value + ord(char) # 해시 충돌을 최소화하고 비트를 골고루 분산 # 비트연산으로 32비트 이동 후 빼기 연산을 통해 해시값을 계산 

        return hash_value ^ (hash_value >> 16) # xor

        # 앞선 연산으로 인해 해시 값이 매우 커졌을 때, 정수형의 앞부분(상위 비트)에만 정보가 쏠려있고 뒷부분(하위 비트)은 덜 섞여 있을 수 있습니다. 만약 나중에 버킷 크기로 나머지 연산(% bucket_size)을 하게 되면 상위 비트의 정보가 버려지게 됩니다.       
    
    
    def _get_index(self, hash_value: int):
        return hash_value & (self.capacity - 1) #  정확히 방 개수 범위의 숫자를 남길 수 있음
    

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [self.bucket_factory() for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.load_factor)

        old_size = self._size
        self._size = 0

        for bucket in old_table:
            for entry in bucket:
                idx = self._get_index(entry.hash_value)
                self.table[idx].insert_or_update(entry)
                self._size += 1

        assert self._size == old_size
                


    def put(self, key: Any, value: Any) -> Optional[Any]:
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)
        bucket = self.table[idx]

        entry = HashEntry(key, value, hash_value)
        old_value = bucket.insert_or_update(entry)

        if old_value is None:
            self._size += 1
            if self._size > self.threshold:
                self._resize()

        return old_value

    def get(self, key: Any) -> Any:
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)
        entry = self.table[idx].search(key, hash_value)
        return entry.value if entry else None


    def remove(self, key: Any) -> Any:
        hash_value = self._get_hash(key)
        idx = self._get_index(hash_value)
        removed_value = self.table[idx].delete(key, hash_value)

        if removed_value is not None:
            self._size -= 1

        return removed_value

    def contains(self, key: Any) -> bool:
        return self.get(key) is not None

    def keys(self) -> list[Any]:
        return [entry.key for bucket in self.table for entry in bucket]

    def values(self) -> list[Any]:
        return [entry.value for bucket in self.table for entry in bucket]

    def items(self) -> list[tuple[Any, Any]]:
        return [(entry.key, entry.value) for bucket in self.table for entry in bucket]

    def size(self) -> int:
        return self._size