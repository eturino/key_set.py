import __future__  # noqa: F401

import key_set  # noqa: F401
from key_set.enum import KeySetType


class TestEnum:  # noqa: D101
    def test_all(self) -> None:
        assert KeySetType.ALL.value == "ALL"

    def test_none(self) -> None:
        assert KeySetType.NONE.value == "NONE"

    def test_some(self) -> None:
        assert KeySetType.SOME.value == "SOME"

    def test_all_except_some(self) -> None:
        assert KeySetType.ALL_EXCEPT_SOME.value == "ALL_EXCEPT_SOME"
