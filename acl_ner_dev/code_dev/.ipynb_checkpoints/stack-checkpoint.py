from tqdm import tqdm
import json

def simple_dict(input_dict):

    # # 输入字典
    # input_dict = {'id': 52, 'mentions': ['antigen testing'], 'type': 'medical test type'}
    
    # 指定要输出的键的顺序
    keys_order = ['mentions', 'type']
    
    # 创建一个新的字典，只包含指定的键
    output_dict = {k: input_dict[k] for k in keys_order if k in input_dict}

    return output_dict

def dup_listdict(list_of_dicts):
    # 使用集合来跟踪已经添加过的字典
    seen = set()
    
    # 使用列表推导式和元组来保持原始顺序并去重
    unique_list_of_dicts = []
    for d in list_of_dicts:
        # 将字典的每个值（如果值是列表，则转换为元组）转换为元组，以便可以添加到集合中
        dict_tuple = tuple(((k, tuple(v) if isinstance(v, list) else v)) for k, v in d.items())
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique_list_of_dicts.append(d)
    return unique_list_of_dicts

def mge_lists(list_one, list_two):
    # 使用集合来跟踪第一个列表中已经出现过的字典
    seen = set()
    for d in list_one:
        # 将字典的每个值（如果值是列表，则转换为元组）转换为元组，以便可以添加到集合中
        dict_tuple = tuple(((k, tuple(v) if isinstance(v, list) else v)) for k, v in d.items())
        seen.add(dict_tuple)
    
    # 遍历第二个列表，将未出现过的元素添加到第一个列表末尾
    for d in list_two:
        dict_tuple = tuple(((k, tuple(v) if isinstance(v, list) else v)) for k, v in d.items())
        if dict_tuple not in seen:
            list_one.append(d)
            seen.add(dict_tuple)
    return list_one

def dup_listset(list1, list2):
    # 合并两个列表
    combined_list = list1 + list2
    
    # 将字典转换为元组（可哈希），去重后再转换回字典
    unique_dicts = {tuple(sorted(d.items())): d for d in combined_list}.values()
    
    # 将结果转换为列表
    result = list(unique_dicts)

    return result

file_path = '../res_dev/gemini-2.0-flash_v21.json'
with open(file_path, 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
    data_gemini_v2_2 = json.load(file)  # 将 JSON 文件内容加载为 Python 对象

file_path = '../res_dev/o3-mini_v21.json'
with open(file_path, 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
    data_03mini_v2 = json.load(file)  # 将 JSON 文件内容加载为 Python 对象

file_path = '../res_dev/deepseek-v3-250324_v21.json'
with open(file_path, 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
    data_ds_v2 = json.load(file)  # 将 JSON 文件内容加载为 Python 对象



print(len(data_gemini_v2_2), len(data_03mini_v2), len(data_ds_v2) )

k_lst = list(data_gemini_v2_2.keys())
print(len(k_lst), k_lst)

for k in tqdm(k_lst):
    if k in list(data_03mini_v2.keys()):    
        d = data_gemini_v2_2[k]['entities']
        d_2 = data_03mini_v2[k]['entities']
        d_simple = [simple_dict(f) for f in d]
        d_2_simple = [simple_dict(f) for f in d_2]
    
        d_new = mge_lists(d_simple, d_2_simple)
        data_gemini_v2_2[k]['entities'] = d_new
        if len(d)!=len(d_new):
            print(k, len(d), len(d_new))

        d = data_gemini_v2_2[k]['triples']
        d_2 = data_03mini_v2[k]['triples']
        d_new = dup_listset(d, d_2)
        data_gemini_v2_2[k]['triples'] = d_new


filename_new = '../res_dev/stack_1.json'
with open(filename_new, 'w', encoding='utf-8') as f:
    # 确保指定ensure_ascii为False以支持非ASCII字符
    json.dump(data_gemini_v2_2, f, ensure_ascii=False, indent=4)
print('finished wrrite data to ->', filename_new)


print('================== 第二遍 =================')
for k in tqdm(k_lst):

    if k in list(data_ds_v2.keys()):
        d_simple = data_gemini_v2_2[k]['entities'].copy()
        len_init = len(d_simple)
        
        d_2 = data_ds_v2[k]['entities']
        # d_simple = d.copy() #[simple_dict(f) for f in d]
        d_2_simple = [simple_dict(f) for f in d_2]
    
        d_new = mge_lists(d_simple, d_2_simple)
        data_gemini_v2_2[k]['entities'] = d_new

        if len_init!=len(d_new):
            print(k, len_init, len(d_new))

        d = data_gemini_v2_2[k]['triples']
        d_2 = data_ds_v2[k]['triples']
        d_new = dup_listset(d, d_2)
        data_gemini_v2_2[k]['triples'] = d_new


filename_new = '../res_dev/stack_2.json'
with open(filename_new, 'w', encoding='utf-8') as f:
    # 确保指定ensure_ascii为False以支持非ASCII字符
    json.dump(data_gemini_v2_2, f, ensure_ascii=False, indent=4)
print('finished wrrite data to ->', filename_new)