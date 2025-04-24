import time
import random
from http import HTTPStatus
import json
from tqdm import tqdm
import multiprocessing as mp
import pandas as pd
from openai import OpenAI
import json
import warnings
import os

# 忽略DeprecationWarning
warnings.filterwarnings("ignore")


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_name', type=str)
parser.add_argument('--modelname', type=str)



global file_name, seed, modelname

args = parser.parse_args()
file_name, modelname = args.file_name, args.modelname

# file_name = 'v2_2'
# modelname = 'o3-mini'
seed = 42




def find_all_positions(main_string, target_string):
    """
    找到指定子字符串在主字符串中出现的所有位置（索引）。
    
    :param main_string: 主字符串
    :param target_string: 要查找的子字符串
    :return: 一个列表，包含子字符串出现的所有起始索引位置
    """
    positions = []  # 用于存储子字符串出现的位置
    start = 0  # 从主字符串的起始位置开始查找

    while True:
        # 在主字符串中查找子字符串的位置
        position = main_string.find(target_string, start)
        if position == -1:  # 如果没有找到子字符串，退出循环
            break
        positions.append(position)  # 将找到的位置添加到列表中
        start = position + 1  # 更新起始位置，继续查找下一个位置

    return positions

def is_good_res(s):
    try:
        positions = find_all_positions(s, '{')
        pos_s = positions[0]
        positions = find_all_positions(s, '}')
        pos_e = positions[-1]
    
        
        s_clean = s[pos_s:pos_e+1]

        res = eval(s_clean)

        entities = res['entities']
        triples = res['triples']
        
        triples_new = [f for f in triples if 'relation' in f.keys() and len(f)==3]

        if len(entities)>0 and len(triples_new)>0:
            return 1, entities, triples_new
        else:
            return 0, [], []     
    except:
        return 0, [], []


# def chunk_list(input_list, chunk_size, num_worker):
#     new_lst = [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
#     if len(new_lst) > num_worker:
#         print(1)
#         new_lst_2 = new_lst[:num_worker].copy()
#         new_lst_2[-1] = new_lst_2[-1] + new_lst[-1]
#         return new_lst_2
#     else:
#         return new_lst

