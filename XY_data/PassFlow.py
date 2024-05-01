# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:05:10 2022

@author: 62878
"""

import pandas as pd
import os
import glob
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from mplsoccer import Pitch, FontManager
from mplsoccer.statsbomb import read_event, EVENT_SLUG

""" Main dataframe """
os.chdir('C:/Users/62878/Learn Python/Events/Piala Presiden')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_csv(f) for f in all_filenames])

""" Filter """
Team_name = 'PSIS'
Player_name = 'Marukawa'
Match = 20220613
Line_height = 60
position = [2, 5, 34, 6, 8, 10, 7, 9, 11]

Actions_1 = ['Pass_success']
Actions_2 = ['Pass_success', 'Cross_success']
Actions_3 = ['Carry']
Actions_4 = ['Pass_success', 'Cross_success', 'Carry']

#df = df.loc[df['Position_id'].isin(position)]

def passes():  
    df_1 = df.loc[df['Event'].isin(Actions_3)]
    #df_x = df.loc[df['Event'].isin(['Pass_failed'])]

    df_1 = df_1[df_1.X2.apply(lambda x: x.isnumeric())]
    df_1['X2'] = df_1['X2'].astype(float)
    df_1['Y2'] = df_1['Y2'].astype(float)

    direct_1 = df_1.loc[df_1['Direction_id'] == 1]
    direct_2 = df_1.loc[df_1['Direction_id'] == 2]

    #conversion for sliced dataframe
    
    direct_2['X'] = direct_2['X'].apply(lambda x: 100-x)
    direct_2['X2'] = direct_2['X2'].apply(lambda x: 100-x)
    direct_2['Y'] = direct_2['Y'].apply(lambda x: 100-x)
    direct_2['Y2'] = direct_2['Y2'].apply(lambda x: 100-x)
    
    df_2 = pd.concat([direct_1, direct_2])
    
    df_2['X'] = df_2['X'].apply(lambda x: x*120/100)
    df_2['X2'] = df_2['X2'].apply(lambda x: x*120/100)
    df_2['Y'] = df_2['Y'].apply(lambda x: x*80/100)
    df_2['Y2'] = df_2['Y2'].apply(lambda x: x*80/100)
        
    return df_2

df_pass = passes()
df_pass = df_pass.reset_index(drop=True)
df_pass = df_pass.loc[df_pass['Team'].isin([Team_name])]

""" Specific player, match & area """
df_pass = df_pass.loc[df_pass['Player'].isin([Player_name])]
#df_pass = df_pass.loc[df_pass['Match_id'].isin([Match])]
#df_pass = df_pass.loc[df_pass['X'] > (Line_height)]

""" Plotting """
rcParams['text.color'] = '#c7d5cc'
pitch = Pitch(pitch_type='statsbomb',  line_zorder=2,
              line_color='#c7d5cc', pitch_color='#22312b')
bins = (6, 5)

fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor('#22312b')
# plot the heatmap - darker colors = more passes originating from that square
bs_heatmap = pitch.bin_statistic(df_pass.X, df_pass.Y, statistic='count', bins=bins)
hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Greens')
# plot the pass flow map with a single color and the
# arrow length equal to the average distance in the cell
fm = pitch.flow(df_pass.X, df_pass.Y, df_pass.X2, df_pass.Y2, color='black',
                arrow_type='same', bins=bins, ax=ax)

plt.tight_layout()
plt.show()