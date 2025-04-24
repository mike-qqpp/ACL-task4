# step1-结果多线程推理
python infer_dis_gemini.py
python infer_dis_part2_gemini.py

python infer_dis_o3mini.py

python infer_dis_dschat.py

# step2-结果合并成单个文件
python merge_res_gemini.py
python merge_res_o3mini.py
python merge_res_dschat.py

# step3-结果融合
python stack.py