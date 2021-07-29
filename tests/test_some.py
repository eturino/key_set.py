# -*- coding: utf-8 -*-
import __future__  # noqa: F401

import key_set  # noqa: F401
from key_set.base import KeySetSome


class TestSome:  # noqa: D101

    def test_represents(self) -> None:
        ks = KeySetSome({'a', 'b'})
        assert ks.represents_some()
        assert not ks.represents_none()
        assert not ks.represents_all()
        assert not ks.represents_all_except_some()

    def test_invert(self) -> None:
        ks = KeySetSome({'a', 'b'})
        actual = ks.invert()
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b'}

    def test_clone(self) -> None:
        ks = KeySetSome({'a', 'b'})
        actual = ks.clone()
        assert actual.represents_some()
        assert actual.elements() == {'a', 'b'}
        assert actual == ks
        assert actual is not ks

    def test_elements(self) -> None:
        ks = KeySetSome({'a', 'b'})
        assert ks.elements() == {'a', 'b'}
