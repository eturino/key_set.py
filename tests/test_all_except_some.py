# -*- coding: utf-8 -*-
import __future__  # noqa: F401

from key_set.base import KeySetAllExceptSome


class TestAllExceptSome:  # noqa: D101

    def test_represents(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        assert ks.represents_all_except_some()
        assert not ks.represents_none()
        assert not ks.represents_all()
        assert not ks.represents_some()

    def test_invert(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        actual = ks.invert()
        assert actual.represents_some()
        assert actual.elements() == {'a', 'b'}

    def test_elements(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        assert ks.elements() == {'a', 'b'}
