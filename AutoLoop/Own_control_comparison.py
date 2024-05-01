# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 19:10:59 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

competition = 'Liga 1'
season = '2022-23'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.loc[(df['Match'].str.contains('nan')==False)]
df = df.reset_index()
df = df.drop(['index'], axis=1)


df.rename(columns = {'Shots / on target':'Shots',
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
                     'Unnamed: 91':'Passes to final third completed',
                     'Unnamed: 92':'Passes to final third accurate %',
                     'Progressive passes / accurate':'Progressive passes',
                     'Unnamed: 94':'Progressive passes completed',
                     'Unnamed: 95':'Progressive passes accurate %',
                     'Smart passes / accurate':'Smart passes',
                     'Unnamed: 97':'Smart passes completed',
                     'Unnamed: 98':'Smart passes accurate %',
                     'Throw ins / accurate':'Throw ins',
                     'Unnamed: 100':'Throw ins accurate',
                     'Unnamed: 101':'Throw ins accurate %'                     
                     }, inplace = True)

col_list = list(df.columns)

# team filter
team_name = 'Persija'

# data to plot
x_value = 'Date'

y1 = 'Progressive passes completed'
y1_control = 'Possession, %'
y1_value = f'{y1} per {y1_control}'
y1_color = 'blue'

y2 = f'Opponent {y1}'
y2_control = f'Opponent {y1_control}'
y2_value = f'{y2} per {y2_control}'
y2_color = 'red'

rolling_average = 4

title_string = f'{team_name} {y1_value} \nvs {y2_value}'
subtitle_string = 'rolling average every %s games | Liga 1 2022-23 | data from wyscout' % (rolling_average)
#subtitle_string = 'Piala Presiden 2022 | data from wyscout | @novalaziz'

df_odd = df.loc[1::2].reset_index()
df_odd = df_odd.drop(['index'], axis=1)
df_even = df.loc[::2].reset_index()
df_even = df_even.drop(['index'], axis=1)

df_odd['Opponent'] = df_even['Team']
df_even['Opponent'] = df_odd['Team']

df_odd[y2] = df_even[y1]
df_even[y2] = df_odd[y1]
df_odd[f'Opponent {y1_control}'] = df_even[y1_control]
df_even[f'Opponent {y1_control}'] = df_odd[y1_control]

df_2 = pd.concat([df_odd, df_even])

# average progressive passes per game each team

df_2 = df_2.sort_values(by=(['Date', 'Match']), ascending=True).reset_index()
df_2 = df_2.drop(['index'], axis=1)

grouped_opponent = df_2.groupby('Opponent').mean()
grouped_opponent[y2_value] = grouped_opponent[y2] / grouped_opponent[y2_control]
grouped_opponent = grouped_opponent.loc[:, y2_value]

#grouped_opponent.loc[team_name]

grouped_team = df_2.groupby(['Team','Date','Opponent']).mean()
grouped_team = grouped_team.reset_index()
grouped_team = grouped_team.loc[grouped_team['Team'] == team_name]
grouped_team[y1_value] = grouped_team[y1] / grouped_team[y1_control]

grouped_team[y2_value] = [grouped_opponent.loc[i] for i in zip(grouped_team['Opponent'])]

df_team = df_2.loc[df_2['Team'] == team_name]

x = np.array(grouped_team[x_value])
y1 = np.array(grouped_team[y1_value].rolling(rolling_average).mean())
y2 = np.array(grouped_team[y2_value].rolling(rolling_average).mean())

# set the canvas
fig, ax = plt.subplots(figsize = (20,8), facecolor='black')
ax.set_facecolor('black')
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
#ax.get_xaxis().set_ticks([])
  
# plot the data
plt.plot(x, y1, color = y1_color, linewidth=3)
plt.plot(x, y2, color = y2_color, linewidth=3)

ax.fill_between(x, y1, y2, where=y1>y2, facecolor=y1_color, alpha=0.6, interpolate=True)
ax.fill_between(x, y1, y2, where=y1<y2, facecolor=y2_color, alpha=0.6, interpolate=True)

plt.xticks(rotation = 'vertical')

plt.suptitle(title_string, y=0.99, color='white', fontsize=22)
plt.title(subtitle_string, x=0.484, color='white', fontsize=12)

plt.legend([y1_value, y2_value], loc ="lower right")
ax.set_ylabel(f'{y1_value} & \n{y2_value}', color='white', size='14', labelpad=12)

plt.show()