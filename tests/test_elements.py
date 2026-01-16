import __future__  # noqa: F401

import key_set  # noqa: F401
from key_set.base import KeySetAll, KeySetAllExceptSome, KeySetNone, KeySetSome


class TestElements:  # noqa: D101
    def test_all(self) -> None:
        ks = KeySetAll()
        assert ks.elements() == set()

    def test_none(self) -> None:
        ks = KeySetNone()
        assert ks.elements() == set()

    def test_some(self) -> None:
        ks = KeySetSome({"a", "b"})
        e = ks.elements()
        assert e == {"a", "b"}
        e.add("c")
        assert ks.elements() == {"a", "b"}

    def test_all_except_some(self) -> None:
        ks = KeySetAllExceptSome({"a", "b"})
        e = ks.elements()
        assert e == {"a", "b"}
        e.add("c")
        assert ks.elements() == {"a", "b"}
