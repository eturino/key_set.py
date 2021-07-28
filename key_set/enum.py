from enum import Enum


class KeySetType(Enum):
    ALL = 'ALL'
    ALL_EXCEPT_SOME = 'ALL_EXCEPT_SOME'
    NONE = 'NONE'
    SOME = 'SOME'
