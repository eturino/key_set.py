from key_set.base import KeySet
from key_set.enum import KeySetType
from key_set.some import KeySetSome


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
