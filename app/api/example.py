# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     example
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

from fastapi import APIRouter

from app.schemas.example import ExampleResponse
from app.schemas.response import Response

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/", response_model=Response[ExampleResponse])
async def test_example():
    return Response.success(data=ExampleResponse(id=1, message="hello"))