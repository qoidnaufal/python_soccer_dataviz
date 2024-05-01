# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 12:52:52 2022

@author: 62878
"""

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter

from mplsoccer import Pitch, FontManager

""" Main dataframe """
os.chdir('/Users/qoidnaufal/Documents/Learn Python/Piala Presiden')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_csv(f) for f in all_filenames])

""" Filter """
Team_filter = 'PSIS'
Player_filter = 'Marukawa'
Match = 20220613

Defend_1 = ('Tackle_win', 'Tackle_lost', 'Pressure', 'Recovery', 'Intercept',
           'Foul', 'Ground_win', 'Ground_lost', 'Aerial_win', 'Aerial_lost',
           'Clearance', 'Block_pass', 'Block_shot', 'Block_cross')
Defend_2 = ('Tackle_win', 'Intercept', 'Recovery')
Defend_3 = ('Tackle_win', 'Pressure')
Defend_4 = ['Pressure']
Line_height = 30

def defensive():  
    #change between All_actions or Successfull_actions
    df_1 = df.loc[df['Event'].isin(Defend_1)]
    
    direct_1 = df_1.loc[df_1['Direction_id'] == 1]
    direct_2 = df_1.loc[df_1['Direction_id'] == 2]

    #conversion for sliced dataframe
    
    direct_2['X'] = direct_2['X'].apply(lambda x: 100-x)
    direct_2['Y'] = direct_2['Y'].apply(lambda x: 100-x)
    #direct_1['X'] = direct_1['X'].apply(lambda x: 100-x)
    #direct_1['X'] = direct_1['X'].apply(lambda x: 100-x)
        
    df_2 = pd.concat([direct_1, direct_2])
    
    df_2['X'] = df_2['X'].apply(lambda x: x*120/100)
    df_2['Y'] = df_2['Y'].apply(lambda x: x*80/100)
                
    return df_2

df_defend = defensive()
df_defend = df_defend.reset_index(drop=True)
df_defend = df_defend.loc[df_defend['Team'].isin([Team_filter])]

""" Specific player and match filter """
df_defend = df_defend.loc[df_defend['Player'].isin([Player_filter])]
#df_defend = df_defend.loc[df_defend['Match_id'].isin([Match])]

#df_defend = df_defend.loc[df_defend['X'] > (Line_height)]

""" Plotting the map """
# setup pitch
pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
              pitch_color='#22312b', line_color='#efefef')

# fontmanager for google font (robotto)
robotto_regular = FontManager()

# path effects
path_eff = [path_effects.Stroke(linewidth=1.5, foreground='black'),
            path_effects.Normal()]

# see the custom colormaps example for more ideas on setting colormaps
pearl_earring_cmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",
                                                       ['#15242e', '#4393c4'], N=10)

fig, axs = pitch.grid(endnote_height=0.03, endnote_space=0,
                      # leave some space for the colorbar
                      grid_width=0.88, left=0.025,
                      title_height=0.06, title_space=0,
                      # Turn off the endnote/title axis. I usually do this after
                      # I am happy with the chart layout and text placement
                      axis=False,
                      grid_height=0.86)
fig.set_facecolor('#22312b')

# plot heatmap
bin_statistic = pitch.bin_statistic(df_defend.X, df_defend.Y, statistic='count', bins=(25, 25))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
pcm = pitch.heatmap(bin_statistic, ax=axs['pitch'], cmap='hot', edgecolors='#22312b')

# add cbar
ax_cbar = fig.add_axes((0.915, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)
cbar.outline.set_edgecolor('#efefef')
cbar.ax.yaxis.set_tick_params(color='#efefef')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#efefef')
for label in cbar.ax.get_yticklabels():
    label.set_fontproperties(robotto_regular.prop)
    label.set_fontsize(15)

"""
#title
axs['title'].text(0.5, 0.5, ("%s defensive actions" % (Team_filter), "by %s" % (Player_filter)), color='white',
                  va='center', ha='center', path_effects=path_eff,
                  fontproperties=robotto_regular.prop, fontsize=30)
"""