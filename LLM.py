#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict, List, Optional, Tuple, Union

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
from typing_extensions import override

_ = load_dotenv(find_dotenv())


class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: List[dict], content: str) -> str:
        pass

    def load_model(self):
        pass


class DeepseekChat(BaseModel):
    def __init__(self, path: str = '', model: str = "deepseek-chat") -> None:
        super().__init__(path)
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        client = OpenAI(api_key=os.getenv('MODEL_API'), base_url=os.getenv('MODEL_BASE_URL'))
        response = client.chat.completions.create(
            model=os.getenv('MODEL_NAME', self.model), # 默认deepseek的 chat模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "用户输入内容为：" + user_prompt},
            ],
            temperature=0.1,
            stream=False,
            top_p=0.7,
            max_tokens=16384,
        )
        return response.choices[0].message.content
