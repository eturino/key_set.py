from __future__ import annotations

from abc import ABC, abstractmethod

# abc is a builtin module, we have to import ABC and abstractmethod
from .enum import KeySetType


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
    def invert(self):
        """Returns a new KeySet that represents the inverse Set of this one.

        All <-> None
        Some <-> AllExceptSome
        """
        pass


class KeySetAll(KeySet):
    """Represents the ALL sets: 𝕌 (the entirety of possible keys)."""

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


class KeySetNone(KeySet):
    """Represents the NONE sets: ø (empty set)."""

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


class KeySetSome(KeySet):
    """Represents the SOME sets: a concrete set (`A ⊂ 𝕌`)."""

    def __init__(self, elements: set[str]):
        """Requires the set of elements of the concrete set."""
        self._elements = set(elements)

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


class KeySetAllExceptSome(KeySet):
    """Represents the ALL_EXCEPT_SOME sets: the complementary of a concrete set.

    Includes all the elements except the given ones (`A' = {x ∈ 𝕌 | x ∉ A}`).
    """

    def __init__(self, elements: set[str]):
        """Requires the set of elements of the concrete set."""
        self._elements = set(elements)

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
