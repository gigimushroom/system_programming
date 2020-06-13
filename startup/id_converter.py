import random
import json
import pandas as pd
import cpca
import pprint as pp
import os.path


# Run the monster!
pd.options.display.max_rows = 999

def parse_ids_to_unique(input_list, db_name='db/id_db.json'):
    db = None
    with open(db_name) as f:
        db = json.load(f)
        
    idx_to_id_dict = {}
    unique_set = set()
    missed = 0
    for i, v in enumerate(input_list):
        name = v
        if name in db and name not in unique_set:
            if not db[name]:
                print('something is fuck up')
            idx_to_id_dict[i] = (name, db[name])
            unique_set.add(name)
            print('Found', name)
        else:
            idx_to_id_dict[i] = None
            missed += 1
    
    print
    
    keys = set(db.keys())
    keys = keys - unique_set
    shuffle_keys = list(keys)
    random.shuffle(shuffle_keys)
    
    #print(shuffle_keys)
    shuffled_list = [(name, db[name]) for name in shuffle_keys]
    for k, v in idx_to_id_dict.items():
        if not v:
            tup = shuffled_list.pop()
            idx_to_id_dict[k] = tup
            
    # Conver dict back to list
    # but in python 3.7+, insertion-order preservation for dicts
    # we should have correct order.
    
    #print(idx_to_id_dict)
    return idx_to_id_dict
    
def test_parse_ids():
    
    input = ["张蔚雯", "周亮", "周亮", "曾雪琴",  "曾雪琴",  "曾雪琴"]
    print(parse_ids_to_unique(input))
    
    print("PASSED")

#test_parse_ids()


def run(file_name, write=False):
    if not file_name or not os.path.isfile(file_name):
        return False
    
    df = pd.read_excel(file_name, sheet_name='Input', usecols = "K", header=None)

    l_of_l = df.values[6:] # Skip ['联系方式']
    input_data = [str(''.join(n)) for n in l_of_l if not pd.isna(n)]
    #print(input_data)
    results = parse_ids_to_unique(input_data)
    #print(results)

    name_col = ['','','','','','']
    id_col = ['','','','','','']
    for _, pair in results.items():
        name, id_num = pair
        name_col.append(name)
        id_col.append(id_num)
    
    if write:
        base = pd.read_excel(file_name, sheet_name='Input', header=None)
        base['替换姓名'] = pd.Series(name_col)
        base['替换身份证'] = pd.Series(id_col)
        base.to_excel('haha3.xls', index=False)
        
    return name_col, id_col

#run('aaa.xlsm')

def test_run(file_name):
    print('Parsing excel:', file_name)

# with open('id_db.json') as f:
#     db = json.load(f)
#     print('陈晨' in db)
