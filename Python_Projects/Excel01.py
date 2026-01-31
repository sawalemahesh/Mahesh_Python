import textwrap

import pandas as pd
from attr.setters import convert

file1= 'employees.xlsx'

# sheet1 = pd.read_excel(file1, sheet_name="Personal_Details")
sheet2 = pd.read_excel(file1, sheet_name="Salary_Details")

# print(sheet1,'\n')
print(sheet2,'\n')
# print(sheet2.head())

s1 = sheet2[sheet2["Salary"] > 20000]
print(s1)

output_file = "filtered_employees.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    s1.to_excel(writer, sheet_name="20000", index=False)
    # it_department_df.to_excel(writer, sheet_name="IT_Department", index=False)

print("Filtered data saved successfully to filtered_employees.xlsx")
sheet2.to_json("employees.json", orient="records", indent=4)
