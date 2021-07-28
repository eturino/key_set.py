from abc import ABC, abstractmethod

# abc is a builtin module, we have to import ABC and abstractmethod
from key_set.enum import KeySetType


class KeySet(ABC):  # Inherit from ABC(Abstract base class)
    """Base class for all KeySets."""

    @abstractmethod  # Decorator to define an abstract method
    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that defines this class."""
        pass

    @abstractmethod  # Decorator to define an abstract method
    def elements(self) -> set[str]:
        """Returns a copy of the set of elements that this KeySet includes.

        It'll return an empty set.
        """
        pass
