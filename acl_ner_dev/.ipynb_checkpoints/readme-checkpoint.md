# 项目说明

本项目旨在通过多模型对数据集进行多线程推理，并将结果进行合并与融合，以提升模型效果。

## 团队名字及团队介绍
qqpprun， 网易易盾， 成员 Chenfeng Qiu, Kaifeng Wei, Yuke Li.

## 数据集

待推理数据集存储于 `./data` 根目录下。

## 运行流程

1. 进入 `./code/` 根目录。
2. 执行 `sh run.sh` 脚本来复现完整流程。

## 代码用途

### 多模型多线程推理

- **infer_dis_gemini.py**：多线程采用 Gemini 模型进行推理，结果将保存于 `./model/make_data` 根目录下。
- **infer_dis_part2_gemini.py**：多线程采用 Gemini 模型进行推理（针对 API 服务可能存在的不稳定现象，对未推理出的案例再次推理）。
- **infer_dis_o3mini.py**：多线程采用 GPT-O3-Mini 模型进行推理。
- **infer_dis_dschat.py**：多线程采用 DeepSeek-V3 模型进行推理。

### 结果合并

- **merge_res_gemini.py**：将 Gemini 模型的多线程结果合并成一个结果文件，存储于 `./res` 根目录下。
- **merge_o3mini.py**：合并 GPT-O3-Mini 模型的结果。
- **merge_res_dschat.py**：合并 DeepSeek-V3 模型的结果。

### 结果融合

- **stack.py**：将多模型结果进行融合，主要是将命名实体识别（NER）实体进行合并，以提升模型效果。


### ps:要是你们需要完整复现，我提供一个临时的api key给你们😊。
