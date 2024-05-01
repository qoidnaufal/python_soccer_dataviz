# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:19:35 2023

@author: 62878
"""

import pandas as pd
import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager

df = pd.read_excel('C:/Users/62878/Documents/Wyscout/Liga 1/2022-23 - Liga 1 - complete.xlsx')
col_list = list(df.columns)
position_list = df['Position'].tolist()

params = ['Availability','Duels won %', 'Aerial won %',
          'tackle', 'Interception',
          'Fouls per 90', 'Dribble per 90', 'Successful dribble %',
          'Longpass', 'Accurate longpass %',
          'Pass to final third', 'Accurate pass to final third',
          'Progressive pass', 'Accurate progressive pass%']

minutes_played = 300
position_filter = 'CB'
#pss_filter = df.loc[(df['Team']=='PSS Sleman')]
df_cb = df.loc[(df['Position'].str.contains(position_filter)) &
               (df['Minutes played']>=minutes_played)]
df_cb = df_cb.set_index('Player')
df_cb = df_cb.drop(['Y. Sayuri','A. Figo','A. Tanjung','Arthur','M. Helmiawan','I. Sanjaya'])

#df_cb['verticality'] = (df_cb['Forward passes per 90'] / ((df_cb['Back passes per 90']) +
                                                          #df_cb['Lateral passes per 90'] +
                                                          #df_cb['Forward passes per 90']))

# params ranked
df_cb['availability'] = df_cb['Minutes played'].rank(pct=True) * 100
df_cb['pct Defensive duels won, %'] = df_cb['Defensive duels won, %'].rank(pct=True) * 100
df_cb['pct Aerial duels won, %'] = df_cb['Aerial duels won, %'].rank(pct=True) * 100
df_cb['pct PAdj Sliding tackles'] = df_cb['PAdj Sliding tackles'].rank(pct=True) * 100
df_cb['pct PAdj Interceptions'] = df_cb['PAdj Interceptions'].rank(pct=True) * 100
df_cb['pct Fouls per 90'] = df_cb['Aerial duels won, %'].rank(ascending=False,pct=True) * 100

df_cb['pct Dribbles per 90'] = df_cb['Dribbles per 90'].rank(pct=True) * 100
df_cb['pct Successful dribbles, %'] = df_cb['Successful dribbles, %'].rank(pct=True) * 100
#df_cb['pct verticality'] = df_cb['verticality'].rank(pct=True) * 100
df_cb['pct Long passes per 90'] = df_cb['Long passes per 90'].rank(pct=True) * 100

df_cb['pct Accurate long passes, %'] = df_cb['Accurate long passes, %'].rank(pct=True) * 100
df_cb['pct Passes to final third per 90'] = df_cb['Passes to final third per 90'].rank(pct=True) * 100
df_cb['pct Accurate passes to final third, %'] = df_cb['Accurate passes to final third, %'].rank(pct=True) * 100
df_cb['pct Progressive passes per 90'] = df_cb['Progressive passes per 90'].rank(pct=True) * 100
df_cb['pct Accurate progressive passes, %'] = df_cb['Accurate progressive passes, %'].rank(pct=True) * 100

# value based on params
df_cb['value'] = df_cb[['availability','pct Defensive duels won, %',
                        'pct Aerial duels won, %','pct PAdj Sliding tackles',
                        'pct PAdj Interceptions','pct Fouls per 90',
                        'pct Dribbles per 90','pct Successful dribbles, %',
                        'pct Long passes per 90','pct Accurate long passes, %',
                        'pct Passes to final third per 90','pct Accurate passes to final third, %',
                        'pct Progressive passes per 90','pct Accurate progressive passes, %']].mean(axis=1)

df_cb['CB rank'] = df_cb['value'].rank(pct=True) * 100
df_cb = df_cb.sort_values(by=['CB rank'], ascending=False)

values = [56,54,60,45,87,40,72,24,96,70,87,69,98,75]

font_normal = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto%5Bwdth,wght%5D.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto-Italic%5Bwdth,wght%5D.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab%5Bwght%5D.ttf')

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-."            # linestyle for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values,              # list of values
    figsize=(8, 8),      # adjust figsize according to your need
    param_location=110,  # where the parameters will be added
    kwargs_slices=dict(
        facecolor="green", edgecolor="#000000",
        zorder=2, linewidth=1
    ),                   # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=11,
        fontproperties=font_normal.prop, va="center"
    ),                   # values to be used when adding parameter
    kwargs_values=dict(
        color="#ffffff", fontsize=12,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="green",
            boxstyle="round,pad=0.2", lw=1
        )
    )                    # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.97, "Tallyson Duarte - PSS Sleman", size=18,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add subtitle
fig.text(
    0.515, 0.942,
    "Percentile Rank vs Liga 1 Centerbacks | 2022-23",
    size=15,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

plt.show()