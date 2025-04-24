from tqdm import tqdm
import json
import os


path = '../data_dev/'

data_lst = []

file_lst = os.listdir(path)
file_lst = [f for f in file_lst if '.json' in f]

for i in range(len(file_lst)):
    file_i = file_lst[i]
    print(i, file_i)
    with open('{}{}'.format(path, file_i), 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
        data_idx = json.load(file)  # 将 JSON 文件内容加载为 Python 对象  
        data_lst = data_lst + data_idx
        
data_lst = data_lst[:]

print(len(data_lst))

res = {}
for i in range(len(data_lst)):
    data_ = data_lst[i]
    res[i] = data_
print(len(res))

with open('../gt_dev/gt_dev.json', 'w', encoding='utf-8') as f:
    # 确保指定ensure_ascii为False以支持非ASCII字符
    json.dump(res, f, ensure_ascii=False, indent=4)


version_lst = ['v12', 'v21', 'v22', 'v13']
model_lst = ['o3-mini', 'gemini-2.0-flash', 'deepseek-v3-250324']

for version in version_lst:
    for model in model_lst:
        try:
            # version = 'v12'
            # model = 'o3-mini'
            data_lst_bak = []
            for i in tqdm(range(5)):
                file_path = '../modelmake_data_dev/{}_sd42_{}_{}.json'.format(model, version, i)
                with open(file_path, 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
                    data = json.load(file)  # 将 JSON 文件内容加载为 Python 对象
                data_lst_bak = data_lst_bak + data
            
            data_lst_part1 = data_lst_bak.copy()
            print(len(data_lst_part1), )
            
            
            data_lst_all = data_lst_part1 #+ data_lst_part2
            desired_order = ['domain', 'title', 'doc', 'entities', 'triples', 'label_set', 'entity_label_set']
            
            output = {}
            for j in tqdm(range(len(data_lst_all)) ):
                data_ = data_lst_all[j]
                # 使用 sorted() 函数对字典进行排序
                sorted_data = {key: data_[key] for key in desired_order if key in data_}
                output[j] = sorted_data
            print('len is : ', len(output))
            
            
            with open('../res_dev/{}_{}.json'.format(model, version), 'w', encoding='utf-8') as f:
                # 确保指定ensure_ascii为False以支持非ASCII字符
                json.dump(output, f, ensure_ascii=False, indent=4)
            print('finished wrrite data to ->',model, version)
        except:
            print('no file of ->',model, version)