# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     example
   Description :
   Author :       powercheng
   date：          2025/5/20
-------------------------------------------------
   Change Activity:
                   2025/5/20:
-------------------------------------------------
"""
__author__ = 'powercheng'

from pydantic import BaseModel


class ExampleResponse(BaseModel):
    id: int
    message: str
