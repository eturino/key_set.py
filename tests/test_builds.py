
# -*- coding: utf-8 -*-
import __future__  # noqa: F401

from typing import List

import key_set  # noqa: F401
from key_set.base import build_all_except_some, build_some


class TestBuilds:  # noqa: D101

    def test_build_some_with_blank(self) -> None:
        keys: List[str] = []
        actual = build_some(keys)
        assert actual.represents_none()

    def test_build_some_with_elements(self) -> None:
        actual = build_some(['A'])
        assert actual.represents_some()
        assert actual.elements() == {'A'}

    def test_build_all_except_some_with_blank(self) -> None:
        keys: List[str] = []
        actual = build_all_except_some(keys)
        assert actual.represents_all()

    def test_build_all_except_some_with_elements(self) -> None:
        actual = build_all_except_some(['A'])
        assert actual.represents_all_except_some()
        assert actual.elements() == {'A'}
