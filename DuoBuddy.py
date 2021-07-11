import duolingo
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import os
import getpass
import csv


# function to get input from user
def get_input():
    username = str(input("Username: "))
    password = getpass.getpass("Password: ")
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
    print("User: ", full_name)
#     return None


get_user_info(info)


# function to print user's languages
def get_user_languages(info):
    languages = info.get_languages(abbreviations=False)
    print("Languages: ", languages)
#     return None


get_user_languages(info)


# function to show user language info
def show_language_info(info):
    lang_info = str(input('What language do you want to work on now?: '))
    details = info.get_language_details(lang_info)
    print('Level:', details['level'])
    print('Points:', details['points'])
    print('Streak:', details['streak'])
#     return None


show_language_info(info)


friends_info = info.get_friends()


# function to show user's friends
def show_friends(info):
    friends_info = info.get_friends()
    friends = str(input(
        'Would you like to see info about your friends? Y or N: '))

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

for friend in friend_info:
    # friends list
    id = friend['id']
    username = friend['username']
    points = friend['points']

    # dictionary of lists
    dict = {'ID' : id, 'Username' : username, 'XP' : points}

    df = pd.DataFrame(dict)

    # saving the dataframe
    df.to_csv('data.csv' , index = False)

    print(df)


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