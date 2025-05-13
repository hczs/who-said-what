# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     logging_config
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

import os
import sys

from loguru import logger

from app.core.config import settings, convert_absolute_path

LOG_LEVEL = settings.project.log_level

# 创建日志目录
log_dir = convert_absolute_path("logs")
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)


def init_loguru() -> None:
    logger.remove()

    # 全局日志级别
    logger.level(LOG_LEVEL)

    # 控制台输出配置
    logger.add(sys.stdout, level="INFO",
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> | <level>{message}</level>")

    # 通用的日志配置
    log_config = {
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        "rotation": "00:00",  # 每天午夜切割日志
        "retention": "30 days",  # 保留最近 30 天的日志
        "compression": "zip",  # 日志压缩格式
        "enqueue": True,  # 异步写入日志
        "encoding": "utf-8",  # 文件编码
    }

    # 常规日志（INFO 及以上）
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
        level="INFO",
        **log_config
    )

    # 错误日志（ERROR 及以上）
    logger.add(
        os.path.join(log_dir, "error_{time:YYYY-MM-DD}.log"),
        level="ERROR",
        **log_config
    )

    logger.info("Loguru 初始化完成")
