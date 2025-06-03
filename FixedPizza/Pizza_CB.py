# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 23:36:20 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from mplsoccer import PyPizza

minimum_minutes = 900
competition = 'Liga 1'
season = '2024-25'
position_centerbacks = 'CB'

player_name = 'João Vitor'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))] # explain for loop & range + len
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#df = pd.read_excel('C:/Users/62878/Documents/Wyscout/League data/Liga 1 - 20230303.xlsx')
col_list = list(df.columns) #explain about listing stuff you want to check
# print(col_list)
position_list = df['Position'].tolist()

nineties = df['Minutes played'] / 90
df['Total Interceptions'] = df['Interceptions per 90'] * nineties
df['Possession'] = df ['Total Interceptions'] * 30 / df['PAdj Interceptions']

df['Successful def actions'] = df['Successful defensive actions per 90'] * nineties
df['PAdj Successful def actions'] = df['Successful def actions'] * 30 / df['Possession']

playmaking =[
    'Accurate short / medium passes, %',
    'Accurate long passes, %', 'Passes to final third per 90',
    'Accurate passes to final third, %',
    'Progressive passes per 90', 'Accurate progressive passes, %'
]
ballcarrying = [
    'Dribbles per 90', 'Successful dribbles, %', 'Progressive runs per 90'
]
defending = [
    'PAdj Sliding tackles',  'PAdj Interceptions', 'PAdj Successful def actions',
    'Defensive duels won, %', 'Aerial duels won, %', 'Fouls per 90'
]

parameters = []
parameters.extend(playmaking)
parameters.extend(ballcarrying)
parameters.extend(defending)

# minute & position filter
df_cb = df.loc[
    (df['Position'].str.contains(position_centerbacks) # explain the use of .str.contains
     & (df['Minutes played']>=minimum_minutes)) # do this first explain eq operation
]

# call the player
df_cb = df_cb.set_index('Player')
idx_list = list(df_cb.index)
print(idx_list)

player_minute = df_cb.loc[player_name, 'Minutes played']
player_club = df_cb.loc[player_name, 'Team within selected timeframe']
player_age = int(df_cb.loc[player_name, 'Age'])
player_position = df_cb.loc[player_name, 'Position']
player_goals = df_cb.loc[player_name, 'Goals']
player_assists = df_cb.loc[player_name, 'Assists']

# show parameters-based columns only
df_cb = df_cb[parameters]
df_cb.replace([np.inf, -np.inf], 0, inplace=True)

# getting z-score & percentile rank
z_score = df_cb.apply(stats.zscore)
z_score['Fouls per 90'] = z_score['Fouls per 90'].apply(lambda x: -1 * x)
percentile = z_score.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
#percentile = z_score.apply(lambda x: (100 - (stats.norm.sf(x) * 100)) * league_ratio)
#percentile = z_score.apply(lambda x: stats.norm.cdf(x) * 100)

# Prepare the ingredients
values = percentile.loc[player_name, :].values.tolist()
values = [round(elem, 1) for elem in values]

# COOK THE PIZZA!!!
# give better spacing
params_2 = [
    'Accurate short / \nmedium passes %', #explain later why this is important
    'Accurate \nlong passes %',
    'Passes to final \nthird per 90',
    'Accurate passes \nto final third %',
    'Progressive \npasses per 90',
    'Accurate progressive \npasses %',
    'Dribbles \nper 90',
    'Successful \ndribbles %',
    'Progressive \ncarries per 90',
    'PAdj Tackles', 
    'PAdj \nInterceptions',
    'PAdj Successful \ndefensive actions',
    'Defensive \nduels won %',
    'Aerial duels \nwon %',
    'Fouls per 90'
    ]

# color for the slices and text
a = len(playmaking)
b = len(ballcarrying)
c = len(defending)
slice_colors = ["#4CBB17"] * a + ["#FF9300"] * b + ["#1A78CF"] * c
text_colors = ["#000000"] * len(parameters)

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
SUB_2 = competition
SUB_3 = season
SUB_4 = player_minute

fig.text(
    0.515, 0.925, f"Position: {SUB_1} | Goals: {player_goals} | Assists: {player_assists}\n{SUB_2} | {SUB_3} | {player_minute} minutes played",
    size=12,
    ha="center", color="#000000"
)


# add credits
TEXT_1 = "Template for CB"
CREDIT_1 = "Data: Wyscout"
CREDIT_2 = "Qoid Naufal"

fig.text(
    0.95, 0.05, f"{TEXT_1}\n{CREDIT_1}\n{CREDIT_2}", size=10,
    color="#000000",
    ha="right"
)

plt.show()
