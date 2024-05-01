# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 21:54:43 2023

@author: 62878
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager
import matplotlib.ticker as ticker

# load in the data
df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2022-23 20230206.xlsx')

col_list = list(df.columns)
#position_list = df['Position'].tolist()

# parameters adjusment
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)

df['Assists/xA ratio'] = (df['Assists'] / df['xA']).fillna(0)
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['90s played'] = df['Minutes played'] / 90

df['Total progressive passes'] = df['Progressive passes per 90'] * df['90s played']
df['Completed progressive passes'] = df['Total progressive passes'] * df['Accurate progressive passes, %'] / 100
df['Progressive passes p90'] = df['Completed progressive passes'] / df['90s played']

df['Total dribbles'] = df['Dribbles per 90'] * df['90s played']
df['Successful dribbles'] = df['Total dribbles'] * df['Successful dribbles, %']/100
df['Dribbles completed p90'] = df['Successful dribbles'] / df['90s played']

df['Longpass received ratio'] = df['Received long passes per 90'] / (df['Received passes per 90'] +
                                                                     df['Received long passes per 90'])

params = ['xG per 90', 'xG/Shot', 'Goals/xG ratio',
          'Shots per 90', 'Shots on target, %',
          'Touches in box per 90', 'Offensive duels won, %',
          'Aerial duels won, %', 'Progressive passes p90',
          'Shot assists per 90', 'xA per 90', 'Assists/xA ratio',
          'Deep completions per 90', 'Deep completed crosses per 90',
          'Dribbles completed p90',
          'Progressive runs per 90', 'Fouls suffered per 90']

# minute & position filter
minutes_played = 500
season = '2022-23'
position_filter = 'CF'
#nationality = 'Indonesia'
df = df.loc[(df['Position'].str.contains(position_filter)) &
               (df['Minutes played']>=minutes_played)]
#df = df.loc[df['Passport country'].str.contains(nationality)]
df = df.set_index('Player')
df = df.drop(['M. Ferdinan', 'J. Bustos', 'Lulinha', 'Privat Mbarga',
              'Renan Silva', 'Sani Riski Fauzi', 'Rizky Pora'])
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

goalscoring = ['xG per 90', 'xG/Shot', 'Shots per 90', 'Goals/xG ratio',
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

cf_top10 = cf_rank.sort_values('All rating', ascending=False).head(10)

cf_top10['Playmaking'] = cf_top10['Playmaking'].apply(lambda x: x + (math.fabs(cf_top10['Playmaking'].min())*1.05))
cf_top10['Goal scoring'] = cf_top10['Goal scoring'].apply(lambda x: x + (math.fabs(cf_top10['Goal scoring'].min())*1.05))
cf_top10['Ball carrying'] = cf_top10['Ball carrying'].apply(lambda x: (x + (math.fabs(cf_top10['Ball carrying'].min())*1.05)))
cf_top10['Duel'] = cf_top10['Duel'].apply(lambda x: (x + (math.fabs(cf_top10['Duel'].min()))*1.05))

cf_top10 = cf_top10.sort_values('All rating')
players_name = list(cf_top10.index)

#PLOT PLOT PLOT
rank_param = ['Goal scoring', 'Playmaking', 'Ball carrying', 'Duel']
rank_values = cf_top10.loc[players_name, :].values.tolist()
fields = rank_param
colors = ['#1D2F6F', '#8390FA', '#6EAF46', '#FAC748']
labels = players_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(12, 10))

# plot bars
left = len(cf_top10) * [0]
for idx, name in enumerate(fields):
    plt.barh(cf_top10.index, cf_top10[name], left = left, color=colors[idx])
    left = left + cf_top10[name]

# title, legend, labels
plt.title('Top 10 Strikers in Liga 1\n', loc='left', size=20, style='oblique')
plt.legend(fields, bbox_to_anchor=([0.55, 1, 0, 0]), ncol=4, frameon=False)
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
    1.01, 0.12, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()