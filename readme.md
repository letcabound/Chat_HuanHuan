# Chat_HuanHuan

>***本仓库为`Chat_HuanHuan`！本仓库的贡献是在参考项目的基础上，优化 `针对甄嬛传小说的对白提取逻辑`；`由指定大模型修改为兼容任一符合Openai接口规范的大模型`，`对提取到的小说对白数据etl处理`，`添加微调部分的代码`等。***
>
>感谢大佬开源的**文本对话抽取**项目，地址：`https://github.com/KMnO4-zx/extract-dialogue.git`

## Show

`repo`：https://github.com/letcabound/Chat_HuanHuan.git

本项目利用`chatgpt`从小说中提取对话集，提取的样本中包括`role`，`dialogue`，比如以下的形式：

```json
[
  {
    "role": "沈眉庄",
    "dialogue": "在京里休息了两日，已经好得多。妹妹今日打扮得好素净，益发显得姿容出众，卓而不群。"
  }, 
  {
    "role": "我",
    "dialogue": "姐姐不是美人么？这样说岂不是要羞煞我。"
  }
]
```

## QuickStart

- 克隆仓库并切换目录：`git clone https://github.com/letcabound/Chat_HuanHuan.git`，`cd Chat_HuanHuan`

- 安装依赖：`pip install -r requirements.txt`
    - 在当前目录创建`.env`文件，并填入`MODEL_NAME`,`MODEL_API`,`MODEL_BASE_URL`。
- 把你要提取的小说或文本，放到当前目录，在`main.py`中修改`path`。

- 运行`main.py`进行微调数据准备，`python main.py`
- 执行`Qwen2.5_7b_Lora微调.ipynb`文件，进行模型微调。

结果如下所示：

```json
{"role": "沈眉庄", "dialogue": "嬛儿，你在这里我就放心了。上次听外婆说妹妹受了风寒，可大好了？"}
{"role": "我", "dialogue": "不过是咳嗽了两声，早就好了。劳姐姐费心。路上颠簸，姐姐可受了风尘之苦。"}
{"role": "沈眉庄", "dialogue": "在京里休息了两日，已经好得多。妹妹今日打扮得好素净，益发显得姿容出众，卓而不群。"}
{"role": "她", "dialogue": "在京里休息了两日，已经好得多。妹妹今日打扮得好素净，益发显得姿容出众，卓而不群。"}
{"role": "我", "dialogue": "姐姐不是美人么？这样说岂不是要羞煞我。"}
{"role": "我", "dialogue": "几日不见，姐姐出落得越发标致了。皇上看见必定过目不忘。"}
{"role": "眉庄", "dialogue": "谨言慎行！今届秀女佼佼者甚多，姐姐姿色不过而而，未必就能中选。"}
```

## 参考

【1】https://eyurtsev.github.io/kor/index.html#

【2】https://zhuanlan.zhihu.com/p/646948797

【3】https://github.com/KMnO4-zx/extract-dialogue.git
