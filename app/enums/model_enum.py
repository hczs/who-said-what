# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     model_enum
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

from enum import Enum
from typing import Optional


class AsrEnum(Enum):
    FIRE_RED_ASR = 'fireredasr'
    SENSE_VOICE = 'sensevoice'

    @classmethod
    def from_string(cls, value: str) -> Optional["AsrEnum"]:
        value_lower = value.lower()
        for member in cls:
            if member.value == value_lower:
                return member
        return None

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]


if __name__ == '__main__':
    print([member.value for member in AsrEnum])