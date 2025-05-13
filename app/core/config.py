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
from pathlib import Path

from pydantic import BaseModel, model_validator

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


class ASRTelespeechCTCConfig(BaseModel):
    model_path: str
    tokens_path: str

    @model_validator(mode="after")
    def resolve_paths(self):
        self.model_path = convert_absolute_path(self.model_path)
        self.tokens_path = convert_absolute_path(self.tokens_path)
        return self


class ASRConfig(BaseModel):
    fireredasr: ASRFireredasrConfig
    telespeechctc: ASRTelespeechCTCConfig


class EmbeddingConfig(BaseModel):
    campplus_path: str
    eres2net_path: str

    @model_validator(mode="after")
    def resolve_paths(self):
        self.campplus_path = convert_absolute_path(self.campplus_path)
        self.eres2net_path = convert_absolute_path(self.eres2net_path)
        return self


class SegmentationConfig(BaseModel):
    pyannote_segmentation_3_0_path: str

    @model_validator(mode="after")
    def resolve_paths(self):
        self.pyannote_segmentation_3_0_path = convert_absolute_path(self.pyannote_segmentation_3_0_path)
        return self


class ModelsConfig(BaseModel):
    asr: ASRConfig
    embedding: EmbeddingConfig
    segmentation: SegmentationConfig


class ProjectConfig(BaseModel):
    log_level: str = "INFO"


class Settings(BaseModel):
    project: ProjectConfig
    voice: VoiceConfig
    models: ModelsConfig


def load_settings(toml_path: str = SETTINGS_CONFIG_PATH) -> Settings:
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    return Settings.model_validate(data)


settings = load_settings()


def main():
    print(settings)


if __name__ == "__main__":
    main()
