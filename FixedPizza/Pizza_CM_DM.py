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

minimum_minutes = 750
competition = 'Liga 1'
season = '2024-25'
position_1 = 'CM'
position_2 = 'DM'

player_name = 'R. Enero'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2019 - Liga 1 - complete.xlsx')
# col_list = list(df.columns)
# print(list(df.columns))
#position_list = df['Position'].tolist()

# parameters adjusment
df['Goals/xG ratio'] = (df['Goals'] / df['xG']).fillna(0)
df['xG/Shot'] = (df['xG']/df['Shots']).fillna(0)
df['Verticality'] = df['Forward passes per 90']/(df['Forward passes per 90'] +
                                                 df['Lateral passes per 90'] +
                                                 df['Back passes per 90'])

df['Assists/xA ratio'] = (df['Assists'] / df['xA']).fillna(0)


nineties = df['Minutes played'] / 90
df['Total Interceptions'] = df['Interceptions per 90'] * nineties
df['Possession'] = df ['Total Interceptions'] * 30 / df['PAdj Interceptions']

df['Successful def actions'] = df['Successful defensive actions per 90'] * nineties
df['PAdj Successful def actions'] = df['Successful def actions'] * 30 / df['Possession']

# df['Total progressive passes'] = df['Progressive passes per 90'] * nineties
# df['Completed progressive passes'] = df['Total progressive passes'] * df['Accurate progressive passes, %'] / 100
# df['Progressive passes p90'] = df['Completed progressive passes'] / nineties

# df['Total passes to f3'] = df['Passes to final third per 90'] * nineties
# df['Completed passes to f3'] = df['Total passes to f3'] * df['Accurate passes to final third, %'] / 100
# df['Passes to final third p90'] = df['Completed passes to f3'] / nineties

# df['Total dribbles'] = df['Dribbles per 90'] * nineties
# df['Successful dribbles'] = df['Total dribbles'] * df['Successful dribbles, %']
# df['Dribbles completed p90'] = df['Successful dribbles'] / nineties

attacking = ['Shots per 90', 'xG/Shot', 'Touches in box per 90']

playmaking = [
    'Passes per 90', 'Accurate short / medium passes, %',
    'Accurate long passes, %', 'Passes to final third per 90',
    'Progressive passes per 90',
    'Shot assists per 90', 'xA per 90'
]

ballhandling = ['Offensive duels won, %', 'Dribbles per 90', 'Progressive runs per 90']

defensive = [
    'PAdj Sliding tackles', 'PAdj Interceptions', 
    'PAdj Successful def actions',
    'Fouls per 90', 'Defensive duels won, %',
    'Aerial duels won, %'
]

parameters = []
parameters.extend(attacking)
parameters.extend(playmaking)
parameters.extend(ballhandling)
parameters.extend(defensive)

# minute & position filter
df_1 = df.loc[
    (df['Position'].str.contains(position_1))
    & (df['Minutes played']>=minimum_minutes)
    & (df['Position'].str.contains('AMF') == False)
]
df_2 = df.loc[
    (df['Position'].str.contains(position_2)
    & (df['Minutes played']>=minimum_minutes))
    & (df['Position'].str.contains('AMF') == False)
]
df_mf = pd.concat([df_1,df_2]).drop_duplicates()

# call the player
df_mf = df_mf.set_index('Player')
idx_list = list(df_mf.index)
print(idx_list)

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
params_2 = [
    'Shots per 90', 'xG/Shot', 'Touches in \nbox per 90',
    'Passes per 90', 'Accurate short / \nmedium passes %',
    'Accurate \nlong passes %', 'Passes to final \nthird per 90',
    'Progressive \npasses per 90',
    'Shot assists \nper 90', 'xA per 90','Offensive duels \nwon, %',
    'Dribbles \nper 90', 'Progressive \ncarries per 90',
    'PAdj Tackles', 'PAdj \nInterceptions', 'PAdj Successful\ndef actions',
    'Cautiousness', 'Defensive \nduels won %',
    'Aerial duels \nwon %'
]

# color for the slices and text
a = len(attacking)
p = len(playmaking)
b = len(ballhandling)
d = len(defensive)
slice_colors = ["#D70232"] * a + ["#4CBB17"] * p + ["#FF9300"] * b + ["#1A78CF"] * d
text_colors = ["#000000"] * len(parameters)

baker = PyPizza(
    params=params_2,                 # list of parameters
    background_color="#EBEBE9",      # background color
    straight_line_color="#000000",   # color for straight lines
    straight_line_lw=1,              # linewidth for straight lines
    last_circle_lw=1,                # linewidth of last circle
    other_circle_lw=1,               # linewidth for other circles
    other_circle_ls="-."             # linestyle for other circles
)

# instantiate PyPizza class
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
TEXT_1 = "Template for CM & DM"
CREDIT_1 = "Data: Wyscout"
CREDIT_2 = "Qoid Naufal"

fig.text(
    0.95, 0.05, f"{TEXT_1}\n{CREDIT_1}\n{CREDIT_2}", size=10,
    color="#000000",
    ha="right"
)

# attacking = "Attacking"
# playmaking = "Playmaking"
# ball_carrying = "Ball-carrying"
# defending = "Defending"

# attacking_start = 0.140
# playmaking_start = (attacking_start + 0.2)
# ball_carrying_start = (playmaking_start + 0.2)
# defending_start = (ball_carrying_start + 0.2)

# # add text
# fig.text(
#     attacking_start, 0.925, attacking, size=14,
#     color="#000000"
# )
# fig.text(
#     playmaking_start, 0.925, playmaking, size=14,
#     color="#000000"
# )
# fig.text(
#     ball_carrying_start, 0.925, ball_carrying, size=14,
#     color="#000000"
# )
# fig.text(
#     defending_start, 0.925, defending, size=14,
#     color="#000000"
# )

# # add rectangles
# fig.patches.extend([
#     plt.Rectangle(
#         (attacking_start + (len(attacking)/100) + 0.02, 0.9225), 0.025, 0.015, fill=True, color="#D70232",
#         transform=fig.transFigure, figure=fig
#     ),
#     plt.Rectangle(
#         (playmaking_start + (len(playmaking)/100 + 0.03), 0.9225), 0.025, 0.015, fill=True, color="#4CBB17",
#         transform=fig.transFigure, figure=fig
#     ),
#     plt.Rectangle(
#         (ball_carrying_start + (len(ball_carrying)/100 + 0.02), 0.9225), 0.025, 0.015, fill=True, color="#FF9300",
#         transform=fig.transFigure, figure=fig
#     ),
#     plt.Rectangle(
#         (defending_start + (len(defending)/100) + 0.03, 0.9225), 0.025, 0.015, fill=True, color="#1A78CF",
#         transform=fig.transFigure, figure=fig
#     ),
# ])

plt.show()
