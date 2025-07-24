# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
from pandas import DataFrame


class DataProcessor:
    """
    将通过大模型，初步从小说中提取到的人物台词对话，进行清洗后处理。
    """
    def __init__(self, org_path: str, goal_path: str = ""):
        self._path = org_path # 待处理文件路径
        if not goal_path:
            file_name = os.path.basename(org_path).split(".")[0]
            self.file_save_path = f"./{file_name}_etl.jsonl"

    def process(self):
        file_path = self._path
        assert os.path.exists(file_path), f"文件不存在:{file_path}"
        assert file_path.endswith("jsonl"), "文件格式应该为 jsonl"
        print(f"开始处理文件:{file_path}")

        try:
            df = self._from_jsonl_2_dataframe(file_path)
            data_etl = self._data_etl(df)

            # 将data_etl数据写入文件
            file_save_path = self.file_save_path
            # data_etl.to_json(file_save_path, orient="records", force_ascii=False, indent=2)
            data_etl.to_json(file_save_path, orient='records', lines=True, force_ascii=False)
            print(f"成功存储清洗后的json文件，存储路径:{file_save_path}")

        except Exception as e:
            print(e)

    @classmethod
    def _from_jsonl_2_dataframe(cls, file_path: str):
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data.append(json.loads(line))
            print("成功将jsonl文件转换为DataFrame格式")

            return pd.DataFrame(data)

        except Exception as e:
            print(f"读取jsonl文件转换为 DataFrame 格式出错。jsonl源文件路径:{file_path}, 错误信息:{e}")
            raise Exception(f"读取jsonl文件转换为 DataFrame 格式出错。jsonl源文件路径:{file_path}, 错误信息:{e}")

    @classmethod
    def _data_etl(cls, df: DataFrame):
        # 角色名称统一
        try:
            df["role"] = df["role"].str.replace("我", "甄嬛")
            df["role"] = df["role"].str.replace("嬛儿", "甄嬛")
            df["role"] = df["role"].str.replace("嬛嬛", "甄嬛")
            print("成功统一角色名称")
        except Exception as e:
            raise Exception(f"DataFrame数据，角色名称统一出错。错误信息:{e}")

        # 过滤 无效对白 行，去重
        try:
            df["dialogue"] = df["dialogue"].str.replace(r'[.“”…]', '', regex=True)
            df = df[df["dialogue"].str.strip() != ""]
            df = df.drop_duplicates(subset=['dialogue'], keep='last')
            print("成功过滤 无效对白 行，去重")
        except Exception as e:
            raise Exception(f"DataFrame数据，过滤 无效对白 行，去重出错。错误信息:{e}")

        return df
