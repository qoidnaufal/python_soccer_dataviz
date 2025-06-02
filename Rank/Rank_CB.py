# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 17:37:04 2023

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
season = "2022-23"
size = 20
minutes_played = 900

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))] # explain for loop & range + len
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

col_list = list(df.columns)
position_list = df['Position'].tolist()

# parameters adjusment
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)
df['Verticality'] = df['Forward passes per 90']/(df['Forward passes per 90'] +
                                                 df['Lateral passes per 90'] +
                                                 df['Back passes per 90'])

df['Assists/xA ratio'] = (df['Assists'] / df['xA']).fillna(0)
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['90s played'] = df['Minutes played'] / 90

df['Total progressive passes'] = df['Progressive passes per 90'] * df['90s played']
df['Completed progressive passes'] = df['Total progressive passes'] * df['Accurate progressive passes, %'] / 100
df['Progressive passes p90'] = df['Completed progressive passes'] / df['90s played']

df['Total passes to f3'] = df['Passes to final third per 90'] * df['90s played']
df['Completed passes to f3'] = df['Total passes to f3'] * df['Accurate passes to final third, %'] / 100
df['Passes to final third p90'] = df['Completed passes to f3'] / df['90s played']

df['Total dribbles'] = df['Dribbles per 90'] * df['90s played']
df['Successful dribbles'] = df['Total dribbles'] * df['Successful dribbles, %']
df['Dribbles completed p90'] = df['Successful dribbles'] / df['90s played']

params = ['Defensive duels won, %', 'Aerial duels won, %',
          'PAdj Sliding tackles', 'PAdj Interceptions',
          'Fouls per 90',
          'Accurate long passes, %', 'Verticality',
          'Passes to final third p90', 'Progressive passes p90',
          'Dribbles completed p90', 'Progressive runs per 90',
          'Goals/xG ratio', 'xG/Shot'
          ]

position_filter = 'CB'
#nationality = 'Indonesia'
df = df.loc[(df['Position'].str.contains(position_filter)) &
               (df['Minutes played']>=minutes_played)]
#df = df.loc[df['Passport country'].str.contains(nationality)]
df = df.set_index('Player')
# df = df.drop(['A. Figo', 'A. Tanjung', 'Y. Sayuri'])
#idx_list = list(df.index)

# show parameters-based columns only
df_cb = df[params]
#dfmf_mean = df_mf.mean(axis=0)

# getting z-score & percentile rank
z_score = df_cb.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

#mean_value = percentile[params].mean(axis=1)


# Ranking parameters
zscore_mean = z_score.mean(axis=0)
defending = ['Defensive duels won, %', 'Aerial duels won, %',
             'PAdj Sliding tackles', 'PAdj Interceptions','Fouls per 90']

playmaking = ['Accurate long passes, %', 'Verticality',
              'Passes to final third p90', 'Progressive passes p90']

ballcarrying = ['Dribbles completed p90', 'Progressive runs per 90']

goalscoring = ['xG/Shot']

# RANKING
defending_value = z_score[defending].sum(axis=1)
playmaking_value = z_score[playmaking].sum(axis=1)
ballcarrying_value = z_score[ballcarrying].sum(axis=1)
# goalscoring_value = z_score[goalscoring].sum(axis=1)

cb_rank = pd.concat({'Defending': defending_value,
                     'Playmaking': playmaking_value,
                     'Ball carrying': ballcarrying_value,
                     # 'Goal scoring': goalscoring_value
                 }, axis=1)

cb_rank['All rating'] = cb_rank.mean(axis=1)

# mf_rank_percentile = mf_rank.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

top_cb = cb_rank.sort_values('All rating', ascending=False).head(size)
# top_cb = cb_rank.sort_values('Defending', ascending=False).head(size)

top_cb['Playmaking'] = top_cb['Playmaking'].apply(lambda x: x + (math.fabs(top_cb['Playmaking'].min())*1.05))
# top_cb['Goal scoring'] = top_cb['Goal scoring'].apply(lambda x: x + (math.fabs(top_cb['Goal scoring'].min())*1.05))
top_cb['Ball carrying'] = top_cb['Ball carrying'].apply(lambda x: x + (math.fabs(top_cb['Ball carrying'].min())*1.05))
top_cb['Defending'] = top_cb['Defending'].apply(lambda x: x + (math.fabs(top_cb['Defending'].min())*1.05))

top_cb = top_cb.sort_values('All rating')
# top_cb = top_cb.sort_values('Defending')
players_name = list(top_cb.index)

#PLOT PLOT PLOT
rank_param = [
    'Defending',
    'Playmaking',
    'Ball carrying',
    # 'Goal scoring'
]
rank_values = top_cb.loc[players_name, :].values.tolist()
colors = [
    '#1D2F6F',
    '#8390FA',
    '#FFA500',
    # '#FAC748'
]
labels = players_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(14, 8))

# plot bars
left = len(top_cb) * [0]
for idx, category in enumerate(rank_param):
    plt.barh(top_cb.index, top_cb[category], left = left, color=colors[idx])
    left = left + top_cb[category]

# title, legend, labels
plt.title(f'Top {size} Centerbacks in Liga 1\n', loc='left', size=20, style='oblique')
plt.legend(rank_param, bbox_to_anchor=([0.55, 1, 0, 0]), ncol=len(rank_param), frameon=False)

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
    0.99, 0.12, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()
