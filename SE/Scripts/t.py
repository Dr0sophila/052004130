import pandas as pd

d = pd.read_excel('../1.xlsx', sheet_name="每日确诊")
a=d.iloc[:,34:37]
a=a.diff(periods=-1)
d=d.drop(['香港',"澳门","台湾"], axis=1)
d=pd.concat([d,a],axis=1)
print(d)
