from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, assert_never

from .enum import KeySetType

if TYPE_CHECKING:
    pass


class KeySet(ABC):
    """Base class for all KeySets."""

    __slots__ = ()

    @abstractmethod
    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that defines this class."""
        pass

    @abstractmethod
    def elements(self) -> set[str]:
        """Returns a copy of the set of elements that this KeySet includes.

        It'll return an empty set.
        """
        pass

    @property
    def _elements_internal(self) -> frozenset[str]:
        """Internal access to elements without copy. Override in subclasses."""
        return frozenset()  # pragma: no cover

    def represents_all(self) -> bool:
        """Returns true if the set is a ALL KeySet."""
        return False

    def represents_none(self) -> bool:
        """Returns true if the set is a NONE KeySet."""
        return False

    def represents_some(self) -> bool:
        """Returns true if the set is a SOME KeySet."""
        return False

    def represents_all_except_some(self) -> bool:
        """Returns true if the set is a ALL_EXCEPT_SOME KeySet."""
        return False

    def __contains__(self, item: str) -> bool:
        """Returns True if the set represented by this includes the elem."""
        return self.includes(item)

    @abstractmethod
    def includes(self, _elem: str) -> bool:
        """Returns True if the set represented by this includes the elem."""
        pass

    @abstractmethod
    def invert(self) -> KeySet:
        """Returns a new KeySet that represents the inverse Set of this one.

        All <-> None
        Some <-> AllExceptSome
        """
        pass

    @abstractmethod
    def clone(self) -> KeySet:
        """Returns a new KeySet that represents the same Set of this one."""
        pass

    @abstractmethod
    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        pass

    @abstractmethod
    def union(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the elements of both (A U B)."""
        pass

    @abstractmethod
    def difference(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the diff (A - B)."""
        pass


class KeySetAll(KeySet):
    """Represents the ALL sets: 𝕌 (the entirety of possible keys)."""

    __slots__ = ()
    _compat_len_mode: bool = False

    @classmethod
    def enable_compat_len(cls, enabled: bool = True) -> None:
        """Enable/disable compatibility mode for __len__.

        When enabled, len(KeySetAll()) returns sys.maxsize instead of raising TypeError.
        This is useful for code that expects all objects to support len().

        Args:
            enabled: True for sys.maxsize, False for TypeError (default)
        """
        cls._compat_len_mode = enabled

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetAll.."""
        if not isinstance(other, KeySet):
            return NotImplemented

        return isinstance(other, KeySetAll)

    def __hash__(self) -> int:
        """Returns hash."""
        return hash(KeySetType.ALL)

    def __len__(self) -> int:
        """Return length of the set.

        By default, raises TypeError since KeySetAll represents an infinite set.
        If compat_len_mode is enabled via enable_compat_len(), returns sys.maxsize.
        """
        if KeySetAll._compat_len_mode:
            return sys.maxsize
        raise TypeError("KeySetAll represents an infinite set and has no len()")

    def __str__(self) -> str:
        """Returns str()."""
        return "<KeySetAll>"

    def __repr__(self) -> str:
        """Returns repr()."""
        return "KeySetAll()"

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.ALL

    def elements(self) -> set[str]:
        """Returns an empty set."""
        return set()

    def represents_all(self) -> bool:
        """Returns true if the set is a ALL KeySet."""
        return True

    def invert(self) -> KeySetNone:
        """Returns a new KeySet NONE."""
        return KeySetNone()

    def clone(self) -> KeySetAll:
        """Returns a new KeySet that represents the same Set of this one."""
        return KeySetAll()

    def includes(self, _elem: str) -> bool:
        """Returns True if the set represented by this includes the elem."""
        return True

    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        return other.clone()

    def union(self, _other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the elements of both (A U B)."""
        return self.clone()

    def difference(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the diff (A - B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return KeySetNone()
            case KeySetType.NONE:
                return self.clone()
            case KeySetType.SOME:
                return KeySetAllExceptSome(other._elements_internal)
            case KeySetType.ALL_EXCEPT_SOME:
                return KeySetSome(other._elements_internal)
            case _ as unreachable:
                assert_never(unreachable)


class KeySetNone(KeySet):
    """Represents the NONE sets: ø (empty set)."""

    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetNone..."""
        if not isinstance(other, KeySet):
            return NotImplemented

        return isinstance(other, KeySetNone)

    def __hash__(self) -> int:
        """Returns hash."""
        return hash(KeySetType.NONE)

    def __len__(self) -> int:
        """Returns 0."""
        return 0

    def __str__(self) -> str:
        """Returns str()."""
        return "<KeySetNone>"

    def __repr__(self) -> str:
        """Returns repr()."""
        return "KeySetNone()"

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.NONE

    def elements(self) -> set[str]:
        """Returns an empty set."""
        return set()

    def represents_none(self) -> bool:
        """Returns true if the set is a NONE KeySet."""
        return True

    def invert(self) -> KeySetAll:
        """Returns a new KeySet ALL."""
        return KeySetAll()

    def clone(self) -> KeySetNone:
        """Returns a new KeySet that represents the same Set of this one."""
        return KeySetNone()

    def includes(self, _elem: str) -> bool:
        """Returns True if the set represented by this includes the elem."""
        return False

    def intersect(self, _other: KeySet) -> KeySetNone:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        return self.clone()

    def union(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the elements of both (A U B)."""
        return other.clone()

    def difference(self, _other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the diff (A - B)."""
        return self.clone()


class KeySetSome(KeySet):
    """Represents the SOME sets: a concrete set (`A ⊂ 𝕌`)."""

    __slots__ = ("_elements",)

    def __init__(self, elements: Iterable[str]) -> None:
        """Requires the set of elements of the concrete set."""
        self._elements = frozenset(elements)

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetSome."""
        if not isinstance(other, KeySet):
            return NotImplemented

        if not isinstance(other, KeySetSome):
            return False

        return self._elements == other._elements

    def __hash__(self) -> int:
        """Returns hash."""
        return hash((KeySetType.SOME, self._elements))

    def __len__(self) -> int:
        """Returns the length of the elements in the set."""
        return len(self._elements)

    def __str__(self) -> str:
        """Returns str()."""
        keys = ",".join(sorted(self._elements))
        return f"<KeySetSome ({keys})>"

    def __repr__(self) -> str:
        """Returns repr()."""
        keys = ",".join(f"'{x}'" for x in self._elements)
        return f"KeySetSome([{keys}])"

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.SOME

    def elements(self) -> set[str]:
        """Returns a copy of the set of the elements of the concrete set."""
        return set(self._elements)

    @property
    def _elements_internal(self) -> frozenset[str]:
        """Internal access to elements without copy."""
        return self._elements

    def represents_some(self) -> bool:
        """Returns true if the set is a SOME KeySet."""
        return True

    def invert(self) -> KeySetAllExceptSome:
        """Returns a new KeySet ALL_EXCEPT_SOME."""
        return KeySetAllExceptSome(self._elements)

    def clone(self) -> KeySetSome:
        """Returns a new KeySet that represents the same Set of this one."""
        return KeySetSome(self._elements)

    def includes(self, elem: str) -> bool:
        """Returns True if the set represented by this includes the elem."""
        return elem in self._elements

    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return self.clone()
            case KeySetType.NONE:
                return KeySetNone()
            case KeySetType.SOME:
                elems = self._elements & other._elements_internal
                return build_some_or_none(elems)
            case KeySetType.ALL_EXCEPT_SOME:
                elems = self._elements - other._elements_internal
                return build_some_or_none(elems)
            case _ as unreachable:
                assert_never(unreachable)

    def union(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the elements of both (A U B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return KeySetAll()
            case KeySetType.NONE:
                return self.clone()
            case KeySetType.SOME:
                elems = self._elements | other._elements_internal
                return build_some_or_none(elems)
            case KeySetType.ALL_EXCEPT_SOME:
                elems = other._elements_internal - self._elements
                return build_all_except_some_or_all(elems)
            case _ as unreachable:
                assert_never(unreachable)

    def difference(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the diff (A - B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return KeySetNone()
            case KeySetType.NONE:
                return self.clone()
            case KeySetType.SOME:
                elems = self._elements - other._elements_internal
                return build_some_or_none(elems)
            case KeySetType.ALL_EXCEPT_SOME:
                elems = self._elements & other._elements_internal
                return build_some_or_none(elems)
            case _ as unreachable:
                assert_never(unreachable)


class KeySetAllExceptSome(KeySet):
    """Represents the ALL_EXCEPT_SOME sets: the complementary of a concrete set.

    Includes all the elements except the given ones (`A' = {x ∈ 𝕌 | x ∉ A}`).
    """

    __slots__ = ("_elements",)

    def __init__(self, elements: Iterable[str]) -> None:
        """Requires the set of elements of the concrete set."""
        self._elements = frozenset(elements)

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetAllExceptSome."""
        if not isinstance(other, KeySet):
            return NotImplemented

        if not isinstance(other, KeySetAllExceptSome):
            return False

        return self._elements == other._elements

    def __hash__(self) -> int:
        """Returns hash."""
        return hash((KeySetType.ALL_EXCEPT_SOME, self._elements))

    def __len__(self) -> int:
        """Returns the length of the elements in the exclusion."""
        return len(self._elements)

    def __str__(self) -> str:
        """Returns str()."""
        keys = ",".join(sorted(self._elements))
        return f"<KeySetAllExceptSome ({keys})>"

    def __repr__(self) -> str:
        """Returns repr()."""
        keys = ",".join(f"'{x}'" for x in self._elements)
        return f"KeySetAllExceptSome([{keys}])"

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.ALL_EXCEPT_SOME

    def elements(self) -> set[str]:
        """Returns a copy of the set of the elements of the concrete set."""
        return set(self._elements)

    @property
    def _elements_internal(self) -> frozenset[str]:
        """Internal access to elements without copy."""
        return self._elements

    def represents_all_except_some(self) -> bool:
        """Returns true if the set is a ALL_EXCEPT_SOME KeySet."""
        return True

    def invert(self) -> KeySetSome:
        """Returns a new KeySet SOME."""
        return KeySetSome(self._elements)

    def clone(self) -> KeySetAllExceptSome:
        """Returns a new KeySet that represents the same Set of this one."""
        return KeySetAllExceptSome(self._elements)

    def includes(self, elem: str) -> bool:
        """Returns True if the set represented by this includes the elem."""
        return elem not in self._elements

    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return self.clone()
            case KeySetType.NONE:
                return KeySetNone()
            case KeySetType.SOME:
                elems = other._elements_internal - self._elements
                return build_some_or_none(elems)
            case KeySetType.ALL_EXCEPT_SOME:
                elems = self._elements | other._elements_internal
                return build_all_except_some_or_all(elems)
            case _ as unreachable:
                assert_never(unreachable)

    def union(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the elements of both (A U B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return KeySetAll()
            case KeySetType.NONE:
                return self.clone()
            case KeySetType.SOME:
                elems = self._elements - other._elements_internal
                return build_all_except_some_or_all(elems)
            case KeySetType.ALL_EXCEPT_SOME:
                elems = other._elements_internal & self._elements
                return build_all_except_some_or_all(elems)
            case _ as unreachable:
                assert_never(unreachable)

    def difference(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that contains the diff (A - B)."""
        match other.key_set_type():
            case KeySetType.ALL:
                return KeySetNone()
            case KeySetType.NONE:
                return self.clone()
            case KeySetType.SOME:
                elems = self._elements | other._elements_internal
                return build_all_except_some_or_all(elems)
            case KeySetType.ALL_EXCEPT_SOME:
                elems = other._elements_internal - self._elements
                return build_some_or_none(elems)
            case _ as unreachable:
                assert_never(unreachable)


def build_all() -> KeySetAll:
    """Returns ALL."""
    return KeySetAll()


def build_none() -> KeySetNone:
    """Returns NONE."""
    return KeySetNone()


def build_some_or_none(seq: Iterable[str]) -> KeySetSome | KeySetNone:
    """Returns NONE if seq is blank, or SOME otherwise."""
    elements = frozenset(seq)
    if elements:
        return KeySetSome(elements)
    return KeySetNone()


def build_all_except_some_or_all(seq: Iterable[str]) -> KeySetAllExceptSome | KeySetAll:
    """Returns ALL if seq is blank, or ALL_EXCEPT_SOME otherwise."""
    elements = frozenset(seq)
    if elements:
        return KeySetAllExceptSome(elements)
    return KeySetAll()
