# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:19:30 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

os.chdir('C:/Users/62878/Documents/Wyscout/Player/PSS')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.loc[(df['Match'].str.contains('nan')==False)]
df = df.reset_index()
df = df.drop(['index'], axis=1)

col_list = list(df.columns)

df.rename(columns = {'Total actions / successful':'Total actions',
                     'Unnamed: 7':'Total actions success',
                     'Shots / on target':'Shots',
                     'Unnamed: 11':'Shots on target',
                     'Passes / accurate':'Passes',
                     'Unnamed: 14':'Passes completed',
                     'Long passes / accurate':'Long passes',
                     'Unnamed: 16':'Long passes completed',
                     'Crosses / accurate':'Crosses',
                     'Unnamed: 18':'Crosses completed',
                     'Dribbles / successful':'Dribbles',
                     'Unnamed: 20':'Dribbles completed',
                     'Duels / won':'Duels',
                     'Unnamed: 22':'Duels won',
                     'Aerial duels / won':'Aerial duels',
                     'Unnamed: 24':'Aerial duels won',
                     }, inplace = True)

df = df.groupby('Player').sum()
#df.loc['Kim Kurniawan']
