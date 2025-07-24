#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/06/16 08:05:08
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

import os
from typing import Dict, List, Optional, Tuple, Union

from tqdm import tqdm
import tiktoken
import re

enc = tiktoken.get_encoding("cl100k_base") # 获取GPT（≥3.5）使用的tokenizer

class ReadFiles:
    """
    class to read files
    """

    def __init__(self, path: str) -> None:
        self._path = path

    def get_content(self, chunk_size: int = 500, cover_content: int = 50):
        # 读取文件内容
        chapter_cnt_dict = self.read_file_content(self._path)

        file_content = []
        for chapter in chapter_cnt_dict:
            content = chapter_cnt_dict[chapter]
            chunk_content = self.get_chunk_by_window(content, chunk_size=chunk_size)

            # 如果chunk内容的开头就是 第xx章，则直接返回，否则在其前面加上 章节 信息。
            for chunk in chunk_content:
                if re.match(r'^第[一二三四五六七八九十百零\d]+章\s?.*', chunk):
                    file_content.append(chunk)
                else:
                    file_content.append(chapter + "。" + chunk)

        return file_content

    @classmethod
    def get_chunk_by_window(cls, text: str, chunk_size: int = 500):
        """
        以行为单位，进行滑动窗口切分。不同chunk之间默认重复一个句子。
        """
        lines = text.splitlines()
        lines = [re.sub(r'\s+', '', cnt) for cnt in lines if re.sub(r'\s+', '', cnt) != '']
        lines = [cnt if cnt.endswith("。") else cnt + "。" for cnt in lines]

        # 滑动窗口合并句子
        chunks = []
        chunk = ""
        for line in lines:
            chunk += line
            if len(chunk) >= chunk_size:
                chunks.append(chunk)
                chunk = line
        if chunk:
            chunks.append(chunk)

        return chunks
    
    @classmethod
    def get_chunk(cls, text: str, max_token_len: int = 600, cover_content: int = 150):
        chunk_text = []

        curr_len = 0
        curr_chunk = ''

        token_len = max_token_len - cover_content
        lines = text.splitlines()  # 假设以换行符分割文本为行

        for line in lines:
            line = line.replace(' ', '')
            line_len = len(enc.encode(line))
            if line_len > max_token_len:
                # 如果单行长度就超过限制，则将其分割成多个块
                num_chunks = (line_len + token_len - 1) // token_len
                for i in range(num_chunks):
                    start = i * token_len
                    end = start + token_len
                    # 避免跨单词分割
                    while not line[start:end].rstrip().isspace():
                        start += 1
                        end += 1
                        if start >= line_len:
                            break
                    curr_chunk = curr_chunk[-cover_content:] + line[start:end]
                    chunk_text.append(curr_chunk)
                # 处理最后一个块
                start = (num_chunks - 1) * token_len
                curr_chunk = curr_chunk[-cover_content:] + line[start:end]
                chunk_text.append(curr_chunk)
                
            if curr_len + line_len <= token_len:
                curr_chunk += line
                curr_chunk += '\n'
                curr_len += line_len
                curr_len += 1
            else:
                chunk_text.append(curr_chunk)
                curr_chunk = curr_chunk[-cover_content:]+line
                curr_len = line_len + cover_content

        if curr_chunk:
            chunk_text.append(curr_chunk)

        return chunk_text
    
    @classmethod
    def read_file_content(cls, file_path: str):
        # 根据文件扩展名选择读取方法
        if file_path.endswith('.txt'):
            return cls.read_text(file_path)
        else:
            raise ValueError("Unsupported file type")
        
    @classmethod
    def read_text(cls, file_path: str):
        # 读取文本文件
        # with open(file_path, 'r', encoding='utf-8') as file:
        #     return file.read()
        chapter_cnt_dict = cls.data_preprocess(file_path)
        return chapter_cnt_dict

    @classmethod
    def data_preprocess(cls, file_path: str):
        """
        将 章节标题 作为key，章节内容作为 value，返回剧本内容。
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        chapter_pattern = re.compile(r'^第[一二三四五六七八九十百零\d]+章\s?.*')
        script_dict = {}
        current_title = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if chapter_pattern.match(line):
                if current_title:
                    script_dict[current_title] = '\n'.join(current_content)
                current_title = line
                current_content = []
            else:
                current_content.append(line)

        # 加上最后一章
        if current_title:
            script_dict[current_title] = '\n'.join(current_content)

        return script_dict