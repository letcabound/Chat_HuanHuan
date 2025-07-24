# -*- coding: utf-8 -*-
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("MODEL_API"), base_url=os.getenv("MODEL_BASE_URL"))

# 聊天调用
response = client.chat.completions.create(
    model="GLM-4-Flash-250414",  # 或 "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "你是一个知识渊博的助手"},
        {"role": "user", "content": "你好，请用一句话解释量子力学"}
    ],
    temperature=0.95,
    max_tokens=100,
    top_p=0.7
)

# 输出结果
print(response.choices[0].message.content)