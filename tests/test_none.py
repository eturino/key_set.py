# -*- coding: utf-8 -*-
import __future__  # noqa: F401

from key_set.base import KeySetAll, KeySetAllExceptSome, KeySetNone, KeySetSome


class TestNone:  # noqa: D101

    def test_represents(self) -> None:
        ks = KeySetNone()
        assert ks.represents_none()
        assert not ks.represents_all()
        assert not ks.represents_some()
        assert not ks.represents_all_except_some()

    def test_invert(self) -> None:
        ks = KeySetNone()
        actual = ks.invert()
        assert actual.represents_all()

    def test_clone(self) -> None:
        ks = KeySetNone()
        actual = ks.clone()
        assert actual.represents_none()
        assert actual == ks
        assert actual is not ks

    def test_elements(self) -> None:
        ks = KeySetNone()
        assert ks.elements() == set()

    def test_intersect_all(self) -> None:
        ks = KeySetNone()
        other = KeySetAll()
        actual = ks.intersect(other)
        assert actual.represents_none()
        assert actual == ks
        assert actual is not ks

    def test_intersect_none(self) -> None:
        ks = KeySetNone()
        other = KeySetNone()
        actual = ks.intersect(other)
        assert actual.represents_none()
        assert actual == ks
        assert actual is not ks

    def test_intersect_some(self) -> None:
        ks = KeySetNone()
        other = KeySetSome({'a', 'b'})
        actual = ks.intersect(other)
        assert actual.represents_none()
        assert actual == ks
        assert actual is not ks

    def test_intersect_all_except_some(self) -> None:
        ks = KeySetNone()
        other = KeySetAllExceptSome({'a', 'b'})
        actual = ks.intersect(other)
        assert actual.represents_none()
        assert actual == ks
        assert actual is not ks

    def test_includes(self) -> None:
        ks = KeySetNone()
        assert not ks.includes('a')
