# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 22:27:07 2023

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
#col_list = list(df.columns)
#position_list = df['Position'].tolist()

#parameters adjustment
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



params = ['Offensive duels won, %', 'Touches in box per 90', 'xG per 90',
          'Goals/xG ratio', 'Passes to final third p90',
          'Progressive passes p90', 'Accurate crosses, %',
          'Deep completed crosses per 90', 'Deep completions per 90',
          'Shot assists per 90', 'xA per 90',
          'Assists/xA ratio', 'Dribbles completed p90',
          'Progressive runs per 90', 'Fouls suffered per 90',
          'Fouls per 90', 'PAdj Sliding tackles', 'PAdj Interceptions',
          'Aerial duels won, %','Defensive duels won, %']

minutes_played = 500
position_filter_1 = 'RB'
position_filter_2 = 'LB'
position_filter_3 = 'WB'

#filtering the position
df_1 = df.loc[(df['Position'].str.contains(position_filter_1)) &
               (df['Minutes played']>=minutes_played)]

df_2 = df.loc[(df['Position'].str.contains(position_filter_2)) &
               (df['Minutes played']>=minutes_played)]

df_3 = df.loc[(df['Position'].str.contains(position_filter_3)) &
               (df['Minutes played']>=minutes_played)]

df_fb = pd.concat([df_1,df_2, df_3]).drop_duplicates()

df_fb = df_fb.set_index('Player')
idx_list = list(df_fb.index)
df_fb = df_fb.drop(['R. Simanjuntak', 'M. Sihran', 'Y. Sayuri'])

df_fb = df_fb[params]

# getting z-score & percentile rank
z_score = df_fb.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

#mean_value = percentile[params].mean(axis=1)


# Ranking parameters
zscore_mean = z_score.mean(axis=0)
playmaking = ['Passes to final third p90', 'Progressive passes p90',
              'Accurate crosses, %', 'Deep completed crosses per 90',
              'Deep completions per 90', 'Shot assists per 90',
              'xA per 90', 'Assists/xA ratio']

attacking = ['Offensive duels won, %', 'Touches in box per 90',
             'xG per 90']

ballcarrying = ['Dribbles completed p90', 'Progressive runs per 90',
                'Fouls suffered per 90']

defending = ['Fouls per 90', 'PAdj Sliding tackles',
             'PAdj Interceptions','Aerial duels won, %',
             'Defensive duels won, %']

# RANKING
playmaking_value = z_score[playmaking].sum(axis=1)
attacking_value = z_score[attacking].sum(axis=1)
ballcarrying_value = z_score[ballcarrying].sum(axis=1)
defending_value = z_score[defending].sum(axis=1)

fb_rank = pd.concat({'Defending': defending_value,
                     'Playmaking': playmaking_value,
                     'Ball carrying': ballcarrying_value,
                     'Attacking': attacking_value
                     },axis=1)

fb_rank['All rating'] = fb_rank.mean(axis=1)


#mf_rank_percentile = mf_rank.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

fb_top10 = fb_rank.sort_values('All rating', ascending=False).head(10)

fb_top10['Playmaking'] = fb_top10['Playmaking'].apply(lambda x: x + (math.fabs(fb_top10['Playmaking'].min())*1.05))
fb_top10['Attacking'] = fb_top10['Attacking'].apply(lambda x: x + (math.fabs(fb_top10['Attacking'].min())*1.05))
fb_top10['Ball carrying'] = fb_top10['Ball carrying'].apply(lambda x: x + (math.fabs(fb_top10['Ball carrying'].min())*1.05))
fb_top10['Defending'] = fb_top10['Defending'].apply(lambda x: x + (math.fabs(fb_top10['Defending'].min())*1.05))

fb_top10 = fb_top10.sort_values('All rating')
players_name = list(fb_top10.index)

#PLOT PLOT PLOT
rank_param = ['Defending', 'Playmaking', 'Ball carrying', 'Attacking']
rank_values = fb_top10.loc[players_name, :].values.tolist()
fields = rank_param
colors = ['#1D2F6F', '#8390FA', '#6EAF46', '#FAC748']
labels = players_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(12, 10))

# plot bars
left = len(fb_top10) * [0]
for idx, name in enumerate(fields):
    plt.barh(fb_top10.index, fb_top10[name], left = left, color=colors[idx])
    left = left + fb_top10[name]

# title, legend, labels
plt.title('Top 10 Fullbacks & Wingbacks in Liga 1\n', loc='left', size=20, style='oblique')
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
    1.03, 0.12, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()