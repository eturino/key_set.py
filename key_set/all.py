from key_set.base import KeySet
from key_set.enum import KeySetType


class KeySetAll(KeySet):
    """Represents the ALL sets: 𝕌 (the entirety of possible keys)."""

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.ALL

    def elements(self) -> set[str]:
        """Returns an empty set."""
        return set()
