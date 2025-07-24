from openai import OpenAI
import json
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

SYSTEM_PROMPT_CHINESE = """
## 任务描述
你是一位专业的文本信息提取专家，你的任务是从用户输入的剧本小说中提取角色的台词对话以及对话所属的人物名称。


## 要求
1. 分析文本内容，提取出文本中的人物的对话台词以及台词对应的人物名称。
2. 你只能提取 中文双引号“” 括起来的内容作为对话台词内容，禁止提取文本的其它旁白内容，禁止胡乱编造。
3. 输出格式为json列表，参照【输出格式示例】，列表的每个元素为字典，字典包含：role，dialogue 两个字段。role为角色姓名，dialogue为对话台词。
4. 如果文本中没有明确的对话台词，则返回josn格式的空列表[]


## 输入格式示例
'
第一章 风波。 这场选秀对我的意义并不大，我只不过来转一圈充个数便回去。爹爹说，我们的女儿娇纵惯了，怎受得了宫廷约束。
因而，我并不细心打扮。脸上薄施粉黛，一身浅绿色裙装。
满满一屋子秀女，与我相熟的只有济州都督沈自山的女儿沈眉庄。我府与她京中外婆府上比邻而居，我和她更是自小一起长大，情谊非寻常可比。她远远看见我，走过来的执我的手，面含喜色关切道：“嬛儿，你在这里我就放心了。上次听外婆说妹妹受了风寒，可大好了？”
我急忙起身说：“不过是咳嗽了两声，早就好了。劳姐姐费心。路上颠簸，姐姐可受了风尘之苦。”
她点点头，细细看我两眼，微笑说：“在京里休息了两日，已经好得多。妹妹今日打扮得好素净，益发显得姿容出众，卓而不群。”
 我脸上飞红，害羞道：“姐姐不是美人么？这样说岂不是要羞煞我。”
'


## 输出格式示例
[
    {"role": "沈眉庄", "dialogue": "嬛儿，你在这里我就放心了。上次听外婆说妹妹受了风寒，可大好了？"},
    {"role": "我", "dialogue": "不过是咳嗽了两声，早就好了。劳姐姐费心。路上颠簸，姐姐可受了风尘之苦。"},
    {"role": "沈眉庄", "dialogue":"在京里休息了两日，已经好得多。妹妹今日打扮得好素净，益发显得姿容出众，卓而不群。"},
    {"role": "我", "dialogue": "姐姐不是美人么？这样说岂不是要羞煞我。"}
]


"""

SYSTEM_PROMPT = """
Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any attributes that do not appear in the schema shown below.
{TypeScript}
Please output the extracted information in JSON format in Excel dialect. 

Do NOT add any clarifying information. Output MUST follow the schema above. Do NOT add any additional columns that do not appear in the schema.

Input: 
{Input}
Output:
{Output}
"""



def get_typescript(schema, type_script_str):
    script = schema['attributes']
    script_str = ',\n    '.join([f"{s['name']}: {s['type']} // {s['description']} " for s in script])
    type_script_str = type_script_str.format(task_description=schema['task_description'], attributes=script_str)
    return type_script_str

def system_prompt(schema):
    return SYSTEM_PROMPT.format(TypeScript=get_typescript(schema, TYPE_SCRIPT), Input=schema['example'][0]['text'], Output=json.dumps(schema['example'][0]['script'], indent=4, ensure_ascii=False))

