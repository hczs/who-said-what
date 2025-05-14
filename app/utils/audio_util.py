# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     audio_util
   Description :
   Author :       powercheng
   date：          2025/5/14
-------------------------------------------------
   Change Activity:
                   2025/5/14:
-------------------------------------------------
"""
__author__ = 'powercheng'

import numpy as np
import librosa
from loguru import logger

from app.core.config import settings
import soundfile as sf


def load_audio(filename: str) -> tuple[np.ndarray, int]:
    """加载音频文件，只取第一个通道的数据，自动进行重采样至配置的全局采样率

    Args:
        filename (str): 文件路径

    Returns:
        tuple[np.ndarray, int]: samples, sample_rate
    """
    data, sample_rate = sf.read(
        filename,
        always_2d=True,
        dtype="float32",
    )
    # use only the first channel
    data = data[:, 0]
    samples = np.ascontiguousarray(data)

    # 如果音频采样率不是16000，进行重采样
    global_sample_rate = settings.voice.global_sample_rate
    if sample_rate != global_sample_rate:
        audio_resampled = librosa.resample(data, orig_sr=sample_rate, target_sr=global_sample_rate)
        logger.info(f"Resampling {filename} from {sample_rate} to {global_sample_rate}")
        return audio_resampled, global_sample_rate
    return samples, sample_rate
