# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     embedding_service
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

import numpy as np
import sherpa_onnx
from loguru import logger

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.embedding_config = sherpa_onnx.SpeakerEmbeddingExtractorConfig(model=settings.models.embedding_path)
        self.embedding_model = None

    def load_model(self) -> None:
        if self.embedding_model is not None:
            logger.warning("embedding model has been loaded")
            return
        self.embedding_model = sherpa_onnx.SpeakerEmbeddingExtractor(self.embedding_config)
        logger.info("load embedding model success!")

    def compute_sync(self, audio_segment: np.ndarray) -> list[float]:
        stream = self.embedding_model.create_stream()
        stream.accept_waveform(sample_rate=settings.voice.global_sample_rate, waveform=audio_segment)
        stream.input_finished()
        assert self.embedding_model.is_ready(stream)
        return self.embedding_model.compute(stream)

    async def compute(self, audio_segment: np.ndarray) -> list[float]:
        return await asyncio.to_thread(self.compute_sync, audio_segment)


embedding_service = EmbeddingService()
