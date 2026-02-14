import os
import random

import dotenv
from dotenv import load_dotenv

class BankManagementSystem:
    def __init__(self, account_name, account_number, account_password, account_email, mobile_number):
        self.account_name = account_name
        self._account_number = account_number
        self._account_password = account_password
        self.account_email = account_email
        self.mobile_number = mobile_number

    def getdata(self):
        self.account_name = input("Enter account name: ").strip()
        self.account_email = input("Enter account email: ").strip()
        self.mobile_number = str(input("Enter mobile number: ")).strip()
        self.account_password = input("Enter password: ").strip()
        self.account_number = input("Enter account number: ").strip()
        load_dotenv(".env")

        os.write(dotenv, 'self.account_name = {}'.format(self.account_name))
        os.write(dotenv, 'self.account_email = {}'.format(self.account_email))
        os.write(dotenv, 'self.account_password = {}'.format(self.account_password))
        os.write(dotenv, 'self.account_number = {}'.format(self.account_number))
        os.write(dotenv, 'self.mobile_number = {}'.format(self.mobile_number))

#
# class CustomerData:
#     def login(self):
#         load_dotenv(".env")
#
#         env_user = os.getenv("customername")
#         env_pass = os.getenv("password")
#
#         user = input("Enter customername: ").strip()
#         pwd = input("Enter password: ").strip()
#
#         if user == env_user and pwd == env_pass:
#             print("Login Successful ✅")
#         else:
#             print("Invalid Credentials ❌")


if __name__ == "__main__":
    BankManagementSystem('Mahesh', 23345666, 'abc@123', 'abc@gmail.com', 9998877665).getdata()

