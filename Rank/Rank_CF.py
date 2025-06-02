# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 21:54:43 2023

@author: 62878
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import os
import glob
import matplotlib.ticker as ticker

competition = "Liga 1"
season = "2024-25"
size = 20
minutes_played = 900
nationality = 'Local' # pick between 'All', 'Local', or 'Foreign'

# load in the data
os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))] # explain for loop & range + len
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

col_list = list(df.columns)
#position_list = df['Position'].tolist()

# parameters adjusment
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)

df['Assists/xA ratio'] = (df['Assists'] / df['xA']).fillna(0)
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['90s played'] = df['Minutes played'] / 90

df['Goals p90'] = df['Goals'] / df['90s played']

df['Total progressive passes'] = df['Progressive passes per 90'] * df['90s played']
df['Completed progressive passes'] = df['Total progressive passes'] * df['Accurate progressive passes, %'] / 100
df['Progressive passes p90'] = df['Completed progressive passes'] / df['90s played']

df['Total dribbles'] = df['Dribbles per 90'] * df['90s played']
df['Successful dribbles'] = df['Total dribbles'] * df['Successful dribbles, %']/100
df['Dribbles completed p90'] = df['Successful dribbles'] / df['90s played']

df['Longpass received ratio'] = df['Received long passes per 90'] / (df['Received passes per 90'] +
                                                                     df['Received long passes per 90'])

params = ['xG per 90', 'Goals p90', 'xG/Shot', 'Goals/xG ratio',
          'Shots per 90', 'Shots on target, %',
          'Touches in box per 90', 'Offensive duels won, %',
          'Aerial duels won, %', 'Progressive passes p90',
          'Shot assists per 90', 'xA per 90', 'Assists/xA ratio',
          'Deep completions per 90', 'Deep completed crosses per 90',
          'Dribbles completed p90',
          'Progressive runs per 90', 'Fouls suffered per 90']

# minute & position filter
position_cf = 'CF'
position_wg = 'W'

#nationality = 'Indonesia'
df = df.loc[
    (df['Position'].str.contains(position_cf))
    & (df['Minutes played'] >= minutes_played)
    & (df['Position'].str.contains('MF') == False)
    # & (df['Position'].str.contains('W') == False)
]
#df = df.loc[df['Passport country'].str.contains(nationality)]
df = df.set_index('Player')
if nationality == 'Local':
               df = df.loc[(df['Passport country'].str.contains('Indonesia'))]
elif nationality == 'Foreign':
               df = df.loc[(df['Passport country'].str.contains('Indonesia') == False)]
#idx_list = list(df.index)

# show parameters-based columns only
df_cf = df[params]

# getting z-score & percentile rank
z_score = df_cf.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

#mean_value = percentile[params].mean(axis=1)


# Ranking parameters
zscore_mean = z_score.mean(axis=0)
playmaking = ['Progressive passes p90', 'Shot assists per 90',
              'xA per 90', 'Assists/xA ratio',
              'Deep completions per 90', 'Deep completed crosses per 90']

goalscoring = ['xG per 90', 'Goals p90', 'xG/Shot', 'Shots per 90', 'Goals/xG ratio',
               'Shots on target, %', 'Touches in box per 90']

ballcarrying = ['Dribbles completed p90',
                'Progressive runs per 90', 'Fouls suffered per 90']

dueling = ['Offensive duels won, %', 'Aerial duels won, %']

# RANKING
playmaking_value = z_score[playmaking].sum(axis=1)
goalscoring_value = z_score[goalscoring].sum(axis=1)
ballcarrying_value = z_score[ballcarrying].sum(axis=1)
duel_value = z_score[dueling].sum(axis=1)

cf_rank = pd.concat({'Goal scoring': goalscoring_value,
                     'Playmaking': playmaking_value,                     
                     'Ball carrying': ballcarrying_value,
                     'Duel': duel_value},axis=1)

#cf_rank['Playmaking'] = cf_rank['Playmaking'].apply(lambda x: x + (math.fabs(cf_rank['Playmaking'].min())*1.05))
#cf_rank['Goal scoring'] = cf_rank['Goal scoring'].apply(lambda x: x + (math.fabs(cf_rank['Goal scoring'].min())*1.05))
#cf_rank['Ball carrying'] = cf_rank['Ball carrying'].apply(lambda x: (x + (math.fabs(cf_rank['Ball carrying'].min())*1.05)))
#cf_rank['Duel'] = cf_rank['Duel'].apply(lambda x: (x + (math.fabs(cf_rank['Duel'].min()))*1.05))

cf_rank['All rating'] = cf_rank.mean(axis=1)

top_cf = cf_rank.sort_values('All rating', ascending=False)

top_cf['Playmaking'] = top_cf['Playmaking'].apply(lambda x: x + (math.fabs(top_cf['Playmaking'].min())*1.05))
top_cf['Goal scoring'] = top_cf['Goal scoring'].apply(lambda x: x + (math.fabs(top_cf['Goal scoring'].min())*1.05))
top_cf['Ball carrying'] = top_cf['Ball carrying'].apply(lambda x: (x + (math.fabs(top_cf['Ball carrying'].min())*1.05)))
top_cf['Duel'] = top_cf['Duel'].apply(lambda x: (x + (math.fabs(top_cf['Duel'].min()))*1.05))

top_cf = top_cf.sort_values('All rating')
players_name = list(top_cf.index)

#PLOT PLOT PLOT
rank_param = ['Goal scoring', 'Playmaking', 'Ball carrying', 'Duel']
rank_values = top_cf.loc[players_name, :].values.tolist()
colors = ['#1D2F6F', '#8390FA', '#6EAF46', '#FAC748']
labels = players_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(13, 9))

# plot bars
left = len(top_cf) * [0]
for idx, name in enumerate(rank_param):
    plt.barh(top_cf.index, top_cf[name], left = left, color=colors[idx])
    left = left + top_cf[name]

# title, legend, labels
plt.title(f'Forwards ranking in Liga 1 {season}\n', loc='left', size=20, style='oblique')
plt.legend(rank_param, bbox_to_anchor=([0.009, 1, 0, 0]), ncol=len(rank_param), frameon=False)

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
