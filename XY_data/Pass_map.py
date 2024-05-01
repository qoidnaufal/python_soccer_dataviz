# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:56:00 2022

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from mplsoccer import Pitch

""" Main dataframe """
os.chdir('C:/Users/62878/Documents/PSS Sleman/Event data')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_csv(f) for f in all_filenames])

def passes():  
    df_1 = df.loc[df['Event'].isin(['Pass_success'])]
    #df_x = df.loc[df['Event'].isin(['Pass_failed'])]

    df_1 = df_1[df_1.X2.apply(lambda x: x.isnumeric())]
    df_1['X2'] = df_1['X2'].astype(float)
    df_1['Y2'] = df_1['Y2'].astype(float)

    direct_1 = df_1.loc[df_1['Direction_id'] == 1]
    direct_2 = df_1.loc[df_1['Direction_id'] == 2]

    #conversion for sliced dataframe
    
    direct_2['X'] = direct_2['X'].apply(lambda x: 100-x)
    direct_1['Y'] = direct_1['Y'].apply(lambda x: 100-x)
    direct_2['X2'] = direct_2['X2'].apply(lambda x: 100-x)
    direct_1['Y2'] = direct_1['Y2'].apply(lambda x: 100-x)

    df_2 = pd.concat([direct_1, direct_2])
    
    df_2['X'] = df_2['X'].apply(lambda x: x*105/100)
    df_2['X2'] = df_2['X2'].apply(lambda x: x*105/100)
    df_2['Y'] = df_2['Y'].apply(lambda x: x*68/100)
    df_2['Y2'] = df_2['Y2'].apply(lambda x: x*68/100)
        
    return df_2

df_pass = passes()
df_pass = df_pass.reset_index(drop=True)

""" Plotting """
pitch = Pitch(pitch_type='custom',  # example plotting a custom pitch
              pitch_length=105, pitch_width=68,
              axis=False, label=False)  # showing axis labels is optional
fig, ax = pitch.draw()

pitch.arrows(df_pass['X'], df_pass['Y'],
             df_pass['X2'], df_pass['Y2'], width=1,
             headwidth=10, headlength=10, color='#ad993c', ax=ax, label='completed passes')

"""
for i in range(len(df_pass)):
    plt.plot([(df_pass["X"][i]),(df_pass["X2"][i])],
             [(df_pass["Y"][i]),(df_pass["Y2"][i])], 
             color="blue")
"""

plt.tight_layout()
plt.show()