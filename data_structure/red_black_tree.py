from __future__ import annotations

from enum import Enum
from typing import Any, Iterator, Optional

from data_structure.hash_entry import HashEntry


class Color(Enum):
    RED = 1
    BLACK = 2


class RBNode:
    """
    Red-Black Tree의 노드.

    트리는 hash_value를 기준으로 정렬한다.
    동일한 hash_value를 가진 HashEntry들은 entries 버킷에 함께 저장한다.
    """

    def __init__(
        self,
        entry: Optional[HashEntry] = None,
        color: Color = Color.RED,
    ) -> None:
        self.entries: list[HashEntry] = []

        if entry is not None:
            self.entries.append(entry)

        self.color = color

        # 생성 직후에는 자기 자신을 가리키도록 설정한다.
        # 실제 노드는 RedBlackTree에서 NIL 또는 부모 노드로 다시 연결한다.
        self.left: RBNode = self
        self.right: RBNode = self
        self.parent: RBNode = self

    @property
    def hash_value(self) -> int:
        """
        이 노드가 담당하는 hash_value.

        NIL 노드는 entries가 비어 있으므로 호출하면 안 된다.
        """
        if not self.entries:
            raise ValueError("NIL 노드에는 hash_value가 없습니다.")

        return self.entries[0].hash_value

    def find_entry(self, key: Any) -> Optional[HashEntry]:
        """버킷 안에서 key가 같은 HashEntry를 찾는다."""
        for entry in self.entries:
            if entry.key == key:
                return entry

        return None

    def find_entry_index(self, key: Any) -> Optional[int]:
        """버킷 안에서 key가 같은 HashEntry의 인덱스를 찾는다."""
        for index, entry in enumerate(self.entries):
            if entry.key == key:
                return index

        return None


