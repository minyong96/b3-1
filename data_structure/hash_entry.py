from typing import Any
from dataclasses import dataclass


@dataclass
class HashEntry:
    key: Any
    value: Any
    hash_value: int

    def __lt__(self, other: "HashEntry") -> bool:
        # 1차 비교: hash_value
        if self.hash_value != other.hash_value:
            return self.hash_value < other.hash_value
        
        # 2차 비교 (해시 충돌 시): key 비교 시도
        try:
            return self.key < other.key
        except TypeError:
            # key끼리 비교 불가능한 타입일 경우(예: int와 str 혼용 등) id 값으로 비교
            return id(self.key) < id(other.key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashEntry):
            return False
        return self.hash_value == other.hash_value and self.key == other.key
