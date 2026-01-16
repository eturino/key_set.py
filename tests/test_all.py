import __future__  # noqa: F401

import pytest

from key_set.base import KeySetAll, KeySetAllExceptSome, KeySetNone, KeySetSome


class TestAll:  # noqa: D101
    def test_represents(self) -> None:
        ks = KeySetAll()
        assert ks.represents_all()
        assert not ks.represents_none()
        assert not ks.represents_some()
        assert not ks.represents_all_except_some()

    def test_invert(self) -> None:
        ks = KeySetAll()
        actual = ks.invert()
        assert actual.represents_none()

    def test_clone(self) -> None:
        ks = KeySetAll()
        actual = ks.clone()
        assert actual.represents_all()
        assert actual == ks
        assert actual is not ks

    def test_repr(self) -> None:
        ks = KeySetAll()
        actual = eval(repr(ks))
        assert actual.represents_all()
        assert actual == ks
        assert actual is not ks

    def test_elements(self) -> None:
        ks = KeySetAll()
        assert ks.elements() == set()

    def test_intersect_all(self) -> None:
        ks = KeySetAll()
        other = KeySetAll()
        actual = ks.intersect(other)
        assert actual.represents_all()

    def test_intersect_none(self) -> None:
        ks = KeySetAll()
        other = KeySetNone()
        actual = ks.intersect(other)
        assert actual.represents_none()

    def test_intersect_some(self) -> None:
        ks = KeySetAll()
        other = KeySetSome({"a", "b"})
        actual = ks.intersect(other)
        assert actual.represents_some()
        assert actual.elements() == {"a", "b"}
        assert actual == other
        assert actual is not other

    def test_intersect_all_except_some(self) -> None:
        ks = KeySetAll()
        other = KeySetAllExceptSome({"a", "b"})
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {"a", "b"}
        assert actual == other
        assert actual is not other

    def test_includes(self) -> None:
        ks = KeySetAll()
        assert ks.includes("a")
        assert "a" in ks

    def test_len(self) -> None:
        ks = KeySetAll()
        with pytest.raises(TypeError, match="infinite set"):
            len(ks)

    def test_len_compat_mode(self) -> None:
        import sys

        ks = KeySetAll()
        # Enable compat mode
        KeySetAll.enable_compat_len(True)
        try:
            assert len(ks) == sys.maxsize
        finally:
            # Restore default behavior
            KeySetAll.enable_compat_len(False)

        # Verify it's back to raising
        with pytest.raises(TypeError, match="infinite set"):
            len(ks)

    def test_union_all(self) -> None:
        ks = KeySetAll()
        other = KeySetAll()
        actual = ks.union(other)
        assert actual.represents_all()

    def test_union_none(self) -> None:
        ks = KeySetAll()
        other = KeySetNone()
        actual = ks.union(other)
        assert actual.represents_all()

    def test_union_some(self) -> None:
        ks = KeySetAll()
        other = KeySetSome({"a", "b"})
        actual = ks.union(other)
        assert actual.represents_all()

    def test_union_all_except_some(self) -> None:
        ks = KeySetAll()
        other = KeySetAllExceptSome({"a", "b"})
        actual = ks.union(other)
        assert actual.represents_all()

    def test_remove_all(self) -> None:
        ks = KeySetAll()
        other = KeySetAll()
        actual = ks.difference(other)
        assert actual.represents_none()

    def test_remove_none(self) -> None:
        ks = KeySetAll()
        other = KeySetNone()
        actual = ks.difference(other)
        assert actual.represents_all()

    def test_remove_some(self) -> None:
        ks = KeySetAll()
        other = KeySetSome({"a", "b"})
        actual = ks.difference(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {"a", "b"}

    def test_remove_all_except_some(self) -> None:
        ks = KeySetAll()
        other = KeySetAllExceptSome({"a", "b"})
        actual = ks.difference(other)
        assert actual.represents_some()
        assert actual.elements() == {"a", "b"}
