#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 15:28:46 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

# set main data to analyze
competition = "Liga 1"
season = "2022-23"
minimum_minutes = 900

# set the parameters
x_value = "Defensive duels per 90"
y_value = "Fouls per 90"

player_name = "T. Febriyanto"

# lets open the data from file
os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.fillna(0)

# filter the minutes
df = df.loc[df["Minutes played"] >= minimum_minutes]

event_list = list(df.columns)

# do this to create some datasets
df = df.set_index('Player')
df_taufiq = df.loc[df.index == player_name]
df_other = df.loc[df.index != player_name]

x = df[x_value]
y = df[y_value]

x1 = df_other[x_value]
y1 = df_other[y_value]

x2 = df_taufiq[x_value]
y2 = df_taufiq[y_value]

# plot the data
fig, ax = plt.subplots(figsize = (11,7))
points1 = ax.scatter(x1, y1, c="green")
points2 = ax.scatter(x2, y2, c="red", s=85)

# add some information along the axis
title_string = f"{player_name} Tendency to Make Foul"
ax.set_xlabel(x_value, size='11', labelpad=12)
ax.set_ylabel(y_value, size='11', labelpad=12)
ax.set_title(title_string, size="22")

#label for each markers
label = df_taufiq.index
for i, txt in enumerate(label):
    ax.annotate(txt, (x2[i], y2[i]), color = 'black', ha='center', va='bottom', size=15)
#plt.show()

#calculate equation for trendline
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

#add trendline to plot
plt.plot(x, p(x), color="black", linestyle="--", linewidth=1)
plt.show()