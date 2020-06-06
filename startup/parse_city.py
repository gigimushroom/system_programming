import pandas as pd
import cpca
pd.options.display.max_rows = 999
df = pd.read_excel('add_replace.xls', usecols = "J", header=None)

l_of_l = df.values[1:]
# print(l_of_l[0])
location_str = l_of_l[0]

location_str = [str(l[0]) for l in l_of_l]
print(len(location_str))

df = cpca.transform(location_str, cut=False)
#print(df)

print(df[0])