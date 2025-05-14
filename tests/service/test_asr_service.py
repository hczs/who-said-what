# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_asr_service
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

from app.service.asr_service import asr_service
from app.utils import audio_util

@pytest.fixture(scope="module", autouse=True)
def load_model():
    asr_service.load_model()

@pytest.mark.asyncio
async def test_asr_wav():
    samples, _ = audio_util.load_audio("../data/three_person_conversation.wav")
    emotion, text = await asr_service.asr_wav(samples)
    assert text is not None