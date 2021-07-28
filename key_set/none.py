from key_set.base import KeySet
from key_set.enum import KeySetType


class KeySetNone(KeySet):
    """Represents the NONE sets: ø (empty set)."""

    def key_set_type(self) -> KeySetType:
        """Returns the KeySetType that describes the set."""
        return KeySetType.NONE

    def elements(self) -> set[str]:
        """Returns an empty set."""
        return set()
