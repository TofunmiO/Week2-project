import pandas as pd
import DuoBuddy.py

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

