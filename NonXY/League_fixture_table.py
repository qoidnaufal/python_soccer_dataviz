# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 14:41:54 2023

@author: 62878
"""

import pandas as pd

df = pd.read_excel('C:/Users/62878/Documents/Wyscout/League data/Complete schedule - Liga 1 2022-23.xlsx')

df['Score_home'] = df['Goals home'] - df['Goals away']
df['Score_away'] = df['Goals away'] - df['Goals home']

