# `key_set`

Python port of [KeySet in TypeScript](https://github.com/eturino/ts-key-set) and [KeySet in Ruby](https://github.com/eturino/ruby_key_set)

TBD

## Limitations

- for now, only KeySet of strings
- no ComposedKeySet yet

## `KeySetType` enum

Enum that represents the 4 types of KeySets:

- `ALL` represents the entirety of possible keys (`𝕌`)
- `NONE` represents an empty set (`∅`)
- `SOME` represents a concrete set (`A ⊂ 𝕌`)
- `ALL_EXCEPT_SOME` represents the complementary of a set, all the elements except the given ones (`A' = {x ∈ 𝕌 | x ∉ A}`) _(see [Complement in Wikipedia](https://en.wikipedia.org/wiki/Complement_set_theory))*

## `KeySet` classes

Methods exposed:

### `key_set_type`

returns the `KeySetType` enum

### `elements`

returns the set with the elements. It will be blank for `All` and `None`.
