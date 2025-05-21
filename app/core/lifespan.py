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

import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.core.loguru_config import init_loguru
from app.service.asr_service import asr_service
from app.service.diarization_service import diarization_service
from app.service.embedding_service import embedding_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = time.time()
    # 日志初始化
    init_loguru(),
    await asyncio.gather(
        # 模型加载
        asyncio.to_thread(asr_service.load_model),
        asyncio.to_thread(diarization_service.load_model),
        asyncio.to_thread(embedding_service.load_model),
    )
    cost_time = time.time() - start_time
    logger.info(f'App init completed, cost {cost_time:.4}s')
    yield
