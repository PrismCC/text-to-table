# 从xls文件中读取数据
import pandas as pd

print(pd.read_excel(io='./table/test.xls',sheet_name=0))
print(pd.read_excel(io='./table/test.xls',sheet_name=1))
