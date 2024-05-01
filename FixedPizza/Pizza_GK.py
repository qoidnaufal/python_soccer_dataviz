# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 13:36:00 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from mplsoccer import PyPizza

competition_played = 'Liga 1'
minutes_played = 900
season = '2022-23'
player_name = 'N. Norhalid'

# load in the data
os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition_played} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2021-22 - Liga 1 - complete.xlsx')

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


position_filter_1 = 'G'
df = df.loc[(df['Position'].str.contains(position_filter_1)) &
              (df['Minutes played']>=minutes_played)]

params = ['Save rate, %', 'Prevented goals per 90',
          'Exits per 90', 'Duels won, %',
          'Clean sheets',
          'Short / medium passes per 90', 'Long passes per 90',
          'Accurate short / medium passes, %', 'Accurate long passes, %']

# call the player
df = df.set_index('Player')
idx_list = list(df.index)

player_minute = df.loc[player_name, 'Minutes played']
player_club = df.loc[player_name, 'Team within selected timeframe']

# show parameters-based columns only
df_gk = df[params]

# getting z-score & percentile rank
z_score = df_gk.apply(stats.zscore)
#z_score['Conceded goals per 90'] = z_score['Conceded goals per 90'].apply(lambda x: -1 * x)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

# Prepare the ingredients
values = percentile.loc[player_name, :].values.tolist()
values = [round(elem, 1) for elem in values]

# COOK THE PIZZA!!!
# give better spacing
params_2 = ['Save rate %', 'Prevented \ngoals per 90',
          'Exits per 90', 'Duels won %',
          'Clean sheets',
          'Short / medium \npasses per 90', 'Long passes \nper 90',
          'Accurate short / \nmedium passes %', 'Accurate long \npasses %']

# color for the slices and text
slice_colors = ["#1A78CF"] * 5 + ["#4CBB17"] * 4
text_colors = ["#000000"] * 9

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
    0.515, 0.99, (f'{player_name} - {player_club}'), size=22,
    ha="center", color="#000000"
)

# add subtitle
SUB_1 = "Percentile Rank vs Goalkeepers"
SUB_2 = competition_played
SUB_3 = season
SUB_4 = player_minute

fig.text(
    0.515, 0.945, f"{SUB_1}\n{SUB_2} | {SUB_3} | %s minutes played" % (player_minute),
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
    0.430, 0.925, "Goalkeeping        Passing", size=14,
    color="#000000"
)

# add rectangles
fig.patches.extend([
    plt.Rectangle(
        (0.402, 0.9225), 0.025, 0.015, fill=True, color="#1A78CF",
        transform=fig.transFigure, figure=fig
    ),    
    plt.Rectangle(
        (0.545, 0.9225), 0.025, 0.015, fill=True, color="#4CBB17",
        transform=fig.transFigure, figure=fig
    ),    
])

plt.show()