def chunk_list(input_list, chunk_size, num_worker):
    # 初始分块
    new_lst = [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
    
    # 如果分块数量大于 num_worker
    if len(new_lst) > num_worker:
        # 保留前 num_worker - 1 个分块
        new_lst_2 = new_lst[:num_worker - 1]
        # 将剩余的分块合并到最后一个分块
        new_lst_2.append(sum(new_lst[num_worker - 1:], start=[]))
        return new_lst_2
    else:
        return new_lst



def call_stream_with_messages(data_):

    BT = f'''你是一个文档ner和三元组提取专家，我会给你一个文档所属领域domain、文档document、待提取的NER实体类型entity_label_set、待提取的三元组关系类型label_set，你帮我根据输入提取出来文档中出现的ner实体及三元组。
    \n'''

    FS = f'''    下面我会给你提供输入、输出的案例\n\n \
##案例1
    ##输入是：
    "domain": "Communication",
    "doc": "The  automatic curb sender was a kind of telegraph key, invented by William Thomson, 1st Baron Kelvin for sending messages on a submarine communications cable, as the well-known Wheatstone transmitter sends them on a land line.\nIn both instruments, the signals are sent by means of a perforated ribbon of paper but the cable sender was the more complicated, because the cable signals are formed by both positive and negative currents, and not merely by a single current, whether positive or negative.  Moreover, to curb the prolongation of the signals due to electromagnetic induction, each signal was made by two opposite currents in succession: a positive followed by a negative, or a negative followed by a positive. The aftercurrent had the effect of \"curbing\" its precursor.\nFor some time, it was the only instrument delicate enough to receive the signals transmitted through a long cable.\nThis self-acting cable key was brought out in 1876, and tried on the lines of the Eastern Telegraph Company.\n",
    "label_set": [
        "HasQuality",
        "InfluencedBy",
        "Continent",
        "NominatedFor",
        "AppliesToPeople",
        "LocatedIn",
        "Founded",
        "Uses",
        "OfficialLanguage",
        "MemberOf",
        "UsedBy",
        "PartOf",
        "Studies",
        "HasWorksInTheCollection",
        "Affiliation",
        "HasEffect",
        "OwnerOf",
        "Country",
        "Creator",
        "DiplomaticRelation",
        "ApprovedBy",
        "HasPart"
    ],
    "entity_label_set": [
        "CARDINAL",
        "DATE",
        "EVENT",
        "FAC",
        "GPE",
        "LANGUAGE",
        "LAW",
        "LOC",
        "MONEY",
        "NORP",
        "ORDINAL",
        "ORG",
        "PERCENT",
        "PERSON",
        "PRODUCT",
        "QUANTITY",
        "TIME",
        "WORK_OF_ART",
        "MISC"
    ]
     ##输出是：
     {{
        "entities": [
            {{
            "id": 0,
                "mentions": [
                    "Industrial Revolution"
                ],
                "type": "event"
            }},
            {{
            "id": 1,
                "mentions": [
                    "HKW"
                ],
                "type": "organization"
            }},
            ... ...
        ],
        "triples": [
            {{
                "head": "Max Planck Institute",
                "relation": "part of",
                "tail": "Max Planck Society"
            }},
            {{
                "head": "Crawford Lake",
                "relation": "country",
                "tail": "Canada"
            }},
            ... ... 
        ],
    }}
    \n'''

    COGP = f'''##注意点：
    ##我不需要你给我分析的过程和赘述，仅仅并且务必只需要你给我输出我指定的json格式结果就行！！
    ##输出格式为{{'entities':'xxx','triples':'xxx'}} ##一定要保证json是正确的格式，通过print函数不会输出报错！！
    ##输出中的entities代表的ner实体，triples是三元组
    \n'''

    Reward = f'''###我希望你能够尽可能多的去挖掘出来NER实体和三元组，这样我会给你一个大大的惊喜！！！
    \n'''

    input = f'''   
    ##我的输入是：
    "domain": {data_['domain']}
    "doc": {data_['doc']}
    "entity_label_set":{data_['entity_label_set']}
    "label_set":{data_['label_set']}
    \n'''

    if file_name == 'v11':
        prompt = BT + input
    elif file_name == 'v12':
        prompt = BT + FS + input
    elif file_name == 'v13':
        prompt = BT + COGP + input
    elif file_name == 'v21':
        prompt = BT + FS + COGP + input
    elif file_name == 'v22':
        prompt = BT + FS + COGP + Reward + input



    key = 'sk-xxx'
    client = OpenAI(
        base_url="https://api.wlai.vip/v1",
        api_key=key
    )

    try:
        response = client.chat.completions.create(
          model=modelname,
          messages=[
            {"role": "user", "content": prompt},
    
          ]
        )
        return eval(response.json().replace("null","'null'"))['choices'][0]['message']['content']
    except:
        return 'no res'



def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def worker_fn(wid, data_lst_wids, ):

    
    if wid <=10:
        cnt_good, cnt_used, cnt_nores = 0, 0, 0
    
        data_lst = data_lst_wids[wid]
        qr_lst = []

        
        for idx in range(len(data_lst)):
            data_ = data_lst[idx]
            desired_order = ['domain', 'title', 'doc', 'label_set', 'entity_label_set']
            data_idx = {key: data_[key] for key in desired_order if key in data_}

            for _ in range(3):
                res_i = call_stream_with_messages(data_idx)
                # time.sleep(1)

                sig_isgood, entities, triples_new = is_good_res(res_i)
                if sig_isgood==1:
                    break
                else:
                    1
                    # res_i = 'no res'
    
            if res_i == 'no res':
                cnt_nores += 1
            else:
                cnt_good += 1
            qr_lst.append({
                        # 'id': data_idx['id'],
                           'domain': data_idx['domain'],
                           'title': data_idx['title'],
                           'doc': data_idx['doc'],
                           'label_set': data_idx['label_set'],
                           'entity_label_set': data_idx['entity_label_set'],
                           'res':res_i,
                           'entities':entities,
                           'triples':triples_new
                           
                           
                           })

    
            print('===== finished wid-{} part {}/{} =====, good:{}, no res:{}'.format(wid,
                                                                                                                      idx+1,
                                                                                                                      len(data_lst),
                                                                                                                      cnt_good,
                                                                                                                      # cnt_used,
                                                                                                                      cnt_nores))
    
            with open('../modelmake_data_dev/{}_sd{}_{}_{}.json'.format(modelname, seed, file_name, wid), 'w',
                      encoding='utf-8') as f:
                # 确保指定ensure_ascii为False以支持非ASCII字符
                json.dump(qr_lst, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    path = '../data_dev/'
    
    data_lst = []
    
    file_lst = os.listdir(path)
    file_lst = [f for f in file_lst if '.json' in f]

    # print(len(file_lst))
    
    for i in range(len(file_lst)):
        file_i = file_lst[i]
        print(i, file_i)
        with open('{}{}'.format(path, file_i), 'r', encoding='utf-8') as file:  # 使用 'utf-8' 编码打开文件
            data_idx = json.load(file)  # 将 JSON 文件内容加载为 Python 对象  
            data_lst = data_lst + data_idx
            
    data_lst = data_lst[:]
    print(len(data_lst))
    print(data_lst[0].keys())

    num_worker = 5

    data_lst_wids = chunk_list(data_lst, len(data_lst) // num_worker, num_worker)
    print('文件切分为：{}块  '.format(len(data_lst_wids)), [len(f) for f in data_lst_wids])

    process_list = []
    for wid in range(num_worker):
        process = mp.Process(target=worker_fn, args=(wid, data_lst_wids,))
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()
