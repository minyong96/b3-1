import time
from dataclasses import dataclass

from data_structure.hash_map import HashMap
from data_structure.linked_list import DoublyLinkedList
from data_structure.min_heap import MinHeap


@dataclass(frozen=True)
class MemoryInfo:
    used_memory: int
    maxmemory: int
    evicted_keys: int


class MiniRedis:
    """
    자료구조를 조합하여 구현한 인메모리 Key-Value 저장소.

    store:
        key -> value

    lru_list:
        head는 가장 최근 사용된 키,
        tail은 가장 오래 사용되지 않은 키

    lru_nodes:
        key -> LRU 연결 리스트의 ListNode

    ttl_map:
        key -> 현재 유효한 expire_at

    ttl_heap:
        (expire_at, key)를 저장하는 최소 힙
    """

    def __init__(self) -> None:
        # 실제 데이터: key -> value
        self.store = HashMap()

        # LRU 관리
        self.lru_list = DoublyLinkedList()
        self.lru_nodes = HashMap()

        # TTL 관리
        self.ttl_map = HashMap()
        self.ttl_heap = MinHeap()

        # 메모리 관리
        self.maxmemory = 0
        self.used_memory = 0
        self.evicted_keys = 0

    # =========================================================
    # 공통 내부 로직
    # =========================================================

    def _entry_size(self, key: str, value: str) -> int:
        """
        요구사항에서 정의한 메모리 크기를 계산한다.

        len(utf8(key)) + len(utf8(value))
        """
        return len(key.encode("utf-8")) + len(value.encode("utf-8"))

    def _touch_lru(self, key: str) -> None:
        """
        키를 가장 최근에 사용된 상태로 만든다.

        기존 키라면 노드를 head로 이동하고,
        신규 키라면 새로운 노드를 head에 추가한다.
        """
        node = self.lru_nodes.get(key)

        if node is not None:
            self.lru_list.move_to_front(node)
            return

        new_node = self.lru_list.insert_front(key)
        self.lru_nodes.put(key, new_node)

    def _remove_from_lru(self, key: str) -> None:
        """
        lru_nodes와 lru_list에서 키를 함께 제거한다.
        """
        node = self.lru_nodes.remove(key)

        if node is None:
            return

        self.lru_list.remove_node(node)

    def _delete_key(self, key: str) -> bool:
        """
        키를 store, LRU, TTL 구조에서 완전히 제거한다.

        ttl_heap의 중간 원소는 직접 삭제하지 않는다.
        나중에 _purge_expired()에서 stale entry로 판단해 제거한다.
        """
        if not self.store.contains(key):
            return False

        value = self.store.get(key)

        self.used_memory -= self._entry_size(key, value)

        self.store.remove(key)
        self._remove_from_lru(key)
        self.ttl_map.remove(key)

        return True

    def _is_expired(self, key: str) -> bool:
        """
        키가 현재 시각 기준으로 만료되었는지 확인한다.
        """
        expire_at = self.ttl_map.get(key)

        if expire_at is None:
            return False

        return expire_at <= int(time.time())

    def _delete_if_expired(self, key: str) -> bool:
        """
        키가 만료됐다면 삭제하고 True를 반환한다.
        """
        if not self._is_expired(key):
            return False

        self._delete_key(key)
        return True

    def _purge_expired(self) -> None:
        """
        최소 힙을 사용해 현재 만료된 키들을 정리한다.

        EXPIRE 재설정, SET, DEL, LRU eviction으로 인해 힙에 남은
        오래된 엔트리는 ttl_map과 비교하여 무시한다.
        """
        now = int(time.time())

        while self.ttl_heap.size() > 0:
            item = self.ttl_heap.peek()

            if item is None:
                return

            expire_at, key = item

            # 최소 만료 시각도 미래라면 나머지도 모두 미래다.
            if expire_at > now:
                return

            self.ttl_heap.pop()

            current_expire_at = self.ttl_map.get(key)

            # SET, DEL, LRU eviction 등으로 TTL이 사라진 경우
            if current_expire_at is None:
                continue

            # EXPIRE가 다시 설정되어 이전 힙 엔트리가 된 경우
            if current_expire_at != expire_at:
                continue

            self._delete_key(key)

    def _evict_if_needed(self) -> None:
        """
        사용 메모리가 maxmemory를 초과하면 LRU 키부터 제거한다.
        """
        while (
            self.maxmemory > 0
            and self.used_memory > self.maxmemory
        ):
            tail = self.lru_list.tail

            if tail is None:
                return

            lru_key = tail.data
            deleted = self._delete_key(lru_key)

            if not deleted:
                # 자료구조 상태가 비정상적인 경우 무한 반복 방지
                return

            self.evicted_keys += 1

    def _can_store_entry(self, key: str, value: str) -> bool:
        """
        단일 엔트리 자체가 maxmemory 안에 들어갈 수 있는지 검사한다.

        maxmemory가 0이면 무제한이다.
        """
        if self.maxmemory == 0:
            return True

        return self._entry_size(key, value) <= self.maxmemory

    # =========================================================
    # 공개 명령 동작
    # =========================================================

    def set(self, key: str, value: str) -> None:
        """
        key에 value를 저장한다.

        기존 키를 덮어쓰면 기존 TTL은 초기화된다.
        저장 후 메모리를 초과하면 LRU eviction을 수행한다.
        """
        self._delete_if_expired(key)

        if not self._can_store_entry(key, value):
            raise MemoryError(
                "single entry exceeds maxmemory"
            )

        if self.store.contains(key):
            old_value = self.store.get(key)

            self.used_memory -= self._entry_size(key, old_value)

            # SET으로 기존 키를 덮어쓰면 TTL 초기화
            self.ttl_map.remove(key)

        self.store.put(key, value)
        self.used_memory += self._entry_size(key, value)

        self._touch_lru(key)
        self._evict_if_needed()

    def get(self, key: str) -> str | None:
        """
        키의 값을 반환한다.

        키가 없거나 만료된 경우 None을 반환한다.
        조회 성공 시 LRU 순서를 갱신한다.
        """
        if self._delete_if_expired(key):
            return None

        if not self.store.contains(key):
            return None

        value = self.store.get(key)

        self._touch_lru(key)

        return value

    def delete(self, key: str) -> bool:
        """
        키를 삭제한다.

        삭제 성공 시 True, 키가 없으면 False를 반환한다.
        """
        if self._delete_if_expired(key):
            return False

        return self._delete_key(key)

    def exists(self, key: str) -> bool:
        """
        현재 유효한 키가 존재하는지 반환한다.
        """
        if self._delete_if_expired(key):
            return False

        return self.store.contains(key)

    def dbsize(self) -> int:
        """
        만료된 키를 정리한 뒤 전체 키 개수를 반환한다.
        """
        self._purge_expired()
        return self.store.size()

    def keys(self) -> list[str]:
        """
        만료된 키를 정리한 뒤 전체 키 목록을 반환한다.
        """
        self._purge_expired()
        return self.store.keys()

    def expire(self, key: str, seconds: int) -> bool:
        """
        키에 TTL을 설정한다.

        키가 없으면 False를 반환한다.
        seconds가 0 이하이면 즉시 삭제하고 True를 반환한다.
        """
        if self._delete_if_expired(key):
            return False

        if not self.store.contains(key):
            return False

        if seconds <= 0:
            self._delete_key(key)
            return True

        expire_at = int(time.time()) + seconds

        self.ttl_map.put(key, expire_at)
        self.ttl_heap.push((expire_at, key))

        return True

    def ttl(self, key: str) -> int:
        """
        TTL 조회 결과:

        -2: 키가 없거나 이미 만료됨
        -1: 키는 존재하지만 TTL이 없음
         N: 남은 TTL 초
        """
        if self._delete_if_expired(key):
            return -2

        if not self.store.contains(key):
            return -2

        expire_at = self.ttl_map.get(key)

        if expire_at is None:
            return -1

        remaining = expire_at - int(time.time())

        if remaining <= 0:
            self._delete_key(key)
            return -2

        return remaining

    def set_maxmemory(self, maxmemory: int) -> None:
        """
        최대 메모리 제한을 설정한다.

        0은 무제한이다.
        제한을 낮춘 결과 현재 메모리가 초과하면 즉시 LRU 제거한다.
        """
        if maxmemory < 0:
            raise ValueError(
                "maxmemory must be greater than or equal to 0"
            )

        self.maxmemory = maxmemory
        self._evict_if_needed()

    def info_memory(self) -> MemoryInfo:
        """
        현재 메모리 정보를 반환한다.
        """
        self._purge_expired()

        return MemoryInfo(
            used_memory=self.used_memory,
            maxmemory=self.maxmemory,
            evicted_keys=self.evicted_keys,
        )