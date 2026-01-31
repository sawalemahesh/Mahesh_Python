from datetime import date

DD= int(input("Enter Date:"))
Month = int(input("Enter Month:"))
Year = int(input("Enter Year:"))
print(f"{DD}/{Month}/{Year}")

limit = 1800

if Year < limit:
    print("Year cannot be greater than limit")
else:
    current_year = date.today().year
    print(current_year)
    current_month = date.today().month
    current_day = date.today().day
    print(current_month, current_day)

    Age = current_year -Year , current_month -Month, current_day -DD