class RedBlackTree:
    """
    hash_value를 기준으로 정렬하는 Red-Black Tree.

    동일한 hash_value를 가진 서로 다른 key는
    하나의 RBNode.entries 버킷에 저장한다.

    size는 트리 노드 수가 아니라 전체 HashEntry 수를 의미한다.
    """

    def __init__(self) -> None:
        # 모든 리프를 표현하는 공용 Sentinel 노드
        self.NIL = RBNode(color=Color.BLACK)

        # 삭제 fixup에서 NIL.left.color 같은 접근이 가능하도록
        # NIL의 모든 링크는 자기 자신을 가리키게 한다.
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL

        self.root = self.NIL

        # 노드 수가 아니라 HashEntry의 총개수
        self.size = 0

    # =========================================================
    # 회전
    # =========================================================

    def _left_rotate(self, x: RBNode) -> None:
        """
        x를 기준으로 왼쪽 회전한다.

              x                     y
             / \\                   / \\
            A   y        ->        x   C
               / \\                / \\
              B   C              A   B
        """
        y = x.right

        if y == self.NIL:
            raise ValueError("오른쪽 자식이 NIL인 노드는 왼쪽 회전할 수 없습니다.")

        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x: RBNode) -> None:
        """
        x를 기준으로 오른쪽 회전한다.

                x                 y
               / \\               / \\
              y   C     ->       A   x
             / \\                   / \\
            A   B                 B   C
        """
        y = x.left

        if y == self.NIL:
            raise ValueError("왼쪽 자식이 NIL인 노드는 오른쪽 회전할 수 없습니다.")

        x.left = y.right

        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    # =========================================================
    # 탐색
    # =========================================================

    def _find_node(self, hash_value: int) -> RBNode:
        """
        hash_value를 담당하는 노드를 반환한다.

        존재하지 않으면 self.NIL을 반환한다.
        """
        current = self.root

        while current != self.NIL:
            if hash_value == current.hash_value:
                return current

            if hash_value < current.hash_value:
                current = current.left
            else:
                current = current.right

        return self.NIL

    def search(
        self,
        hash_value: int,
        key: Any,
    ) -> Optional[HashEntry]:
        """
        hash_value와 key가 모두 일치하는 HashEntry를 찾는다.

        해시값이 같더라도 key가 다르면 서로 다른 엔트리로 취급한다.
        """
        node = self._find_node(hash_value)

        if node == self.NIL:
            return None

        return node.find_entry(key)

    def contains(
        self,
        hash_value: int,
        key: Any,
    ) -> bool:
        """해당 key가 존재하는지 반환한다."""
        return self.search(hash_value, key) is not None

    # =========================================================
    # 삽입
    # =========================================================

    def insert(self, entry: HashEntry) -> Optional[Any]:
        """
        HashEntry를 삽입한다.

        동일한 hash_value와 key가 이미 존재하면 value만 수정하고
        기존 value를 반환한다.

        새로운 key라면 삽입하고 None을 반환한다.
        """

        # 같은 hash_value를 가진 노드가 이미 존재하는지 확인
        collision_node = self._find_node(entry.hash_value)

        if collision_node != self.NIL:
            existing_entry = collision_node.find_entry(entry.key)

            if existing_entry is not None:
                old_value = existing_entry.value
                existing_entry.value = entry.value
                return old_value

            # 해시값만 같고 key는 다른 해시 충돌
            collision_node.entries.append(entry)
            self.size += 1
            return None

        new_node = RBNode(entry=entry, color=Color.RED)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = self.NIL

        parent = self.NIL
        current = self.root

        while current != self.NIL:
            parent = current

            if new_node.hash_value < current.hash_value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent == self.NIL:
            self.root = new_node
        elif new_node.hash_value < parent.hash_value:
            parent.left = new_node
        else:
            parent.right = new_node

        self.size += 1
        self._insert_fixup(new_node)

        return None

    def _insert_fixup(self, z: RBNode) -> None:
        """
        삽입으로 인해 깨진 Red-Black Tree 속성을 복구한다.
        """
        while z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right

                # Case 1: 부모와 삼촌이 모두 RED
                if uncle.color == Color.RED:
                    z.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    z.parent.parent.color = Color.RED

                    z = z.parent.parent

                else:
                    # Case 2: 삼촌은 BLACK, z는 오른쪽 자식
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)

                    # Case 3: 삼촌은 BLACK, z는 왼쪽 자식
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._right_rotate(z.parent.parent)

            else:
                # 위 로직의 좌우 대칭
                uncle = z.parent.parent.left

                if uncle.color == Color.RED:
                    z.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    z.parent.parent.color = Color.RED

                    z = z.parent.parent

                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)

                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._left_rotate(z.parent.parent)

        self.root.color = Color.BLACK
        self.root.parent = self.NIL

    # =========================================================
    # 삭제
    # =========================================================

    def _transplant(self, u: RBNode, v: RBNode) -> None:
        """
        u가 있던 위치를 v로 대체한다.

        v가 NIL이어도 parent를 설정해야 delete fixup에서
        부모와 형제 노드를 찾을 수 있다.
        """
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def _minimum(self, node: RBNode) -> RBNode:
        """주어진 서브트리에서 hash_value가 가장 작은 노드를 찾는다."""
        if node == self.NIL:
            raise ValueError("NIL 서브트리에서는 최소 노드를 찾을 수 없습니다.")

        current = node

        while current.left != self.NIL:
            current = current.left

        return current

    def delete(
        self,
        hash_value: int,
        key: Any,
    ) -> Optional[Any]:
        """
        hash_value와 key가 일치하는 엔트리를 삭제한다.

        삭제 성공 시 기존 value를 반환하고,
        존재하지 않으면 None을 반환한다.

        주의:
        value 자체로 None을 허용한다면 '없음'과 구분되지 않는다.
        """

        node = self._find_node(hash_value)

        if node == self.NIL:
            return None

        entry_index = node.find_entry_index(key)

        if entry_index is None:
            return None

        removed_entry = node.entries[entry_index]
        removed_value = removed_entry.value

        # 동일 hash_value를 가진 엔트리가 여러 개라면
        # 트리 구조는 그대로 두고 버킷에서만 제거한다.
        if len(node.entries) > 1:
            node.entries.pop(entry_index)
            self.size -= 1
            return removed_value

        # 이 노드에 엔트리가 하나뿐이면 RBNode 자체를 삭제한다.
        self._delete_node(node)
        self.size -= 1

        return removed_value

    def _delete_node(self, z: RBNode) -> None:
        """
        Red-Black Tree에서 RBNode 하나를 구조적으로 삭제한다.
        """
        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)

        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)

        else:
            # z의 중위 후속자
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                # x가 NIL이어도 삭제 보정을 위해 부모 정보가 필요하다.
                x.parent = y

            else:
                self._transplant(y, y.right)

                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)

            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == Color.BLACK:
            self._delete_fixup(x)

        if self.root != self.NIL:
            self.root.parent = self.NIL
            self.root.color = Color.BLACK
        else:
            self.NIL.parent = self.NIL

    def _delete_fixup(self, x: RBNode) -> None:
        """
        BLACK 노드 삭제로 인해 깨진 black-height를 복구한다.
        """
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                sibling = x.parent.right

                # 방어 코드:
                # 정상적인 RB Tree에서는 fixup 중 sibling이 NIL인 상황이
                # 일반적으로 발생하지 않지만, 발생해도 NIL을 RED로 바꾸면 안 된다.
                if sibling == self.NIL:
                    x = x.parent
                    continue

                # Case 1: 형제가 RED
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    x.parent.color = Color.RED

                    self._left_rotate(x.parent)
                    sibling = x.parent.right

                # Case 2: 형제의 두 자식이 모두 BLACK
                if (
                    sibling.left.color == Color.BLACK
                    and sibling.right.color == Color.BLACK
                ):
                    sibling.color = Color.RED
                    x = x.parent

                else:
                    # Case 3: 형제의 가까운 자식은 RED,
                    # 먼 자식은 BLACK
                    if sibling.right.color == Color.BLACK:
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED

                        self._right_rotate(sibling)
                        sibling = x.parent.right

                    # Case 4: 형제의 먼 자식이 RED
                    sibling.color = x.parent.color
                    x.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK

                    self._left_rotate(x.parent)
                    x = self.root

            else:
                # 위 로직의 좌우 대칭
                sibling = x.parent.left

                if sibling == self.NIL:
                    x = x.parent
                    continue

                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    x.parent.color = Color.RED

                    self._right_rotate(x.parent)
                    sibling = x.parent.left

                if (
                    sibling.right.color == Color.BLACK
                    and sibling.left.color == Color.BLACK
                ):
                    sibling.color = Color.RED
                    x = x.parent

                else:
                    if sibling.left.color == Color.BLACK:
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED

                        self._left_rotate(sibling)
                        sibling = x.parent.left

                    sibling.color = x.parent.color
                    x.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK

                    self._right_rotate(x.parent)
                    x = self.root

        x.color = Color.BLACK
        self.NIL.color = Color.BLACK

    # =========================================================
    # 순회
    # =========================================================

    def inorder(self) -> Iterator[HashEntry]:
        """
        hash_value 오름차순으로 모든 HashEntry를 반환한다.

        동일한 hash_value를 가진 엔트리들은
        해당 버킷의 삽입 순서대로 반환한다.
        """

        def _inorder(node: RBNode) -> Iterator[HashEntry]:
            if node == self.NIL:
                return

            yield from _inorder(node.left)

            for entry in node.entries:
                yield entry

            yield from _inorder(node.right)

        yield from _inorder(self.root)

    # =========================================================
    # 검증 및 편의 기능
    # =========================================================

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def validate(self) -> None:
        """
        Red-Black Tree의 핵심 불변식을 검증한다.

        문제가 있으면 AssertionError가 발생한다.
        테스트 코드에서 사용하는 용도다.
        """
        assert self.NIL.color == Color.BLACK, "NIL 노드는 BLACK이어야 합니다."

        if self.root == self.NIL:
            assert self.size == 0, "빈 트리의 size는 0이어야 합니다."
            return

        assert self.root.color == Color.BLACK, "루트는 BLACK이어야 합니다."
        assert self.root.parent == self.NIL, "루트의 부모는 NIL이어야 합니다."

        entry_count = 0

        def validate_node(
            node: RBNode,
            minimum_hash: Optional[int],
            maximum_hash: Optional[int],
        ) -> int:
            nonlocal entry_count

            if node == self.NIL:
                # NIL 노드 하나를 BLACK으로 계산
                return 1

            assert node.entries, "일반 노드의 entries는 비어 있을 수 없습니다."

            node_hash = node.hash_value

            if minimum_hash is not None:
                assert node_hash > minimum_hash, (
                    "왼쪽 서브트리보다 큰 hash_value여야 합니다."
                )

            if maximum_hash is not None:
                assert node_hash < maximum_hash, (
                    "오른쪽 서브트리보다 작은 hash_value여야 합니다."
                )

            for entry in node.entries:
                assert entry.hash_value == node_hash, (
                    "하나의 노드에는 동일한 hash_value만 저장할 수 있습니다."
                )

            entry_count += len(node.entries)

            if node.left != self.NIL:
                assert node.left.parent == node, (
                    "왼쪽 자식의 parent 연결이 잘못되었습니다."
                )

            if node.right != self.NIL:
                assert node.right.parent == node, (
                    "오른쪽 자식의 parent 연결이 잘못되었습니다."
                )

            if node.color == Color.RED:
                assert node.left.color == Color.BLACK, (
                    "RED 노드의 왼쪽 자식은 BLACK이어야 합니다."
                )
                assert node.right.color == Color.BLACK, (
                    "RED 노드의 오른쪽 자식은 BLACK이어야 합니다."
                )

            left_black_height = validate_node(
                node.left,
                minimum_hash,
                node_hash,
            )

            right_black_height = validate_node(
                node.right,
                node_hash,
                maximum_hash,
            )

            assert left_black_height == right_black_height, (
                f"노드 hash={node_hash}의 좌우 black-height가 다릅니다."
            )

            return left_black_height + (
                1 if node.color == Color.BLACK else 0
            )

        validate_node(
            self.root,
            minimum_hash=None,
            maximum_hash=None,
        )

        assert entry_count == self.size, (
            f"실제 엔트리 수 {entry_count}와 size {self.size}가 다릅니다."
        )