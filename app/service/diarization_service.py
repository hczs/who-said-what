# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     diarization_service
   Description :
   Author :       powercheng
   date：          2025/5/14
-------------------------------------------------
   Change Activity:
                   2025/5/14:
-------------------------------------------------
"""
__author__ = 'powercheng'

import asyncio

import numpy as np
import sherpa_onnx
from pydantic import BaseModel

from app.core.config import settings
from app.service.embedding_service import embedding_service


class DiarizationResult(BaseModel):
    start: float
    end: float
    duration: float
    speaker: int
    text: str


class DiarizationService:
    def __init__(self) -> None:
        self.diarization_model = None

    def load_model(self, num_speakers: int = -1, cluster_threshold: float = 0.5) -> None:
        segmentation_config = sherpa_onnx.OfflineSpeakerSegmentationModelConfig(
            pyannote=sherpa_onnx.OfflineSpeakerSegmentationPyannoteModelConfig(model=settings.models.segmentation_path)
        )
        cluster_config = sherpa_onnx.FastClusteringConfig(num_clusters=num_speakers, threshold=cluster_threshold)
        diarization_config = sherpa_onnx.OfflineSpeakerDiarizationConfig(segmentation=segmentation_config,
                                                                         embedding=embedding_service.embedding_config,
                                                                         clustering=cluster_config,
                                                                         min_duration_on=0.3,
                                                                         min_duration_off=0.5)
        if not diarization_config.validate():
            raise RuntimeError(
                "Diarization model load config error! Please check your config and make sure all required files exist")
        self.diarization_model = sherpa_onnx.OfflineSpeakerDiarization(diarization_config)

    async def process(self, audio_data: np.ndarray, sample_rate: int) -> list[DiarizationResult]:
        if sample_rate != settings.voice.global_sample_rate:
            raise ValueError(f"Sample rate must be {settings.voice.global_sample_rate}")

        result = await asyncio.to_thread(self.diarization_model.process, audio_data)
        result = result.sort_by_start_time()
        diarization_results = [
            DiarizationResult.model_validate({
                'start': r.start,
                'end': r.end,
                'duration': r.duration,
                'speaker': r.speaker,
                'text': r.text
            }) for r in result
        ]
        return diarization_results


diarization_service = DiarizationService()
