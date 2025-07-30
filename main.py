import time
import json
import os

from extract import SYSTEM_PROMPT_CHINESE
from data_process import DataProcessor
from LLM import DeepseekChat
from utils import ReadFiles
from tqdm import tqdm


def main(file_path: str, chunk_size: int = 300, extracted_succeed: bool = False, etl_succeed: bool = False):

    file_name = os.path.basename(file_path).split('.')[0]
    jsonl_save_path = f'./data/output/{file_name}.jsonl'

    if not extracted_succeed:
        docs = ReadFiles(file_path).get_content(chunk_size=chunk_size, cover_content=0)
        sys_prompt = SYSTEM_PROMPT_CHINESE
        model = DeepseekChat()

        for i in tqdm(range(len(docs))):
            time.sleep(3)
            response_model = model.chat(sys_prompt, docs[i]).strip('```json').strip('```').strip()
            try:
                response = json.loads(response_model)
                for item in response:
                    with open(jsonl_save_path, 'a', encoding='utf-8') as f:
                        json.dump(item, f, ensure_ascii=False)
                        f.write('\n')
            except Exception as e:
                print(f"第{i}个文本块处理过程出错，错误信息:{e}")
                print(f"模型返回的信息为：{response_model}")

    if not etl_succeed:
        processor = DataProcessor(jsonl_save_path)
        processor.process()


if __name__ == '__main__':
    # file_path = './data/甄嬛传.txt'
    file_path = './data/甄嬛传_21.txt'
    main(file_path,
         extracted_succeed=True, # 是否完成了对话抽取
         etl_succeed=False # 是否完成了对话抽取后的etl逻辑
         )

