#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 08:36:03 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

competition = 'Liga 1'
season = '2022-23'
player_name = 'J. Bustos'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player specific data/{player_name}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.loc[(df['Match'].str.contains('nan')==False)]
df = df.reset_index()
df = df.drop(['index'], axis=1)

col_list = list(df.columns)

df.rename(columns = {'Total actions / successful':'Total actions',
                     'Unnamed: 6':'Successful actions',
                     'Shots / on target':'Total shots',
                     'Unnamed: 10':'Shots on target',
                     'Passes / accurate':'Passes',
                     'Unnamed: 13':'Passes completed',
                     'Long passes / accurate':'Long passes',
                     'Unnamed: 15':'Long passes completed',
                     'Crosses / accurate':'Crosses',
                     'Unnamed: 17':'Crosses completed',
                     'Dribbles / successful':'Dribbles',
                     'Unnamed: 19':'Dribbles completed',
                     'Duels / won':'Duels',
                     'Unnamed: 21':'Duels won',
                     'Aerial duels / won':'Aerial duels',
                     'Unnamed: 23':'Aerial duels won',
                     'Losses / own half':'Losses',
                     'Unnamed: 26':'Losses own half',
                     'Recoveries / opp. half':'Recoveries',
                     'Unnamed: 28':'Recoveries opp. half',
                     'Defensive duels / won':'Defensive duels',
                     'Unnamed: 32':'Defensive duels won',
                     'Loose ball duels / won':'Loose ball duels',
                     'Unnamed: 34':'Loose ball duels won',
                     'Sliding tackles / successful':'Tackles',
                     'Unnamed: 36':'Tackles won',
                     'Offensive duels / won':'Offensive duels',
                     'Unnamed: 43':'Offensive duels won',
                     'Through passes / accurate':'Through passes',
                     'Unnamed: 49':'Through passes completed',
                     'Passes to final third / accurate':'Passes to final third',
                     'Unnamed: 53':'Passes to final third completed',
                     'Passes to penalty area / accurate':'Passes to penalty area',
                     'Unnamed: 55':'Passes to penalty area completed',
                     'Forward passes / accurate':'Forward passes',
                     'Unnamed: 58':'Forward passes completed',
                     'Back passes / accurate':'Back passes',
                     'Unnamed: 60':'Back passes completed',
                     'Saves / with reflexes':'Saves',
                     'Unnamed: 65':'Saves with reflexes',
                     'Passes to GK / accurate':'Passes to GK',
                     'Unnamed: 68':'Passes to GK completed'
                     }, inplace = True)