import requests
import duolingo
import json
import mysql.connector
from mysql.connector import Error
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

base_url = 'https://www.duolingo.com/api/1'

#function to get input from user
def get_input():
    username = str(input("Username: "))
    password = str(input("Password: "))
    return duolingo.Duolingo(username, password)

info = get_input()

#function to connect to mysql server
def connect_server(localhost, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection successful")
    except Error as err:
         print(f"Error: '{err}'")
            
    return connection

#connect_server()
    
#function to print user full name and info
def get_user_info(info):
    user_information = info.get_user_info()
    full_name = user_information['fullname']
    #get user's full name
    print("User: " , full_name)
    return None

get_user_info(info)

# function to print user's languages
def get_user_languages(info):
    languages = info.get_languages(abbreviations=False)
    print("Languages: " , languages)
    return None

get_user_languages(info)

# function to show user language info
def show_language_info(info):
    lang_info = str(input('What language do you want to work on now?: '))
    details = info.get_language_details(lang_info)
    print('Level:', details['level'])
    print('Points:', details['points'])
    print('Streak:', details['streak'])
    return None

show_language_info(info)

# function to show user's friends
def show_friends(info):
    friends_info = info.get_friends()
    friends = str(input('Would you like to see info about your friends? Y or N: '))

    if friends == 'Y':
        for index, value in enumerate(friends_info):
            print(index, value)
        # for loop to get total xp of user's friends
        for friend in friends_info:
            print(friend['points'])
    elif friends == 'N':
        print("You may exit the program now")
    return None
        
show_friends(info)