from tqdm import tqdm
import json

version = 'v2_2'
model = 'deepseek-v3-250324'
data_lst_bak = []
for i in tqdm(range(6)):
    file_path = '../modelmake_data/{}_sd42_{}_{}.json'.format(model, version, i)
    with open(file_path, 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
        data = json.load(file)  # 将 JSON 文件内容加载为 Python 对象
    data_lst_bak = data_lst_bak + data

id_forbid_lst = [f['id'] for f in data_lst_bak if len(f['entities'])>0 and  len(f['triples'])>0]
print(len(id_forbid_lst), )

data_lst_part1 = [f for f in data_lst_bak if f['id'] in id_forbid_lst]
print(len(data_lst_part1), )

# # ==================part2 数据 ==============
# data_lst_part2 = []
# for i in tqdm(range(6)):
#     file_path = '../modelmake_data/{}_sd42_{}_{}_part2.json'.format(model, version, i)
#     with open(file_path, 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
#         data = json.load(file)  # 将 JSON 文件内容加载为 Python 对象
#     data_lst_part2 = data_lst_part2 + data
# print(len(data_lst_part2))

data_lst_all = data_lst_part1 #+ data_lst_part2
desired_order = ['domain', 'title', 'doc', 'entities', 'triples', 'label_set', 'entity_label_set']

output = {}
for j in tqdm(range(len(data_lst_all)) ):
    data_ = data_lst_all[j]
    # 使用 sorted() 函数对字典进行排序
    sorted_data = {key: data_[key] for key in desired_order if key in data_}
    output[data_['id']] = sorted_data
print('len is : ', len(output))


with open('../res/{}_{}.json'.format(model, version), 'w', encoding='utf-8') as f:
    # 确保指定ensure_ascii为False以支持非ASCII字符
    json.dump(output, f, ensure_ascii=False, indent=4)
print('finished wrrite data to ->',model, version)