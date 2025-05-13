# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

import importlib
import pkgutil

from fastapi import FastAPI

from app.api import example
from app.core.lifespan import lifespan
from app.core.middleware import log_request_middleware

app = FastAPI(lifespan=lifespan)

# 添加请求日志中间件
app.middleware("http")(log_request_middleware)

app.include_router(example.router)

# 动态导入 app.api 目录下的所有模块
package = importlib.import_module("app.api")
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f"app.api.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
