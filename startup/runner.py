import addr_converter as ad
import pandas as pd
import id_converter as id_c
import split_addrs as sp

def remove_addr_and_id_dup(input, output='haha.xls'):
    addr_col_data, num_col_data = ad.run(input)
    name_col, id_col = id_c.run(input)
    
    base = pd.read_excel(input, sheet_name='Input', header=None)
    base['替换地址'] = pd.Series(addr_col_data)
    base['替换电话'] = pd.Series(num_col_data)
    base['替换姓名'] = pd.Series(name_col)
    base['替换身份证'] = pd.Series(id_col)
    base.to_excel(output, index=False)
    
    return True
    
def split_addr(input, output='splitted.xls'):
    return sp.run(input, output)
    
#remove_addr_and_id_dup('aaa.xlsm')