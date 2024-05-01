#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:14:50 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
#import math
#import numpy as np

competition = 'Liga 1'
season = '2022-23'

# variables & control
position = 'CF'
minimum_minutes = 900

per_90 = 'active' # pick active or not active

x_var = 'Touches in box'
x_control = 'Shots'
x_value = f'{x_var} per 90' # can only be plotted if per_90 is not active
x_plot = x_value

y_var = 'xG per 90' # pick xG or xG per 90
y_control = 'Shots'
y_value = f'{y_var} per {y_control}'
y_plot = y_var

c_var = 'Passport country'
c_value = 'Nationality'
#s_value = 'xG'

# title & subtitle
suptitle_string  = f"Striker Threat Clustering | {competition} {season}"
if per_90 == 'active':
    title_string = f'{x_plot} vs {y_plot} | Data from Wyscout | minimum {minimum_minutes} minutes played'
else:
    title_string = f'{x_plot} vs {y_plot} | Data from Wyscout | minimum {minimum_minutes} minutes played'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

col_list = list(df.columns)

# filter position
df = df.loc[
    (df['Position'].str.contains(position))
    & (df['Minutes played']>=minimum_minutes)
    ]

# parameters adjusment
df['90s played'] = df['Minutes played'] / 90

if per_90 == 'not active':
    df[f'{x_var}'] = df[f'{x_var} per 90'] * df['90s played']   
    df[x_value] = df[f'{x_var}'] / df[f'{x_control}']
else:
    None

df[y_value] = (df[f'{y_var}']/df[f'{y_control}']).fillna(0)

df = df.reset_index()

#df.loc[df[f"{c_var}"] == 'Indonesia', f"{c_value}"] = '1'
#df.loc[df[f"{c_var}"] != 'Indonesia', f"{c_value}"] = '0'

df_lokal = df.loc[df[f'{c_var}'].str.contains('Indonesia')]
df_lokal = df_lokal.set_index('Player')

df_asing = df.loc[df[f'{c_var}'].str.contains('Indonesia') == False]
df_asing = df_asing.set_index('Player')

df_gabung = pd.concat([df_lokal, df_asing])

# data to plot
if per_90 == 'not active':
    x_lokal = df_lokal[x_plot]
    x_asing = df_asing[x_plot]
    x = df_gabung[x_plot]
else:
    x_lokal = df_lokal[f'{x_var} per 90']
    x_asing = df_asing[f'{x_var} per 90']
    x = df_gabung[f'{x_var} per 90']
y_lokal = df_lokal[y_plot]
y_asing = df_asing[y_plot]

y = df_gabung[y_plot]

# plot the scatter
fig, ax = plt.subplots(figsize = (12,12))
points_lokal = ax.scatter(x_lokal, y_lokal, c='red', s=150)
points_asing = ax.scatter(x_asing, y_asing, c='blue', s=150)

#ax.invert_xaxis()
#ax.invert_yaxis()

# title & subtitle
plt.suptitle(suptitle_string, x=0.5, y=0.932, fontsize=25)
plt.title(title_string, x=0.5, fontsize=14)

# labeling each axis
if per_90 == 'active':
    ax.set_xlabel(f'{x_var} per 90', size='14', labelpad=12)
else:
    ax.set_xlabel(x_plot, size='14', labelpad=12)
ax.set_ylabel(y_plot, size='14', labelpad=12)

# add xy mean line to cluster the plot into quadrants
x_min = x.min()
x_max = x.max()
y_min = y.min()
y_max = y.max()
xq_right = x.mean() + x.mean()/100
xq_left = x.mean() - x.mean()/100

# quadrant line
plt.plot([x.mean(),x.mean()],[y_max,y_min],'k-', linestyle = ":", lw=1)
plt.plot([x_min,x_max],[y.mean(),y.mean()],'k-', linestyle = ":", lw=1)

# labels & legends
#plt.legend([f"{y1_value}", f"{y2_value}"], loc ="lower right")

# add credits
CREDIT_1 = "@novalaziz"

fig.text(
    0.85, 0.07, f"{CREDIT_1}", size=10,
    color="#000000",
    ha="right"
)

#label for each markers
label = df_lokal.index
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]), color = 'black', ha='center', va='bottom')

plt.show()