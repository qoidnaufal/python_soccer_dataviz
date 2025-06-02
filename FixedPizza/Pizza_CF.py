# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:11:26 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats
from mplsoccer import PyPizza

minutes_played = 900
season = '2024-25'
competition_played = 'Liga 1'
position_filter_1 = 'CF'
# max_age = 30
# minimum_height = 183

player_name = 'Léo Gaúcho'

# load in the data
os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition_played} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#df = pd.read_excel('C:/Users/62878/Documents/Wyscout/League data/Uruguay Primera Division - 2022.xlsx')

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
df['Successful dribbles'] = df['Total dribbles'] * df['Successful dribbles, %']
df['Dribbles completed p90'] = df['Successful dribbles'] / df['90s played']

df['Longpass received ratio'] = df['Received long passes per 90'] / (df['Received passes per 90'] +
                                                                     df['Received long passes per 90'])

# minute & position filter

df = df.loc[(df['Position'].str.contains(position_filter_1)) &
              (df['Minutes played']>=minutes_played)
#              & (df["Height"]>=minimum_height)
              ]

goalscoring = [
    'xG per 90', 'xG/Shot', 'Shots per 90',
    'Shots on target, %', 'Touches in box per 90'
]

playmaking = [
    'Smart passes per 90', 'Deep completions per 90',
    'Shot assists per 90', 'xA per 90'
]

ballcarrying = [
    'Dribbles per 90', 'Successful dribbles, %',
    'Progressive runs per 90', 'Fouls suffered per 90'
]

duels = ['Offensive duels won, %', 'Aerial duels won, %']

params = []
params.extend(goalscoring)
params.extend(playmaking)
params.extend(ballcarrying)
params.extend(duels)

# call the player
df = df.set_index('Player')
idx_list = list(df.index)
print(idx_list)

player_minute = df.loc[player_name, 'Minutes played']
player_club = df.loc[player_name, 'Team within selected timeframe']
player_age = int(df.loc[player_name, 'Age'])
player_goals = df.loc[player_name, 'Goals']
player_assists = df.loc[player_name, 'Assists']
player_position = df.loc[player_name, 'Position']
player_height = df.loc[player_name, 'Height']

# show parameters-based columns only
df_cf = df[params].fillna(0)

# getting z-score & percentile rank
z_score = df_cf.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

# RANKING
mean_value = z_score[params].mean(axis=1)
cf_rank = mean_value.rank(ascending=False)

# Prepare the ingredients
values = percentile.loc[player_name, :].values.tolist()
values = [round(elem, 1) for elem in values]

# COOK THE PIZZA!!!
# give better spacing
params_2 = [
    'xG per 90', 'xG/Shot', 'Shots per 90', 'Shots on \ntarget %',
    'Touches in box \nper 90', 'Smart passes per 90',
    'Deep completions \nper 90', 'Shot assists \nper 90',
    'xA per 90', 'Dribbles \nper 90', 'Successful \ndribbles %',
    'Progressive \nruns per 90', 'Fouls suffered \nper 90',
    'Offensive duels \nwon %', 'Aerial duels \nwon %'
]

len_a = len(goalscoring)
len_b = len(playmaking)
len_c = len(ballcarrying)
len_d = len(duels)

# color for the slices and text
slice_colors = ["#D70232"] * len_a + ["#4CBB17"] * len_b + ["#FF9300"] * len_c + ["#1A78CF"] * len_d
text_colors = ["#000000"] * len(params)

# instantiate PyPizza class
baker = PyPizza(
    params=params_2,                 # list of parameters
    background_color="#EBEBE9",      # background color
    straight_line_color="#000000",   # color for straight lines
    straight_line_lw=1,              # linewidth for straight lines
    last_circle_lw=1,                # linewidth of last circle
    other_circle_lw=1,               # linewidth for other circles
    other_circle_ls="-."             # linestyle for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values,                          # list of values
    figsize=(9, 9),                  # adjust figsize according to your need
    color_blank_space="same",        # use same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    param_location=106,              # where the parameters will be added
    kwargs_slices=dict(
        facecolor="green", edgecolor="#000000",
        zorder=2, linewidth=1
    ),                   # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=10,
        va="center",
    ),                   # values to be used when adding parameter
    kwargs_values=dict(
        color="#ffffff", fontsize=10,
        zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="green",
            boxstyle="round,pad=0.2", lw=1
        )
    )                    # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.97, (f'{player_name} - {player_club} ({player_age} years old)'), size=18,
    ha="center", color="#000000"
)

# add subtitle
SUB_1 = player_position
SUB_2 = competition_played
SUB_3 = season
SUB_4 = player_minute

fig.text(
    0.515, 0.925, f"Position: {SUB_1} | Goals: {player_goals} | Assists: {player_assists}\n{SUB_2} | {SUB_3} | {player_minute} minutes played",
    size=12,
    ha="center", color="#000000"
)


# add credits
TEXT_1 = "Template for CF"
CREDIT_1 = "Data: Wyscout"
CREDIT_2 = "Qoid Naufal"

fig.text(
    0.95, 0.05, f"{TEXT_1}\n{CREDIT_1}\n{CREDIT_2}", size=10,
    color="#000000",
    ha="right"
)

plt.show()
