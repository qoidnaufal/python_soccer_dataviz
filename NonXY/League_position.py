# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 09:50:51 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

df = pd.read_excel('C:/Users/62878/Documents/PSS Sleman/Final report/Leage form.xlsx')

x_value = 'Week'
y_value = 'Position'

x = np.array(df[x_value])
y = np.array(df[y_value])

# set the canvas
fig, ax = plt.subplots(figsize = (20,8), facecolor='black')
ax.set_facecolor('black')
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# plot the data
plt.plot(x, y, color = 'green', linewidth=4, marker='D')
#plt.xticks(rotation = 'vertical')
#ax.invert_xaxis()
#ax.invert_yaxis()

plt.xlim(0.5, 34)
plt.ylim(18, 1)

label = df.Opponent
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]),
                color = 'white',
                ha='center',
                va='bottom',
                rotation=60)

title_string = 'PSS Sleman League Rank Performance'
#subtitle_string = 'rolling average every %s games | data from wyscout | @novalaziz' % (rolling_average)
subtitle_string = 'Liga 1 | 2022-23 | data from transfermarkt'

plt.suptitle(title_string, y=0.945, color='white', fontsize=22)
plt.title(subtitle_string, x=0.484, color='white', fontsize=12)

plt.show()