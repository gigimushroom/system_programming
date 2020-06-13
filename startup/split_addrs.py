import pandas as pd
import cpca

pd.options.display.max_rows = 999

def run(input, ouput):
    
    base = pd.read_excel(input, header=None)

    df = pd.read_excel(input, usecols = "J", header=None)

    l_of_l = df.values[1:]
    location_str = [str(l[0]) for l in l_of_l]
    #print(location_str)

    cp = cpca.transform(location_str, cut=False)

    prov = [v[0] for v in cp.values]
    city = [v[1] for v in cp.values]
    area = [v[2] for v in cp.values]
    #print(prov)

    base['新的省'] = [''] + prov
    base['新的市'] = [''] + city
    base['新的区'] = [''] + area
    base.to_excel(ouput, index=False)
    
    return True