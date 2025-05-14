# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     asr_service
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
from app.enums.model_enum import AsrEnum


class AsrService:
    def __init__(self):
        self.asr_type: AsrEnum = AsrEnum.from_string(settings.models.asr)
        self.recognizer = None

    def load_model(self) -> None:
        if self.recognizer is not None:
            logger.warning("asr model has been loaded")
            return
        # load asr model
        if self.asr_type == AsrEnum.FIRE_RED_ASR:
            self.recognizer = sherpa_onnx.OfflineRecognizer.from_fire_red_asr(
                decoder=settings.models.fireredasr.decoder_path,
                encoder=settings.models.fireredasr.encoder_path,
                tokens=settings.models.fireredasr.tokens_path,
            )
        elif self.asr_type == AsrEnum.SENSE_VOICE:
            self.recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
                model=settings.models.sensevoice.model_path,
                tokens=settings.models.sensevoice.tokens_path,
                sample_rate=settings.voice.global_sample_rate
            )
        else:
            raise ValueError(f"asr_type must be in {AsrEnum.values()}, current is {self.asr_type.value}")
        logger.info(f"load asr model success, asr_type: {self.asr_type.value}")

    def asr_wav_sync(self, wav_data: np.ndarray) -> tuple[str, str]:
        """
        wav 文件数据识别（同步）

        :param wav_data: wav数据段
        :return: 文本情绪（生气（ANGRY）、高兴（HAPPY）、伤心（SAD）和中性（NEUTRAL）），文本内容
        """
        asr_stream = self.recognizer.create_stream()
        asr_stream.accept_waveform(sample_rate=settings.voice.global_sample_rate, waveform=wav_data)
        self.recognizer.decode_stream(asr_stream)
        result = asr_stream.result
        return result.emotion, result.text

    async def asr_wav(self, wav_data: np.ndarray) -> tuple[str, str]:
        """
        wav 文件数据识别

        :param wav_data: wav数据段
        :return: 文本情绪（生气（ANGRY）、高兴（HAPPY）、伤心（SAD）和中性（NEUTRAL）），文本内容
        """
        return await asyncio.to_thread(self.asr_wav_sync, wav_data)


asr_service = AsrService()
