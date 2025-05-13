# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     run
   Description :
   Author :       powercheng
   date：          2025/5/13
-------------------------------------------------
   Change Activity:
                   2025/5/13:
-------------------------------------------------
"""
__author__ = 'powercheng'

import uvicorn


def main():
    uvicorn.run(app="app.main:app", host="127.0.0.1", port=9000, reload=True)

if __name__ == "__main__":
    main()