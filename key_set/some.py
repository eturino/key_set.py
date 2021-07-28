from key_set.base import KeySet
from key_set.enum import KeySetType


class KeySetSome(KeySet):
    """Represents the SOME sets: a concrete set (`A ⊂ 𝕌`)."""

    def __init__(self, elements: set[str]):
        """Requires the set of elements of the concrete set."""
        self._elements = elements

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.SOME

    def elements(self) -> set[str]:
        """Returns a copy of the set of the elements of the concrete set."""
        return set(self._elements)
