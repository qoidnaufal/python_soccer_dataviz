# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 16:41:07 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

competition = "Liga 1"
season = "2022-23"

team_name = 'Persebaya Surabaya'
rolling_average = 4

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.loc[(df['Match'].str.contains('nan')==False)]
df = df.reset_index()
df = df.drop(['index'], axis=1)


df.rename(columns = {
    'Shots / on target':'Shots',
    'Unnamed: 9':'Shots on target',
    'Unnamed: 10':'Shots accurate %',
    'Passes / accurate':'Passes',
    'Unnamed: 12':'Passes completed',
    'Unnamed: 13':'Passes accurate %',
    'Losses / Low / Medium / High':'Ball losses',
    'Unnamed: 16':'Ball losses low',
    'Unnamed: 17':'Ball losses medium',
    'Unnamed: 18':'Ball losses high',
    'Recoveries / Low / Medium / High':'Recoveries',
    'Unnamed: 20':'Recoveries low',
    'Unnamed: 21':'Recoveries medium',
    'Unnamed: 22':'Recoveries high',
    'Duels / won':'Duels',
    'Unnamed: 24':'Duels won',
    'Unnamed: 25':'Duels won %',
    'Shots from outside penalty area / on target':'Shots from outside penalty area',
    'Unnamed: 27':'Shots from outside penalty area on target',
    'Unnamed: 28':'Shots from outside penalty area accurate %',
    'Positional attacks / with shots':'Positional attacks',
    'Unnamed: 30':'Positional attacks with shots',
    'Unnamed: 31': 'Positional attacks with shots %',
    'Counterattacks / with shots':'Counterattacks',
    'Unnamed: 33':'Counterattacks with shots',
    'Unnamed: 34': 'Counterattacks with shots %',
    'Set pieces / with shots': 'Set pieces',
    'Unnamed: 36':'Set pieces with shots',
    'Unnamed: 37':'Set pieces with shots %',
    'Corners / with shots':'Corners',
    'Unnamed: 39': 'Corners with shots',
    'Unnamed: 40': 'Corners with shots %',
    'Free kicks / with shots':'Free kicks',
    'Unnamed: 42':'Free kicks with shots',
    'Unnamed: 43':'Free kicks with shots %',
    'Penalties / converted':'Penalties',
    'Unnamed: 45':'Penalties converted',
    'Unnamed: 46':'Penalties converted %',
    'Crosses / accurate':'Crosses',
    'Unnamed: 48':'Crosses accurate',
    'Unnamed: 49':'Crosses accurate %',
    'Penalty area entries (runs / crosses)':'Penalty area entries',
    'Unnamed: 53':'Penalty area entries via runs',
    'Unnamed: 54': 'Penalty area entries via crosses',
    'Offensive duels / won':'Offensive duels',
    'Unnamed: 57':'Offensive duels won',
    'Unnamed: 58':'Offensive duels won %',
    'Shots against / on target':'Shots conceded',
    'Unnamed: 62':'Shots conceded on target',
    'Unnamed: 63':'Shots conceded on target %',
    'Defensive duels / won':'Defensive duels',
    'Unnamed: 65':'Defensive duels won',
    'Unnamed: 66':'Defensive duels won %',
    'Aerial duels / won':'Aerial duels',
    'Unnamed: 68':'Aerial duels won',
    'Unnamed: 69':'Aerial duels won %',
    'Sliding tackles / successful':'Tackles',
    'Unnamed: 71':'Tackles success',
    'Unnamed: 72':'Tackles success %',
    'Forward passes / accurate':'Forward passes',
    'Unnamed: 79':'Forward passes accurate',
    'Unnamed: 80':'Forward passes accurate %',
    'Back passes / accurate':'Back passes',
    'Unnamed: 82':'Back passes accurate',
    'Unnamed: 83':'Back passes accurate %',
    'Lateral passes / accurate':'Lateral passes',
    'Unnamed: 85':'Lateral passes accurate',
    'Unnamed: 86':'Lateral passes accurate %',
    'Long passes / accurate':'Long passes',
    'Unnamed: 88':'Long passes accurate',
    'Unnamed: 89':'Long passes accurate %',
    'Passes to final third / accurate':'Passes to final third',
    'Unnamed: 91':'Passes to final third accurate',
    'Unnamed: 92':'Passes to final third accurate %',
    'Progressive passes / accurate':'Progressive passes',
    'Unnamed: 94':'Progressive passes accurate',
    'Unnamed: 95':'Progressive passes accurate %',
    'Smart passes / accurate':'Smart passes',
    'Unnamed: 97':'Smart passes accurate',
    'Unnamed: 98':'Smart passes accurate %',
    'Throw ins / accurate':'Throw ins',
    'Unnamed: 100':'Throw ins accurate',
    'Unnamed: 101':'Throw ins accurate %'
    }, inplace = True)

col_list = list(df.columns)

# team filter

title_string = '%s xG vs xGA Performance' % (team_name)
subtitle_string = f'Rolling average every {rolling_average} games | {competition} {season} | data from wyscout'

df_odd = df.loc[1::2].reset_index()
df_odd = df_odd.drop(['index'], axis=1)
df_even = df.loc[::2].reset_index()
df_even = df_even.drop(['index'], axis=1)

df_odd['Opponent'] = df_even['Team']
df_even['Opponent'] = df_odd['Team']
df_odd['xGA'] = df_even['xG']
df_even['xGA'] = df_odd['xG']

df_2 = pd.concat([df_odd, df_even])

df_2['xG difference'] = df_2['xG'] - df_2['xGA']
df_2['Goals difference'] = df_2['Goals'] - df_2['Conceded goals']

df_2 = df_2.sort_values(by=(['Date', 'Match']), ascending=True).reset_index()
df_2 = df_2.drop(['index'], axis=1)

team_home = df_2['Match'].str.split('-').str[0]
team_list = df_2['Match'].str.split('-').str[1]
team_away = team_list.str.split().str[0]
df_2['Home'] = team_home

df_team = df_2.loc[df_2['Team'] == team_name]

df_team['xG_rolling'] = df_team.xG.rolling(rolling_average).mean()
df_team['xGA_rolling'] = df_team.xGA.rolling(rolling_average).mean()

# data to plot
x = df_team['Date']
y1 = df_team['xG_rolling']
y2 = df_team['xGA_rolling']

x = np.array(x)
y1 = np.array(y1)
y2 = np.array(y2)

# set the canvas
fig, ax = plt.subplots(figsize = (20,8), facecolor='black')
ax.set_facecolor('black')
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
#ax.get_xaxis().set_ticks([])
  
# plot the data
plt.plot(x, y1, color = 'blue', linewidth=3)
plt.plot(x, y2, color = 'red', linewidth=3)

ax.fill_between(x, y1, y2, where=y1>y2, facecolor='blue', alpha=0.6, interpolate=True)
ax.fill_between(x, y1, y2, where=y1<y2, facecolor='red', alpha=0.6, interpolate=True)

plt.xticks(rotation = 'vertical')

plt.suptitle(title_string, y=0.945, color='white', fontsize=22)
plt.title(subtitle_string, x=0.484, color='white', fontsize=12)

plt.legend(["xG", "xGA"], loc ="lower right")
ax.set_ylabel('xG & xGA', color='white', size='14', labelpad=12)

plt.show()