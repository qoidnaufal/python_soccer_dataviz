# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 09:27:04 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats
#import math
import numpy as np
from mplsoccer import PyPizza

os.chdir('/Users/qoidnaufal/Documents/Wyscout/Player data/Liga 1 2022-23')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2021-22 - Liga 1 - complete.xlsx')
#col_list = list(df.columns)
#position_list = df['Position'].tolist()

# parameters adjusment
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)
df['Verticality'] = df['Forward passes per 90']/(df['Forward passes per 90'] +
                                                 df['Lateral passes per 90'] +
                                                 df['Back passes per 90'])

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

parameters = ['Verticality', 'Accurate short / medium passes, %',
              'Accurate long passes, %', 'Dribbles completed p90',
              'Progressive runs per 90', 'Touches in box per 90',
              'Smart passes per 90', 'Passes to final third p90',
              'Progressive passes p90', 'Deep completions per 90',
              'Accurate crosses, %', 'xA per 90', 'xG per 90'
              ]

# minute & position filter
minimum_minutes = 900
competition_played = 'Liga 1'
season = '2022-23'
position_1 = 'AM'
position_2 = 'CM'
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
player_name = 'J. Bustos'
player_minute = df_mf.loc[player_name, 'Minutes played']

# show parameters-based columns only
df_mf = df_mf[parameters]
df_mf.replace([np.inf, -np.inf], 0, inplace=True)

# getting z-score & percentile rank
z_score = df_mf.apply(stats.zscore)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

# Prepare the ingredients
values = percentile.loc[player_name, :].values.tolist()
values = [round(elem, 1) for elem in values]

params_2 = ['Verticality', 'Accurate short / \nmedium passes, %',
              'Accurate long \npasses, %', 'Dribbles per 90',
              'Progressive runs \nper 90', 'Touches in box \nper 90',
              'Smart passes \nper 90', 'Passes to final \nthird per 90',
              'Progressive passes \nper 90', 'Deep completions \nper 90',
              'Accurate \ncrosses %', 'xA per 90', 'xG per 90'
              ]

# color for the slices and text
slice_colors = ["#4CBB17"] * 6 + ["#1A78CF"] * 7
text_colors = ["#000000"] * 13

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
    0.515, 0.99, (player_name), size=22,
    ha="center", color="#000000"
)

# add subtitle
SUB_1 = f"Percentile Rank vs {position_1} & {position_2}"
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
    0.432, 0.925, "Playing style       Output", size=14,
    color="#000000"
)

# add rectangles
fig.patches.extend([
    plt.Rectangle(
        (0.403, 0.9225), 0.025, 0.015, fill=True, color="#4CBB17",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.544, 0.9225), 0.025, 0.015, fill=True, color="#1A78CF",
        transform=fig.transFigure, figure=fig
    ),   
])

plt.show()