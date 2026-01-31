import pandas as pd
import xlsxwriter
import openpyxl

file1= 'employees_practice.xlsx'

open = pd.read_excel(file1, sheet_name="Employee_Data")
open2 = pd.read_excel(file1, sheet_name="Salary_Details")
print(open, '\n')

merged = pd.merge(open, open2, on="Emp_ID", how="outer")
print(merged)

# sort = open[open['Department']=='IT']
# print(sort, '\n')
# sal =open[open['Salary'] > 50000]
# print(sal, '\n')
#
File1 = 'updatedsheet.xlsx'

with pd.ExcelWriter(File1, engine="openpyxl") as writer:
    merged.to_excel(writer, sheet_name="IT", index=False)






