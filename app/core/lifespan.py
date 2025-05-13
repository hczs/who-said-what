# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     lifespan
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.core.loguru_config import init_loguru


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 日志初始化
    start_time = time.time()
    init_loguru()
    cost_time = time.time() - start_time
    logger.info(f'App init completed, cost {cost_time:.4}s')
    yield
