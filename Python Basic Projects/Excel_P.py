import openpyxl
import pandas as pd

file1 = 'Practice_Data.xlsx'

sheet1 = pd.read_excel(file1, sheet_name='Sales_Data')
print(sheet1)

sheet2 = pd.read_excel(file1, sheet_name='Employee_Data')
print(sheet2)

sheet3 = pd.read_excel(file1, sheet_name='Student_Data')
print(sheet3)

