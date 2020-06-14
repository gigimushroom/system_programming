import random
import json
import pandas as pd
import cpca
import pprint as pp
import os.path


# Run the monster!
pd.options.display.max_rows = 999

def adjust_weight(s):    
    # dict for items > 1.2
    available = 0
    more_dict = {}
    for i, v in enumerate(s):
        if v > 1.2:
            # If value is too big, at most we can use is 1.2
            val = min(v - 1.2, 1.2)
            more_dict[i] = val
            available += val
    
    total_deducted = 0
    
    print('available', available)
    # Make item < 1.01 becomes 1.01
    result = list(s)
    for i, v in enumerate(s):
        if v < 1.2:
            needs = 1.02 - v
            if needs < available:
                available -= needs
                v += needs
                total_deducted += needs
                result[i] = v
            else:
                print('No more items available.')
                break

    sorted_d = sorted(more_dict.items(), key=lambda x: x[1])
    for k, v in sorted_d:
        if total_deducted <= 0:
            break
        if v > total_deducted:
            v = total_deducted
        result[k] -= v
        total_deducted -= v
    
    print(result, sum(result))
    return result
    
def run(file_name, write=False):
    if not file_name or not os.path.isfile(file_name):
        return False
    
    df = pd.read_excel(file_name, sheet_name='Input', usecols = "G", header=None,convert_float=True)

    l_of_l = df.values[6:]
    input_data = [round(n[0], 2) for n in l_of_l if not pd.isna(n)]
    #print(input_data)
    results = adjust_weight(input_data)
    print(results)
    
    print('原始重量', sum(input_data))
    print('改好的重量', sum(results))
    
    weight_col = ['','','','','','']
    weight_col.extend(results)
    
    if write:
        base = pd.read_excel(file_name, sheet_name='Input', header=None)
        base['修改重量'] = pd.Series(weight_col)
        base.to_excel('haha2.xls', index=False)
        
    return weight_col

#run('aaa.xlsm', write=True)

def test_run(file_name):
    print('Parsing excel:', file_name)

