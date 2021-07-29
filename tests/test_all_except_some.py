# -*- coding: utf-8 -*-
import __future__  # noqa: F401

from key_set.base import KeySetAll, KeySetAllExceptSome, KeySetNone, KeySetSome


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

    def test_clone(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        actual = ks.clone()
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b'}
        assert actual == ks
        assert actual is not ks

    def test_elements(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        assert ks.elements() == {'a', 'b'}

    def test_intersect_all(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetAll()
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual == ks
        assert actual is not ks

    def test_intersect_none(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetNone()
        actual = ks.intersect(other)
        assert actual.represents_none()
        assert actual == other
        assert actual is not other

    def test_intersect_some_same_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetSome({'a', 'b'})
        actual = ks.intersect(other)
        assert actual.represents_none()

    def test_intersect_some_subset_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetSome({'a'})
        actual = ks.intersect(other)
        assert actual.represents_none()

    def test_intersect_some_superset_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetSome({'a', 'b', 'c'})
        actual = ks.intersect(other)
        assert actual.represents_some()
        assert actual.elements() == {'c'}

    def test_intersect_some_with_some_common_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetSome({'a', 'c'})
        actual = ks.intersect(other)
        assert actual.represents_some()
        assert actual.elements() == {'c'}

    def test_intersect_some_without_common_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetSome({'c', 'd'})
        actual = ks.intersect(other)
        assert actual.represents_some()
        assert actual.elements() == {'c', 'd'}

    def test_intersect_all_except_some_same_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetAllExceptSome({'a', 'b'})
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b'}

    def test_intersect_all_except_some_subset_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetAllExceptSome({'a'})
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b'}

    def test_intersect_all_except_some_superset_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetAllExceptSome({'a', 'b', 'c'})
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b', 'c'}

    def test_intersect_all_except_some_with_some_common_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetAllExceptSome({'a', 'c'})
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b', 'c'}

    def test_intersect_all_except_some_without_common_keys(self) -> None:
        ks = KeySetAllExceptSome({'a', 'b'})
        other = KeySetAllExceptSome({'c', 'd'})
        actual = ks.intersect(other)
        assert actual.represents_all_except_some()
        assert actual.elements() == {'a', 'b', 'c', 'd'}
