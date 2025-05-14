# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_diarization_service
   Description :
   Author :       powercheng
   date：          2025/5/14
-------------------------------------------------
   Change Activity:
                   2025/5/14:
-------------------------------------------------
"""
__author__ = 'powercheng'

import pytest
from app.utils import audio_util
from app.service.diarization_service import diarization_service

@pytest.mark.asyncio
async def test_process():
    samples, sample_rate = audio_util.load_audio("../data/three_person_conversation.wav")
    diarization_service.load_model()
    result = await diarization_service.process(samples, sample_rate)
    assert result is not None and len(result) == 3
