# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:00:20 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from mplsoccer import PyPizza

minimum_minutes = 600
competition = 'K3'
season = '2023'
position_1 = 'CM'
position_2 = 'DM'

player_name = 'Lee Min-Woo'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2019 - Liga 1 - complete.xlsx')
#col_list = list(df.columns)
#position_list = df['Position'].tolist()

# parameters adjusment
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)
df['Verticality'] = df['Forward passes per 90']/(df['Forward passes per 90'] +
                                                 df['Lateral passes per 90'] +
                                                 df['Back passes per 90'])

df['Assists/xA ratio'] = (df['Assists'] / df['xA']).fillna(0)

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

parameters = ['xG per 90',
              'Shots per 90', 'xG/Shot', 'Touches in box per 90',
              'Accurate short / medium passes, %',
              'Accurate long passes, %', 'Passes to final third p90',
              'Progressive passes p90',
              'Shot assists per 90', 'xA per 90',
              'Dribbles completed p90', 'Progressive runs per 90',
              'PAdj Sliding tackles', 'PAdj Interceptions', 
              'Fouls per 90', 'Defensive duels won, %',
              'Aerial duels won, %']

# minute & position filter
df_1 = df.loc[
    (df['Position'].str.contains(position_1))
            & (df['Minutes played']>=minimum_minutes)
            ]
df_2 = df.loc[
    (df['Position'].str.contains(position_2)
     & (df['Minutes played']>=minimum_minutes))
    ]
df_mf = pd.concat([df_1,df_2]).drop_duplicates()

# call the player
df_mf = df_mf.set_index('Player')
idx_list = list(df_mf.index)

player_minute = df_mf.loc[player_name, 'Minutes played']
player_club = df_mf.loc[player_name, 'Team within selected timeframe']
player_age = int(df_mf.loc[player_name, 'Age'])
player_goals = df_mf.loc[player_name, 'Goals']
player_assists = df_mf.loc[player_name, 'Assists']
player_position = df_mf.loc[player_name, 'Position']

# show parameters-based columns only
df_mf = df_mf[parameters]
df_mf.replace([np.inf, -np.inf], 0, inplace=True)

# getting z-score & percentile rank
z_score = df_mf.apply(stats.zscore)
z_score['Fouls per 90'] = z_score['Fouls per 90'].apply(lambda x: -1 * x)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
#percentile = z_score.apply(lambda x: stats.norm.cdf(x) * 100)

# Prepare the ingredients
values = percentile.loc[player_name, :].values.tolist()
values = [round(elem, 1) for elem in values]

# COOK THE PIZZA!!!
# give better spacing
params_2 = ['xG per 90', 'Shots per 90',
            'xG/Shot', 'Touches in \nbox per 90',
            'Accurate short / \nmedium passes %',
            'Accurate \nlong passes %', 'Passes to final \nthird per 90',
            'Progressive \npasses per 90',
            'Shot assists \nper 90', 'xA per 90',
            'Dribbles \nper 90', 'Progressive \ncarries per 90',
            'PAdj Tackles', 'PAdj \nInterceptions',
            'Cautiousness', 'Defensive \nduels won %',
            'Aerial duels \nwon %']

# color for the slices and text
slice_colors = ["#D70232"] * 4 + ["#4CBB17"] * 6 + ["#FF9300"] * 2 + ["#1A78CF"] * 5
text_colors = ["#000000"] * 17

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
    figsize=(12, 12),                # adjust figsize according to your need
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
        color="#000000", fontsize=11,
        va="center",
    ),                   # values to be used when adding parameter
    kwargs_values=dict(
        color="#ffffff", fontsize=12,
        zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="green",
            boxstyle="round,pad=0.2", lw=1
        )
    )                    # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.99, (f'{player_name} - {player_club} ({player_age} years old)'), size=22,
    ha="center", color="#000000"
)

# add subtitle
SUB_1 = player_position
SUB_2 = competition
SUB_3 = season
SUB_4 = player_minute

fig.text(
    0.515, 0.945, f"Position: {SUB_1} | Goals: {player_goals} | Assists: {player_assists}\n{SUB_2} | {SUB_3} | {player_minute} minutes played",
    size=15,
    ha="center", color="#000000"
)

# add credits
CREDIT_1 = "Data: Wyscout"
CREDIT_2 = "@novalaziz"

fig.text(
    0.1, 0.1, f"{CREDIT_1}\n{CREDIT_2}", size=10,
    color="#000000",
    ha="left"
)

# add text
fig.text(
    0.305, 0.925, "Attacking      Playmaking      Ball-carrying      Defending", size=14,
    color="#000000"
)

# add rectangles
fig.patches.extend([
    plt.Rectangle(
        (0.277, 0.9225), 0.025, 0.015, fill=True, color="#D70232",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.386, 0.9225), 0.025, 0.015, fill=True, color="#4CBB17",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.510, 0.9225), 0.025, 0.015, fill=True, color="#FF9300",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.647, 0.9225), 0.025, 0.015, fill=True, color="#1A78CF",
        transform=fig.transFigure, figure=fig
    ),
])

plt.show()