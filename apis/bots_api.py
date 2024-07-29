# -*- coding: utf-8 -*-
"""
@Time: 2024/6/17 上午2:29
@Auth: Bacchos
@File: bots_api.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)
"""

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

from fastapi.responses import StreamingResponse

from apps.genai import initialize_model
from db.db_utils import store_conversation

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    bot_name: str


def load_prompt(bot_name: str) -> str:
    file_mapping = {
        "BTC": "BTC_prompt.json",
        "ETH": "ETH_prompt.json",
        "PEPE": "PEPE_prompt.json",
        "SOL": "SOL_prompt.json",
        "DOGE": "DOGE_prompt.json",
    }
    file_name = file_mapping.get(bot_name)
    if not file_name:
        raise HTTPException(status_code=400, detail="Invalid bot_name")

    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "..", file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as file_prompt:
            return json.load(file_prompt)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Prompt file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON file")


@router.post("/chat_api")
async def chat_api(request: ChatRequest):
    try:
        conversation_history = load_prompt(request.bot_name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading prompt file")

    user_input = request.message
    conversation_history.append({"role": "user", "parts": [user_input]})

    try:
        model = initialize_model(request.bot_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error initializing model")

    chat_session = model.start_chat(history=conversation_history)
    response = chat_session.send_message(user_input, stream=True)

    async def response_stream():
        conversation_text = ""
        for chunk in response:
            conversation_text += chunk.text + "\n"
            yield chunk.text + "\n"
        store_conversation(request.bot_name, 'user', user_input)
        store_conversation(request.bot_name, 'model', conversation_text)

    return StreamingResponse(response_stream(), media_type="text/plain")
