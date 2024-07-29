# -*- coding: utf-8 -*-
"""
@Time: 2024/6/17 上午2:28
@Auth: Bacchos
@File: genai.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)
"""

import json
import os
import google.generativeai as genai
from google.generativeai import GenerationConfig

from db.db_utils import get_system_instruction

genai.configure(api_key=os.environ["GENAI_API_KEY"])
genai_config = GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    response_mime_type="text/plain",
)


def initialize_model(bot_name: str):
    system_instruction = get_system_instruction(bot_name)
    if system_instruction is None:
        raise ValueError(f"No system instruction found for {bot_name}")

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=genai_config,
        system_instruction=system_instruction,
    )
