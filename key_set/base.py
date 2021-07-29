from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Set, TypeVar, Union

from .enum import KeySetType

TKS = TypeVar('TKS', List[str], Set[str])


class KeySet(ABC):  # Inherit from ABC(Abstract base class)
    """Base class for all KeySets."""

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


class KeySetAll(KeySet):
    """Represents the ALL sets: 𝕌 (the entirety of possible keys)."""

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetAll.."""
        if not isinstance(other, KeySet):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return isinstance(other, KeySetAll)

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

    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        return other.clone()


class KeySetNone(KeySet):
    """Represents the NONE sets: ø (empty set)."""

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetNone..."""
        if not isinstance(other, KeySet):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return isinstance(other, KeySetNone)

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

    def intersect(self, _other: KeySet) -> KeySetNone:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        return self.clone()


class KeySetSome(KeySet):
    """Represents the SOME sets: a concrete set (`A ⊂ 𝕌`)."""

    def __init__(self, elements: TKS):
        """Requires the set of elements of the concrete set."""
        self._elements = set(elements)

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetSome."""
        if not isinstance(other, KeySet):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if not isinstance(other, KeySetSome):
            return False

        return self._elements == other.elements()

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.SOME

    def elements(self) -> set[str]:
        """Returns a copy of the set of the elements of the concrete set."""
        return set(self._elements)

    def represents_some(self) -> bool:
        """Returns true if the set is a SOME KeySet."""
        return True

    def invert(self) -> KeySetAllExceptSome:
        """Returns a new KeySet ALL_EXCEPT_SOME."""
        return KeySetAllExceptSome(self.elements())

    def clone(self) -> KeySetSome:
        """Returns a new KeySet that represents the same Set of this one."""
        return KeySetSome(self.elements())

    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        if other.represents_all():
            return self.clone()
        if other.represents_none():
            return other.clone()
        if other.represents_some():
            els = self._elements.intersection(other.elements())
            return build_some(els)
        if other.represents_all_except_some():
            els = self._elements.difference(other.elements())
            return build_some(els)
        return NotImplemented


class KeySetAllExceptSome(KeySet):
    """Represents the ALL_EXCEPT_SOME sets: the complementary of a concrete set.

    Includes all the elements except the given ones (`A' = {x ∈ 𝕌 | x ∉ A}`).
    """

    def __init__(self, elements: TKS):
        """Requires the set of elements of the concrete set."""
        self._elements = set(elements)

    def __eq__(self, other: Any) -> bool:
        """Returns True if `other` is KeySetAllExceptSome."""
        if not isinstance(other, KeySet):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if not isinstance(other, KeySetAllExceptSome):
            return False

        return self._elements == other.elements()

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.ALL_EXCEPT_SOME

    def elements(self) -> set[str]:
        """Returns a copy of the set of the elements of the concrete set."""
        return set(self._elements)

    def represents_all_except_some(self) -> bool:
        """Returns true if the set is a ALL_EXCEPT_SOME KeySet."""
        return True

    def invert(self) -> KeySetSome:
        """Returns a new KeySet SOME."""
        return KeySetSome(self.elements())

    def clone(self) -> KeySetAllExceptSome:
        """Returns a new KeySet that represents the same Set of this one."""
        return KeySetAllExceptSome(self.elements())

    def intersect(self, other: KeySet) -> KeySet:
        """Returns a new KeySet that represents the intersection (A ∩ B)."""
        if other.represents_all():
            return self.clone()
        if other.represents_none():
            return other.clone()
        if other.represents_some():
            els = other.elements().difference(self._elements)
            return build_some(els)
        if other.represents_all_except_some():
            els = self._elements.union(other.elements())
            return build_all_except_some(els)
        return NotImplemented


TS = Union[KeySetSome, KeySetNone]
TAES = Union[KeySetAllExceptSome, KeySetAll]


def build_some(seq: TKS) -> TS:
    """Returns NONE if seq is blank, or SOME otherwise."""
    if len(seq) > 0:
        return KeySetSome(seq)
    else:
        return KeySetNone()


def build_all_except_some(seq: TKS) -> TAES:
    """Returns ALL if seq is blank, or ALL_EXCEPT_SOME otherwise."""
    if len(seq) > 0:
        return KeySetAllExceptSome(seq)
    else:
        return KeySetAll()
