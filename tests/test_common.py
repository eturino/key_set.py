"""Tests for common KeySet behaviors: str, hash, equality edge cases."""

from key_set import KeySetAll, KeySetAllExceptSome, KeySetNone, KeySetSome


class TestStr:
    """Test __str__ for all KeySet types."""

    def test_str_all(self) -> None:
        assert str(KeySetAll()) == "<KeySetAll>"

    def test_str_none(self) -> None:
        assert str(KeySetNone()) == "<KeySetNone>"

    def test_str_some(self) -> None:
        result = str(KeySetSome({"a", "b"}))
        assert result.startswith("<KeySetSome (")
        assert result.endswith(")>")

    def test_str_all_except_some(self) -> None:
        result = str(KeySetAllExceptSome({"a", "b"}))
        assert result.startswith("<KeySetAllExceptSome (")
        assert result.endswith(")>")


class TestHash:
    """Test __hash__ for all KeySet types."""

    def test_hash_all(self) -> None:
        ks = KeySetAll()
        assert hash(ks) == hash(KeySetAll())
        # Can be used in sets
        s = {ks, KeySetAll()}
        assert len(s) == 1

    def test_hash_none(self) -> None:
        ks = KeySetNone()
        assert hash(ks) == hash(KeySetNone())
        s = {ks, KeySetNone()}
        assert len(s) == 1

    def test_hash_some(self) -> None:
        ks = KeySetSome({"a", "b"})
        assert hash(ks) == hash(KeySetSome({"a", "b"}))
        s = {ks, KeySetSome({"a", "b"})}
        assert len(s) == 1

    def test_hash_all_except_some(self) -> None:
        ks = KeySetAllExceptSome({"a", "b"})
        assert hash(ks) == hash(KeySetAllExceptSome({"a", "b"}))
        s = {ks, KeySetAllExceptSome({"a", "b"})}
        assert len(s) == 1

    def test_hash_different_types(self) -> None:
        # Different types should have different hashes (usually)
        s = {KeySetAll(), KeySetNone(), KeySetSome({"a"}), KeySetAllExceptSome({"a"})}
        assert len(s) == 4

    def test_usable_as_dict_key(self) -> None:
        d = {
            KeySetAll(): "all",
            KeySetNone(): "none",
            KeySetSome({"a"}): "some",
            KeySetAllExceptSome({"a"}): "all_except_some",
        }
        assert d[KeySetAll()] == "all"
        assert d[KeySetNone()] == "none"
        assert d[KeySetSome({"a"})] == "some"
        assert d[KeySetAllExceptSome({"a"})] == "all_except_some"


class TestEqualityWithNonKeySet:
    """Test __eq__ returns NotImplemented for non-KeySet objects."""

    def test_all_not_equal_to_string(self) -> None:
        assert KeySetAll() != "all"
        assert KeySetAll() != 1
        assert KeySetAll() != None  # noqa: E711
        assert KeySetAll() != {"a"}

    def test_none_not_equal_to_string(self) -> None:
        assert KeySetNone() != "none"
        assert KeySetNone() != 0
        assert KeySetNone() != None  # noqa: E711
        assert KeySetNone() != set()

    def test_some_not_equal_to_set(self) -> None:
        assert KeySetSome({"a", "b"}) != {"a", "b"}
        assert KeySetSome({"a"}) != "a"
        assert KeySetSome({"a"}) != ["a"]

    def test_all_except_some_not_equal_to_set(self) -> None:
        assert KeySetAllExceptSome({"a", "b"}) != {"a", "b"}
        assert KeySetAllExceptSome({"a"}) != "a"


class TestEqualityBetweenDifferentTypes:
    """Test that different KeySet types are not equal to each other."""

    def test_some_not_equal_to_all(self) -> None:
        assert KeySetSome({"a"}) != KeySetAll()

    def test_some_not_equal_to_none(self) -> None:
        assert KeySetSome({"a"}) != KeySetNone()

    def test_some_not_equal_to_all_except_some(self) -> None:
        assert KeySetSome({"a"}) != KeySetAllExceptSome({"a"})

    def test_all_except_some_not_equal_to_all(self) -> None:
        assert KeySetAllExceptSome({"a"}) != KeySetAll()

    def test_all_except_some_not_equal_to_none(self) -> None:
        assert KeySetAllExceptSome({"a"}) != KeySetNone()

    def test_all_except_some_not_equal_to_some(self) -> None:
        assert KeySetAllExceptSome({"a"}) != KeySetSome({"a"})
