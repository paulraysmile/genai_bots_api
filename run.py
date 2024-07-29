# -*- coding: utf-8 -*-
"""
@Time: 2024/7/25 上午1:15
@Auth: Bacchos
@File: run.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)
"""

from fastapi import FastAPI
from apis.bots_api import router as chat_api_router
import uvicorn

app = FastAPI()

app.include_router(chat_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)