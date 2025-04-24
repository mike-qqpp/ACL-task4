# README

## Project Description

This project aims to enhance model performance through clever prompt engineering and multi-model multi-threaded inference on the dataset, followed by merging and fusing the results. Ultimately, it achieved first place in ACL2025-shared-task4.

## 1. Ablation Study on Dev Data

First, navigate to the root directory `./acl_ner_dev/code_dev`.

### 1.1 Multi-Threaded Inference with Multiple Models

Run the shell script `sh run_dev.sh`, which performs multi-threaded inference using multiple models. This script will execute the following commands:

```bash
python infer_dis.py --file_name v11 --modelname o3-mini
python infer_dis.py --file_name v12 --modelname o3-mini
python infer_dis.py --file_name v13 --modelname o3-mini
python infer_dis.py --file_name v21 --modelname o3-mini
python infer_dis.py --file_name v22 --modelname o3-mini

python infer_dis.py --file_name v11 --modelname gemini-2.0-flash
python infer_dis.py --file_name v12 --modelname gemini-2.0-flash
python infer_dis.py --file_name v13 --modelname gemini-2.0-flash
python infer_dis.py --file_name v21 --modelname gemini-2.0-flash
python infer_dis.py --file_name v22 --modelname gemini-2.0-flash

python infer_dis.py --file_name v11 --modelname deepseek-v3-250324
python infer_dis.py --file_name v12 --modelname deepseek-v3-250324
python infer_dis.py --file_name v13 --modelname deepseek-v3-250324
python infer_dis.py --file_name v21 --modelname deepseek-v3-250324
python infer_dis.py --file_name v22 --modelname deepseek-v3-250324
```

Here, the file names represent different prompt combinations:
- `v11`: BT + input  
- `v12`: BT + FS + input  
- `v13`: BT + COGP + input  
- `v21`: BT + FS + COGP + input  
- `v22`: BT + FS + COGP + Reward + input  

### 1.2 Result Fusion

Run `python stack.py` to:
1. Fuse `gemini-2.0-flash` and `o3-mini` results, generating `/acl_ner_dev/code_dev/res_dev/stack_1.json`.
2. Fuse `gemini-2.0-flash`, `o3-mini`, and `deepseek-v3` results, generating `/acl_ner_dev/code_dev/res_dev/stack_2.json`.

### 1.3 Evaluation

Run `sh eval_dev.sh` to output evaluation metrics for each model.

## 2. Inference on Test Dataset

First, navigate to the root directory `./acl_ner_test/code`.

## Dataset

The dataset for inference is stored in the root directory `./data`.

## Workflow

1. Navigate to the root directory `./code/`.
2. Run the shell script `sh run.sh` to reproduce the complete process.

## Shell Scripts and Their Purposes

### Multi-Model Multi-Threaded Inference

- **infer_dis_gemini.py**: Performs multi-threaded inference using the Gemini model. Results are saved in the root directory `./model/make_data`.
- **infer_dis_part2_gemini.py**: Performs multi-threaded inference using the Gemini model (for cases where the API service may be unstable, re-inferencing cases that failed initially).
- **infer_dis_o3mini.py**: Performs multi-threaded inference using the GPT-O3-Mini model.
- **infer_dis_dschat.py**: Performs multi-threaded inference using the DeepSeek-V3 model.

### Result Merging

- **merge_res_gemini.py**: Merges multi-threaded results from the Gemini model into a single result file, stored in the root directory `./res`.
- **merge_o3mini.py**: Merges results from the GPT-O3-Mini model.
- **merge_res_dschat.py**: Merges results from the DeepSeek-V3 model.

### Result Fusion

- **stack.py**: Fuses results from multiple models, primarily merging named entity recognition (NER) entities to enhance model performance.

### Note

If you need to fully reproduce the results, I can provide a temporary API key for you 😊.