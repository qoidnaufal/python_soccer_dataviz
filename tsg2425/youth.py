import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

df = pd.read_csv("~/Documents/LearnPython/tsg2425/data/youth_liga1.csv")

# ###################################################
#
#                       CLUBS
#
# ###################################################

liga1 = df.loc[
    df['Competition'].str.contains('BRI Liga 1')
]['Youth Club'].drop_duplicates().to_list()
liga1.append('Malut United')

# ###################################################
#
#                     CLUB Now
#
# ###################################################

club_now = df['Club now'].drop_duplicates().to_list()
club_now.append('Malut United')

# ###################################################
#
#                     Players
#
# ###################################################

players = df['Name'].to_list()
data = {}

for i in range(len(players)):
    dict = {}
    row = df.loc[df['Name'].str.contains(players[i])]
    # data.update({'Name': players[i]})
    dict.update({'Club now': row['Club now'].values[0]}) 
    dict.update({'Pos': row['Pos'].values[0]})
    dict.update({'DOB': row['DOB'].values[0]})
    dict.update({'Minutes': row['Minutes'].values[0]})
    dict.update({'Games': row['Games'].values[0]})
    dict.update({'Youth Club': row['Youth Club'].values[0]})
    data.update(f"{players[i]}": dict)

print(data)
