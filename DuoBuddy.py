import requests
import duolingo
import pandas as pd

def get_input():
    username = str(input("Enter duolingo username: "))
    password = str(input("Enter duolingo password: "))
    return duolingo.Duolingo(username, password)

info = get_input() #user name should be in strings...info
user_information = info.get_user_info()
full_name = user_information['fullname']

print(full_name)
