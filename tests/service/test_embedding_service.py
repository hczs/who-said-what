# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_embedding_service
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

from app.service.embedding_service import embedding_service
from app.utils import audio_util


@pytest.fixture(scope="module", autouse=True)
def load_model():
    embedding_service.load_model()

@pytest.mark.asyncio
async def test_embedding_compute():
    samples, _ = audio_util.load_audio("../data/three_person_conversation.wav")
    embeddings = await embedding_service.compute(samples)
    assert embeddings is not None