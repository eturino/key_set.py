import __future__  # noqa: F401

from key_set import (
    build_all,
    build_all_except_some_or_all,
    build_none,
    build_some_or_none,
)


class TestBuilds:  # noqa: D101
    def test_build_all(self) -> None:
        actual = build_all()
        assert actual.represents_all()

    def test_build_none(self) -> None:
        actual = build_none()
        assert actual.represents_none()

    def test_build_some_with_blank(self) -> None:
        keys: list[str] = []
        actual = build_some_or_none(keys)
        assert actual.represents_none()

    def test_build_some_with_elements(self) -> None:
        actual = build_some_or_none(["A"])
        assert actual.represents_some()
        assert actual.elements() == {"A"}

    def test_build_all_except_some_with_blank(self) -> None:
        keys: list[str] = []
        actual = build_all_except_some_or_all(keys)
        assert actual.represents_all()

    def test_build_all_except_some_with_elements(self) -> None:
        actual = build_all_except_some_or_all(["A"])
        assert actual.represents_all_except_some()
        assert actual.elements() == {"A"}
