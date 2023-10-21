---
language:
- zh
- en
tags:
- hello123hedong
pipeline_tag: text-generation
license: other
tasks:
- chat
studios:
- hello123hedong/LightBig-Baichuan-MedLLM
widgets:
  - task: chat
    version: 1
    inputs:
      - type: text
        name: text
        title: 输入文字
        validator:
        max_words: 128
      - type: text-list
        name: history
    examples:
      - name: 1
        title: 示例1
        inputs:
          - name: text
            data:  请介绍下心脏病
          - name: text
            data: []
    inferencespec:
      cpu: 4
      memory: 32000
      gpu: 1
      gpu_memory: 24000
---
# LightBig-Baichuan-MedLLM

## 概述

LightBig-Baichuan-MedLLM 有效地对齐了医疗场景下的人类偏好，弥合了通用语言模型输出与真实世界医疗问答对之间的差距。
先经过开源医疗数据集进行SFT后, 再使用比赛数据集进行qlora微调.

## 数据集
为了训练 LightBig-Baichuan-MedLLM ，采用复旦大学的 命名为 DISC-Med-SFT的数据集，其中包含了超过47万个衍生于现有的医疗数据集重新构建得到的样本。
[DISC-Med-SFT 数据集](https://huggingface.co/datasets/Flmc/DISC-Med-SFT)

医疗问答对数据集
[MLEC-QA](https://github.com/Judenpech/MLEC-QA)


### 下载
该数据集总共发布了近47万条训练数据，其中包括重构AI医患对话和知识图谱问答对。
您可以访问这个[链接](https://huggingface.co/datasets/Flmc/DISC-Med-SFT)下载数据集。

医疗问答对数据集
[MLEC-QA](https://github.com/Judenpech/MLEC-QA)

## 部署

当前版本的 LightBig-Baichuan-MedLLM 是基于[**Baichuan-13B**](https://github.com/baichuan-inc/Baichuan-13B)训练得到的。
您可以直接从 [modescope](https://www.modelscope.cn/hello123hedong/LightBig-Baichuan-MedLLM.git) 上下载模型权重，或者根据下列代码样例中的方式自动获取。

首先，您需要安装项目的依赖环境。
```shell
pip install -r requirements.txt
```

### 利用modescope 的transformers模块来进行推理
```python
>>> import torch
>>> from modelscope import AutoModelForCausalLM, AutoTokenizer
>>> from modelscope import GenerationConfig
>>> tokenizer = AutoTokenizer.from_pretrained("hello123hedong/LightBig-Baichuan-MedLLM", use_fast=False, trust_remote_code=True)
>>> model = AutoModelForCausalLM.from_pretrained("hello123hedong/LightBig-Baichuan-MedLLM", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
>>> model.generation_config = GenerationConfig.from_pretrained("hello123hedong/LightBig-Baichuan-MedLLM")
>>> messages = []
>>> messages.append({"role": "user", "content": "我感觉自己颈椎非常不舒服，每天睡醒都会头痛"})
>>> response = model.chat(tokenizer, messages)
>>> print(response)
```

## 对模型进行微调
使用比赛的数据集, 处理成我们规定的数据形式对模型进行微调。  data_deal2.py 生成模型训练数据集 格式数据 
目录train/data中已经生成了.可以直接使用
我们的训练代码在 [Firefly](https://github.com/yangjianxin1/Firefly) 的基础上进行了修改，
使用了不同的数据结构和对话格式。这里我们只提供了qlora微调：
```shell
deepspeed --num_gpus={num_gpus} ./train/train_qlora.py --train_args_file ./train/train_args/baichuan-13b-sft-qlora.json
```
> 请您在开始进行模型训练前检查 `baichuan-13b-sft-qlora.json` 中的设置。

## 模型评测
1) 下载模型权重 [modescope](https://www.modelscope.cn/hello123hedong/LightBig-Baichuan-MedLLM.git) 
到  "./output/baichuan-13b/merge" 
2) 运行infer.py 文件 , 生成结果
3) 运行 gen_result.py 生成评测数据

## 调优经验
使用比赛提供的数据集进一步微调
1) "num_train_epochs": 6,
    "per_device_train_batch_size": 10,
    "gradient_accumulation_steps": 2,
    "learning_rate": 1e-4,

```json
{
    "epoch": 9.92,
    "train_loss": 2.5992207204141926,
    "train_runtime": 6723.0793,
    "train_samples_per_second": 1.487,
    "train_steps_per_second": 0.046
}
```
指令调优可以, 效果未知

2) "num_train_epochs": 16,
    "per_device_train_batch_size": 10,
     "gradient_accumulation_steps": 2,
    "learning_rate": 1e-4,
```json
***** train metrics *****
  epoch                    =       16.0
  train_loss               =     0.9776
  train_runtime            = 3:10:51.09
  train_samples_per_second =      1.397
  train_steps_per_second   =       0.07
```
指令调优可以, 效果未知


## error
1. 解决ValueError: Error initializing torch.distributed using env:// rendezvous:: environment variable 报错
[link](https://blog.csdn.net/weixin_57634679/article/details/129082198)
2. ERROR: Could not build wheels for mpi4py, which is required to install pyproject.toml-based projects
[link](https://blog.csdn.net/wenzhang1216/article/details/126902883)
3.  pip install bitsandbytes==0.39.0 否则报错  使用的cuda是11.6

## 致谢
本项目基于如下开源项目展开，在此对相关项目和开发人员表示诚挚的感谢：

- [**cMedQA**](https://github.com/zhangsheng93/cMedQA2)

- [**Baichuan-13B**](https://github.com/baichuan-inc/Baichuan-13B)

- [**FireFly**](https://github.com/yangjianxin1/Firefly)

同样感谢其他限于篇幅未能列举的为本项目提供了重要帮助的工作。
