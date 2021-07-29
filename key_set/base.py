from abc import ABC, abstractmethod

# abc is a builtin module, we have to import ABC and abstractmethod
from key_set.enum import KeySetType


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