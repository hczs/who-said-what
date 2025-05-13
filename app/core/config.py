# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

import tomllib
from functools import cached_property
from pathlib import Path
from typing import Any, Union

from loguru import logger
from pydantic import BaseModel, model_validator

from app.enums.model_enum import AsrEnum

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]


def convert_absolute_path(relative_path: str) -> str:
    return str(PROJECT_ROOT.joinpath(relative_path))


SETTINGS_CONFIG_PATH = convert_absolute_path("config/settings.toml")


class VoiceConfig(BaseModel):
    global_sample_rate: int = 16000


class ASRFireredasrConfig(BaseModel):
    encoder_path: str
    decoder_path: str
    tokens_path: str

    @model_validator(mode="after")
    def resolve_paths(self):
        self.encoder_path = convert_absolute_path(self.encoder_path)
        self.decoder_path = convert_absolute_path(self.decoder_path)
        self.tokens_path = convert_absolute_path(self.tokens_path)
        return self


class ASRSenseVoiceConfig(BaseModel):
    model_path: str
    tokens_path: str

    @model_validator(mode="after")
    def resolve_paths(self):
        self.model_path = convert_absolute_path(self.model_path)
        self.tokens_path = convert_absolute_path(self.tokens_path)
        return self


class ASRConfig(BaseModel):
    fireredasr: ASRFireredasrConfig
    sensevoice: ASRSenseVoiceConfig


class ModelsConfig(BaseModel):
    asr: str
    embedding_path: str
    segmentation_path: str
    asr_config: dict[str, Any]

    @model_validator(mode="after")
    def resolve_paths(self):
        self.embedding_path = convert_absolute_path(self.embedding_path)
        self.segmentation_path = convert_absolute_path(self.segmentation_path)
        return self

    @cached_property
    def fireredasr(self) -> ASRFireredasrConfig:
        asr_type = AsrEnum.from_string(settings.models.asr)
        if asr_type == AsrEnum.FIRE_RED_ASR:
            return ASRFireredasrConfig.model_validate(self.asr_config.get("fireredasr"))
        else:
            logger.error(f"Please config the [asr.fireredasr] in {SETTINGS_CONFIG_PATH}")
            raise ValueError(f"Please config the [asr.fireredasr] in {SETTINGS_CONFIG_PATH}")

    @cached_property
    def sensevoice(self) -> ASRSenseVoiceConfig:
        asr_type = AsrEnum.from_string(settings.models.asr)
        if asr_type == AsrEnum.SENSE_VOICE:
            return ASRSenseVoiceConfig.model_validate(self.asr_config.get("sensevoice"))
        else:
            raise ValueError(f"Please config the [asr.sensevoice] in {SETTINGS_CONFIG_PATH}")


class ProjectConfig(BaseModel):
    log_level: str = "INFO"


class Settings(BaseModel):
    project: ProjectConfig
    voice: VoiceConfig
    models: ModelsConfig


def load_settings(toml_path: str = SETTINGS_CONFIG_PATH) -> Settings:
    """
    加载项目toml配置文件，返回封装好的settings对象和原始的配置文件字典

    :param toml_path: 项目配置文件路径
    :return: settings 对象，原始配置文件字典
    """
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)
    # 注入 asr 配置
    data["models"]["asr_config"] = data.get("asr", {})
    return Settings.model_validate(data)


settings = load_settings()

if __name__ == '__main__':
    print(settings)