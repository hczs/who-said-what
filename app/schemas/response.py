# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     response
   Description :
   Author :       powercheng
   date：          2025/5/20
-------------------------------------------------
   Change Activity:
                   2025/5/20:
-------------------------------------------------
"""
__author__ = 'powercheng'

from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T]

    @classmethod
    def success(cls, data: T) -> "Response[T]":
        return cls(code=200, message="success", data=data)

    @classmethod
    def fail(cls, message: str) -> "Response[None]":
        return cls(code=400, message=message, data=None)
