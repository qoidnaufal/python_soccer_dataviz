# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 21:17:21 2023

@author: 62878
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
from highlight_text import fig_text
import numpy as np
import matplotlib.ticker as ticker

df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2022-23 20230206.xlsx')
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

params = ['Touches in box per 90', 'xG per 90',
          'Goals/xG ratio', 'xG/Shot', 'Shots per 90', 'Verticality',
          'Progressive passes p90', 'Accurate crosses, %',
          'Deep completed crosses per 90', 'Deep completions per 90',
          'Shot assists per 90', 'xA per 90',
          'Assists/xA ratio', 'Dribbles completed p90',
          'Progressive runs per 90', 'Fouls suffered per 90',
          'PAdj Sliding tackles', 'PAdj Interceptions',
          'Defensive duels won, %', 'Offensive duels won, %']

minutes_played = 500
position_filter_1 = 'W'
position_filter_2 = 'LAMF'
position_filter_3 = 'RAMF'
nationality = 'Indonesia'
#filtering the position
df_1 = df.loc[(df['Position'].str.contains(position_filter_1)) &
               (df['Minutes played']>=minutes_played)]

df_2 = df.loc[(df['Position'].str.contains(position_filter_2)) &
               (df['Minutes played']>=minutes_played)]

df_3 = df.loc[(df['Position'].str.contains(position_filter_3)) &
               (df['Minutes played']>=minutes_played)]

df_w = pd.concat([df_1,df_2, df_3]).drop_duplicates()
df_w = df_w.loc[df['Passport country'].str.contains(nationality)]
df_w = df_w.set_index('Player')
#df_w = df_w.drop(['E. Vidal', 'M. Osman', 'Yusuf Helal',
                  #'E. Febriansyah', 'S. Arif Munip',
                  #'Sani Riski Fauzi', 'R. Matsumura'])

idx_list = list(df_w.index)

df_w = df_w[params]

# getting z-score & percentile rank
z_score = df_w.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

# Ranking parameters
zscore_mean = z_score.mean(axis=0)
defending = ['PAdj Sliding tackles', 'PAdj Interceptions',
             'Defensive duels won, %']

playmaking = ['Verticality',
              'Progressive passes p90', 'Accurate crosses, %',
              'Deep completed crosses per 90', 'Deep completions per 90',
              'Shot assists per 90', 'xA per 90',
              'Assists/xA ratio']

ballcarrying = ['Dribbles completed p90',
                'Progressive runs per 90',
                'Fouls suffered per 90', 'Offensive duels won, %']

goalscoring = ['Touches in box per 90', 'xG per 90',
               'Goals/xG ratio', 'xG/Shot', 'Shots per 90']

# RANKING
defending_value = z_score[defending].sum(axis=1)
playmaking_value = z_score[playmaking].sum(axis=1)
ballcarrying_value = z_score[ballcarrying].sum(axis=1)
goalscoring_value = z_score[goalscoring].sum(axis=1)

w_rank = pd.concat({'Ball carrying': ballcarrying_value,
                     'Goal scoring': goalscoring_value,
                     'Playmaking': playmaking_value,
                     'Defending': defending_value},axis=1)

w_rank['All rating'] = w_rank.mean(axis=1)

#mf_rank_percentile = mf_rank.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

w_top10 = w_rank.sort_values('All rating', ascending=False).head(10)

w_top10['Playmaking'] = w_top10['Playmaking'].apply(lambda x: x + (math.fabs(w_top10['Playmaking'].min())*1.05))
w_top10['Goal scoring'] = w_top10['Goal scoring'].apply(lambda x: x + (math.fabs(w_top10['Goal scoring'].min())*1.05))
w_top10['Ball carrying'] = w_top10['Ball carrying'].apply(lambda x: x + (math.fabs(w_top10['Ball carrying'].min())*1.05))
w_top10['Defending'] = w_top10['Defending'].apply(lambda x: x + (math.fabs(w_top10['Defending'].min())*1.05))

w_top10 = w_top10.sort_values('All rating')
players_name = list(w_top10.index)

#PLOT PLOT PLOT
rank_param = ['Ball carrying', 'Goal scoring', 'Playmaking', 'Defending']
rank_values = w_top10.loc[players_name, :].values.tolist()
fields = rank_param
colors = ['#1D2F6F', '#8390FA', '#6EAF46', '#FAC748']
labels = players_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(12, 10))

# plot bars
left = len(w_top10) * [0]
for idx, name in enumerate(fields):
    plt.barh(w_top10.index, w_top10[name], left = left, color=colors[idx])
    left = left + w_top10[name]

# title, legend, labels
plt.title('Top 10 Wingers in Liga 1\n', loc='left', size=20, style='oblique')
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
    1.04, 0.12, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()