import pandas as pd


file1  = 'employees_practice.xlsx'

sheet1 = pd.read_excel(file1)
print(sheet1)