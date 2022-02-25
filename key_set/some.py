from key_set.all_except_some import KeySetAllExceptSome
from key_set.base import KeySet
from key_set.enum import KeySetType


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
