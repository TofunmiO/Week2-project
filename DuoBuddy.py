import duolingo
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import os
import getpass
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go  # make sure to pip install
import numpy as np


print('*----------------------------WELCOME TO DUOBUDDY-------------------------------*')
# function to get input from user


def get_input():
    username = str(input("Enter your Username: "))
    password = getpass.getpass("Enter your Password: ")
    return username, password


x = get_input()
info = duolingo.Duolingo(x[0], x[1])
# print(info.get_user_info())


def create_engine_function(users):
    return create_engine('mysql://root:codio@localhost/' + users)


# function to print user full name and info
def get_user_info(info):
    user_information = info.get_user_info()
    full_name = user_information['fullname']
    # get user's full name
    print("Your full name is: ", full_name)
#     return None


get_user_info(info)


# function to print user's languages
def get_user_languages(info):
    languages = info.get_languages(abbreviations=False)
    print("The languages you are currently learning are: ", languages)
#     return None


get_user_languages(info)

friends_info = info.get_friends()


# function to show user language info
def show_language_info(info):
    lang_info = str(input('Which language do you want to more information on?: '))
    details = info.get_language_details(lang_info)
    print('Your current level is: ', details['level'])
    print('Your total points are: ', details['points'])
    print('Your current streak is: ', details['streak'])
    friends_info = info.get_friends()
    friends = str(input(
        'Would you like to see information about your friends? Y or N: '))

    if friends == 'Y':
#         print('Here is your Friend List: ')
#         for index, value in enumerate(friends_info):
#             print(index, value)
        print('')
        print("*--------------------------Here are your DuoBuddies-----------------------------*")
        
        for friend in friends_info:
            if details['points'] <= friend['points']:
                print(friend['username'])
#             if details['points'] < friend['points']:
#                 print('Sorry! You have no DuoBuddy at this time')
#                 print('Try to increase your points and try again!')
#             friend_point = friend['points']

#         for index in friends_point:
#             print(index)
        print("*--------------------------Thank you for using DuoBuddy--------------------------*")
    elif friends == 'N':
        print("*-------------------------You may exit the program now--------------------------*")
        print("*-------------------------Thank you for using DuoBuddy--------------------------*")
#     return None


show_language_info(info)


# function to show user's friends
# def show_friends(info):
#     friends_info = info.get_friends()
#     friends = str(input(
#         'Would you like to see information about your friends? Y or N: '))

#     if friends == 'Y':
#         friend_point =[]
#         print('Here is your Friend List: ')
#         for index, value in enumerate(friends_info):
#             print( index, value)
#         for friend in friends_info():
#             friend_list = friend['points']
#         print("*------------------Thank you for using
#         DuoBuddy------------------*")
#         print("*------------------Here are your DuoB
#         uddies!---------------------*")
# #         if details['points']
#     elif friends == 'N':
#         print("*------------------You may exit th
#         e program now-------------------*")
#         print("*------------------Thank you for us
#         ing DuoBuddy-------------------*")
#     return None


# show_friends(info)


# creating dataframe
def get_df(friends_info):
    # creating data frame to add data to
    col_names = ['id', 'username', 'points']
    df = pd.DataFrame(columns=col_names)
    for friend in friends_info:
        df.loc[len(df.index)] = [friend['id'],
                                 friend['username'], friend['points']]
    
    return df


df = get_df(friends_info)
# turns data from df to csv
df.to_csv('data.csv', index = False)
data = pd.read_csv("data.csv")
# to access data's columns
bPlot = pd.DataFrame(data)
X = list(bPlot.iloc[:, 1])
Y = list(bPlot.iloc[:, 2])
# plot the data as a bar graph
# plt.bar(X, Y, color='g')
# plt.title('Users and their points')
# plt.xlabel('Users')
# plt.ylabel('Points')
# # plt.show()
# plt.write_html('data.html')


fig = go.Figure(data=go.Bar(x=X, y=Y)) # create a figure
fig.write_html('figure.html') # export to HTML file

users = 'users'
user_data = 'user_data'
saved_data = 'saved_data'


# function to write table
def write_table(df, users, user_data):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
              + users + '; "')
    df.to_sql(user_data, con=create_engine_function(users),
              if_exists='replace',
              index=False)


write_table(df, users, user_data)


# function to save database to file named saved_data
def save_file(df, users, user_data, saved_data):
    df.to_sql(user_data, con=create_engine_function(users),
              if_exists='replace', index=False)
    os.system("mysqldump -u root -pcodio {} > {}.sql"
              .format(users, saved_data))


save_file(df, users, user_data, saved_data)


# function to load database
def load(users, saved_data):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
              + users + '; "')
    os.system("mysql -u root -pcodio {} < {}.sql".format(users, saved_data))


#     function to update database
def update_database(users, user_data, saved_data):
    load(users, saved_data)
    # write_table(df, users, user_data, 'append')
    df = pd.read_sql_table(user_data, con=create_engine_function(users))
    return df


df = update_database(users, user_data, saved_data)
