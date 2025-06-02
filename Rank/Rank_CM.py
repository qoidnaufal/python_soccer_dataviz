# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:37:06 2023

@author: 62878
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import os
import glob
import numpy as np
import matplotlib.ticker as ticker

competition = "Liga 1"
season = "2024-25"
size = 33
minutes_played = 900
nationality = 'Local' # pick between 'All', 'Local', or 'Foreign'

# load in the data
os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))] # explain for loop & range + len
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

# parameters adjusment
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)
df['90s played'] = df['Minutes played'] / 90

df['Total progressive passes'] = df['Progressive passes per 90'] * df['90s played']
df['Completed progressive passes'] = df['Total progressive passes'] * df['Accurate progressive passes, %'] / 100
df['Progressive passes p90'] = df['Completed progressive passes'] / df['90s played']

df['Goals p90'] = df['Goals'] / df['90s played']

df['Total passes to f3'] = df['Passes to final third per 90'] * df['90s played']
df['Completed passes to f3'] = df['Total passes to f3'] * df['Accurate passes to final third, %'] / 100
df['Passes to final third p90'] = df['Completed passes to f3'] / df['90s played']

df['Total dribbles'] = df['Dribbles per 90'] * df['90s played']
df['Successful dribbles'] = df['Total dribbles'] * df['Successful dribbles, %']
df['Dribbles completed p90'] = df['Successful dribbles'] / df['90s played']

params = ['xG per 90', 'Goals p90',
          'xG/Shot', 'Shots per 90', 'Touches in box per 90',
          'Passes to final third p90',
          'Progressive passes p90', 'Deep completions per 90',
          'Shot assists per 90', 'xA per 90',
          'Dribbles completed p90', 'Progressive runs per 90',
          'Fouls suffered per 90', 'PAdj Sliding tackles',
          'PAdj Interceptions', 'Defensive duels won, %',
          'Aerial duels won, %', 'Offensive duels won, %']

position_include = ['CMF', 'AMF', 'DMF']

# print(list(df.columns))

#position_exclude = 'W'
df0 = df.loc[(df['Position'].str.contains(position_include[0]))
               & (df['Minutes played']>=minutes_played)
               & (df['Position'].str.contains('W')==False)
               ]
df1 = df.loc[(df['Position'].str.contains(position_include[1]))
               & (df['Minutes played']>=minutes_played)
               & (df['Position'].str.contains('W')==False)
               ]
df2 = df.loc[(df['Position'].str.contains(position_include[2]))
               & (df['Minutes played']>=minutes_played)
               & (df['Position'].str.contains('W')==False)
               ]
df = pd.concat([df0, df1, df2]).drop_duplicates()
df = df.set_index('Player')
if nationality == 'Local':
               df = df.loc[(df['Passport country'].str.contains('Indonesia'))]
elif nationality == 'Foreign':
               df = df.loc[(df['Passport country'].str.contains('Indonesia') == False)]

# show parameters-based columns only
df_mf = df[params]
#dfmf_mean = df_mf.mean(axis=0)

# getting z-score & percentile rank
z_score = df_mf.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

#mean_value = percentile[params].mean(axis=1)


# Ranking parameters
zscore_mean = z_score.mean(axis=0)
playmaking = ['Passes to final third p90',
               'Progressive passes p90','Deep completions per 90',
               'Deep completions per 90', 'Shot assists per 90',
               'xA per 90']

#, 'Assists/xA ratio'

goalscoring = ['xG/Shot', 'Goals p90', 'Shots per 90',
                'Touches in box per 90']

# 'Goals/xG ratio',

ballcarrying = ['Dribbles completed p90', 'Progressive runs per 90',
                 'Fouls suffered per 90']

defending = ['PAdj Sliding tackles', 'PAdj Interceptions',
              'Defensive duels won, %', 'Aerial duels won, %']

# RANKING
playmaking_value = z_score[playmaking].sum(axis=1)
goalscoring_value = z_score[goalscoring].sum(axis=1)
ballcarrying_value = z_score[ballcarrying].sum(axis=1)
defending_value = z_score[defending].sum(axis=1)

mf_rank = pd.concat({'Playmaking': playmaking_value,
                     'Goal scoring': goalscoring_value,
                     'Ball carrying': ballcarrying_value,
                     'Defending': defending_value},axis=1)

mf_rank['All rating'] = mf_rank.mean(axis=1)

#mf_rank_percentile = mf_rank.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

mf_top10 = mf_rank.sort_values('All rating', ascending=False).head(size)

mf_top10['Playmaking'] = mf_top10['Playmaking'].apply(lambda x: x + (math.fabs(mf_top10['Playmaking'].min())*1.05))
mf_top10['Goal scoring'] = mf_top10['Goal scoring'].apply(lambda x: x + (math.fabs(mf_top10['Goal scoring'].min())*1.05))
mf_top10['Ball carrying'] = mf_top10['Ball carrying'].apply(lambda x: x * 0.5) # + (math.fabs(mf_top10['Ball carrying'].min())*1.05))
mf_top10['Defending'] = mf_top10['Defending'].apply(lambda x: x + (math.fabs(mf_top10['Defending'].min())*1.05))

mf_top10 = mf_top10.sort_values('All rating')
players_name = list(mf_top10.index)

#PLOT PLOT PLOT
rank_param = ['Playmaking', 'Goal scoring', 'Ball carrying', 'Defending']
rank_values = mf_top10.loc[players_name, :].values.tolist()
fields = rank_param
colors = ['#1D2F6F', '#8390FA', '#6EAF46', '#FAC748']
labels = players_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(13, 9))

# plot bars
left = len(mf_top10) * [0]
for idx, name in enumerate(fields):
    plt.barh(mf_top10.index, mf_top10[name], left = left, color=colors[idx])
    left = left + mf_top10[name]

# title, legend, labels
plt.title(f'{nationality} Top {size} Midfielders in Liga 1 {season}\n', loc='left', size=20, style='oblique')
plt.legend(fields, bbox_to_anchor=([0.009, 1, 0, 0]), ncol=len(rank_param), frameon=False)
#plt.xlabel('Percentile value')

# remove spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

#remove those stupid numbers below
ax.xaxis.set_major_locator(ticker.NullLocator())

# add credits
CREDIT_1 = "data: wyscout"
CREDIT_2 = "viz by: Qoid Naufal"
CREDIT_3 = 'minimum minutes played = %s' % (minutes_played)

fig.text(
    0.85, 0.12, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()
