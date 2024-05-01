# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 12:21:28 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

os.chdir('C:/Users/62878/Documents/Wyscout/League data/Liga 1 - teams')
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
                     'Unnamed: 18':'Ball loses high',
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

league = df.loc[0]['Competition']
year = '2022-23'
team_name = 'PSIS Semarang'
date_ridwan = '2023-01-16'
date_agius = '2023-02-25'

subtitle_string = f"{league} | {year}"
#subtitle_string = f"{league} | starting from {date}"
title_string = 'Playing Style Comparison \n%s' % (subtitle_string)

#odd = df.index[1::2]
#even = df.index[::2]
df_odd = df.loc[1::2].reset_index()
df_odd = df_odd.drop(['index'], axis=1)
df_even = df.loc[::2].reset_index()
df_even = df_even.drop(['index'], axis=1)

df_odd['Opponent'] = df_even['Team']
df_even['Opponent'] = df_odd['Team']
df_odd['xGA'] = df_even['xG']
df_even['xGA'] = df_odd['xG']
df_odd['PPDA against'] = df_even['PPDA']
df_even['PPDA against'] = df_odd['PPDA']

df_2 = pd.concat([df_odd, df_even])
df_2['xG difference'] = df_2['xG'] - df_2['xGA']

# team filter
df_team = df_2.loc[df_2['Team'] == team_name]
df_team = df_team.sort_values(by=['Date'], ascending=True).reset_index()
df_team = df_team.drop(['index'], axis=1)

# new metrics
#ptf3 = df_2['Passes to final third accurate']
#pae = df_2['Penalty area entries']
#bp = df_2['Possession, %']
#dcp = df_2['Deep completed passes']
#dcc = df_2['Deep completed crosses']
#pa = df_2['Positional attacks']
#ca = df_2['Counterattacks']

# attacking efficiency
#df_2['Passes to final third per possession'] = ptf3/bp
#df_2['Penalty area entries per possession'] = pae/bp
#df_2['Penalty area entries per successful final third pass'] = pae/ptf3
#3df_2['Deep completion per possession'] = (dcp+dcc)/bp

# playing style
#df_2['Positional attacks per possession'] = pa/bp
#df_2['Counterattacks per possession'] = ca/bp
#df_2['Positional attacks tendency'] = (pa/(pa+ca))*bp
#df_2['Counterattacks tendency'] = (ca/(ca+pa))/bp

#df_grouped_sum = df_xGA.groupby('Team').sum()
#df_grouped_mean = df_2.groupby('Team').mean()

# date-based filter
#df_date = df_xGA.loc[df_xGA['Date'] >= date]
#df_grouped_sum = df_date.groupby('Team').sum()
#df_grouped_mean = df_date.groupby('Team').mean()

# ingredients
#x_label = df_team['Date'].tolist()
list_opponent = df_team['Opponent'].tolist()
list_xG = df_team['xG'].tolist()
list_xGA = df_team['xGA'].tolist()
