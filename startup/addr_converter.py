import random
import json
import pandas as pd
import cpca
import pprint as pp
import os.path

tests = ['广东省中山市石岐起湾道盛景园11-302', '河南省商丘市夏邑县龙湖明珠东区16-502']
# find similar addr for duplicate addr
    
# Given a list, containing dups, generate a new list.
dup_l = [['广东省中山市石岐起湾道盛景园11-302', '123456'],
         ['河南省商丘市夏邑县龙湖明珠东区16-502', '8888'],
         ['广东省中山市石岐起湾道盛景园11-302', '123456'], 
         ['广东省中山市石岐起湾道盛景园11-302', '123456'], 
         ['河南省商丘市夏邑县龙湖明珠东区16-502', '8888'],
         ['河南省商丘市夏邑县龙湖明珠东区16-502', '8888'],
         ['河南省商丘市夏邑县龙湖明珠东区16-502', '8888'],
         ['河南省商丘市夏邑县龙dassa东区16-999', '7777'],
        ]

def addr_transform(loc):
    cp = cpca.transform(loc, cut=False,open_warning=False)
    prov = [v[0] for v in cp.values]
    city = [v[1] for v in cp.values]
    area = [v[2] for v in cp.values]
    
    return prov[0], city[0], area[0]
    
def parse_addrs_to_unique(dup_l, db_name='db/addr.json'):
    # parse json to dict
    db = None
    with open(db_name) as f:
        db = json.load(f)

    def find_similar_addr(addr, db=None, count=1):
        # Given an address, and duplicate count, return unique addresses. 
        def addr_transform(loc):
            cp = cpca.transform(loc, cut=False,open_warning=False)
            prov = [v[0] for v in cp.values]
            city = [v[1] for v in cp.values]
            area = [v[2] for v in cp.values]

            return prov[0], city[0], area[0]

        p, c, a = addr_transform([addr])
        if not c in db[p]:
            c = ''

        if not a in db[p][c]:
            a = ''

        result = []

        if count-1 > len(db[p][c][a]):
            print("You will get duplicate for", addr)

        bigger_list = db[p][c][a]
        random.shuffle(bigger_list)
        if '' in db[p][c]:
            list_add_on = db[p][c]['']
            random.shuffle(list_add_on)
            bigger_list.extend(list_add_on)

        chosen = bigger_list[:count-1]

        result.extend(chosen)
        return result


    all_addr = []
    all_addr_d = {}
    # Parse the original list.
    for addr, num in dup_l:
        all_addr.append(addr)
        all_addr_d[addr]=num
    
    print(all_addr)
    # dict for {addr_A: 5, addr_B: 8}. Number of count
    addr_count_dict = {}
    for a in all_addr:
        if a in addr_count_dict:
            addr_count_dict[a]+=1
        else:
            addr_count_dict[a]=1

    # Filter to only duplicates
    filtered_d = {}
    for k,v in addr_count_dict.items():
        if v > 1:
            filtered_d[k]=v
    print('filtered', filtered_d)

    # Generate a dict, key is addr, value is list of unique address replacement.
    all_choices = {}
    for addr, count in filtered_d.items():
        p, c, a = addr_transform([addr])
        result_list = find_similar_addr(addr, db=db, count=count)
        result_list.append([addr, all_addr_d[addr]])
        all_choices[addr] = result_list
    #print(all_choices)

    # Prepare final result. If address is duplicated, use one from all_choices.
    final_list = []
    for addr, num in dup_l:
        if addr in filtered_d:
            choice=all_choices[addr].pop()
            final_list.append(choice)
        else:
            final_list.append([addr,num])

    #pp.pprint(final_list)

    # Verify
    for i, v in enumerate(final_list):
        str = "Old addr(%s) converts to (%s)" % (dup_l[i][0], v[0])
        #print(str)
    
    return final_list

#print(parse_addrs_to_unique(dup_l))


# Run the monster!
pd.options.display.max_rows = 999

def run(file_name, write=False):
    if not file_name or not os.path.isfile(file_name):
        return False
    
    df = pd.read_excel(file_name, sheet_name='Input', usecols = "L:M", header=None)

    l_of_l = df.values[6:] # Skip ['联系方式' '收件人地址']

    input_data = []
    for num, addr in l_of_l:
        if pd.isna(addr):
            break
        input_data.append([addr, str(num)])

    results = parse_addrs_to_unique(input_data)
    print(results[:5])

    addr_col_data = ['','','','','','']
    num_col_data = ['','','','','','']
    for addr, num in results:
        addr_col_data.append(addr)
        num_col_data.append(num)
    
    if write:
        base = pd.read_excel(file_name, sheet_name='Input', header=None)
        base['替换地址'] = pd.Series(addr_col_data)
        base['替换电话'] = pd.Series(num_col_data)
        base.to_excel('haha.xls', index=False)
    
    return addr_col_data, num_col_data

# run('bbb.xlsm')

def test_run(file_name):
    print('Parsing excel:', file_name)

