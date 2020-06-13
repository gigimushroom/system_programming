import csv
import chardet
import pandas as pd 
from collections import defaultdict
import json
import codecs


df = pd.read_table("db/id_db.csv")
lines = df.values
        
addr_d = {}
for l in lines:
    tokens = l[0].split(',')
    addr_d[tokens[0]] = tokens[1]
        
print(json.dumps(addr_d, ensure_ascii=False))

with open('id_db.json', 'w', encoding='utf-8') as f:
    json.dump(addr_d, f, ensure_ascii=False, indent=4)