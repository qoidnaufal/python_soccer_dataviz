#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 12:58:43 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats

competition = 'Liga 1'
season = '2022-23'

# variables
# filter & control
position_1 = 'AMF'
position_2 = 'CMF'
position_3 = 'W'
position_4 = 'CF'
minimum_minutes = 900

# x
x_var = 'xA'
x_control = 'Shot assists'
x_adj = f'{x_var} per {x_control}' # can only be plotted if per_90 is not active
x_plot = f'{x_var} per 90'

# y
PDI = ['Key passes per 90',
       'Smart passes per 90',
       'Deep completions p90',
       'Shot assists per 90']

y_var = 'Deep completions' # pick xG or xG per 90
y_control = 'Pass'
y_adj = f'{y_var} per {y_control}'
y_plot = 'PAdj Passing Danger Index' #f'{y_var} per 90'

# c if needed
c_var = 'Passport country'
c_value = 'Nationality'

# title & subtitle
suptitle_string  = f"Creator Clustering | {competition} {season}"
title_string = f'Viz by @novalaziz | Data from Wyscout | minimum {minimum_minutes} minutes played'

# importing the df
os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df_padj = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

df_padj = df_padj.groupby('Team').mean(numeric_only = True)
df_padj = df_padj.loc[:, 'Possession, %']

# checking variables
col_list = list(df.columns)

# filter position
def position_filter():
    df_1 = df.loc[
        (df['Position'].str.contains(position_1))
        & (df['Minutes played']>=minimum_minutes)
        ]
    df_2 = df.loc[
        (df['Position'].str.contains(position_2))
        & (df['Minutes played']>=minimum_minutes)
        ]
    df_3 = df.loc[
        (df['Position'].str.contains(position_3))
        & (df['Minutes played']>=minimum_minutes)
        ]
    df_4 = df.loc[
        (df['Position'].str.contains(position_4))
        & (df['Minutes played']>=minimum_minutes)
        ]
    df_z = pd.concat([df_1, df_2, df_3, df_4])
    return df_z
df = position_filter()

# variables adjustment
df['Deep completions p90'] = df['Deep completions per 90'] + df['Deep completed crosses per 90']
df['Passing Danger Index'] = stats.hmean(df[PDI], axis=1)

df['Team possession'] = [df_padj.loc[i] for i in zip(df['Team within selected timeframe'])]
df['PAdj Passing Danger Index'] = df['Passing Danger Index'] *(50/df['Team possession'])

df['90s played'] = df['Minutes played'] / 90

df[x_control] = df[f'{x_control} per 90'] * df['90s played']
df[x_adj] = df[x_var] / df[x_control]

df[y_var] = df[f'{y_var} per 90'] * df['90s played']
df[y_control] = df[f'{y_control}es per 90'] * df['90s played']
df[y_adj] = df[y_var] / df[y_control]

df = df.set_index('Player')

# splitting lokal vs asing
df_lokal = df.loc[df[f'{c_var}'].str.contains('Indonesia')]
df_asing = df.loc[df[f'{c_var}'].str.contains('Indonesia') == False]
df_gabung = pd.concat([df_lokal, df_asing])

# data to plot
# x
x_lokal = df_lokal[x_plot]
x_asing = df_asing[x_plot]
x = df_gabung[x_plot]

# y
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

# axis label
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
plt.plot([x.mean(),x.mean()],[y_max,y_min], linestyle = ":", lw=1, color = 'black')
plt.plot([x_min,x_max],[y.mean(),y.mean()], linestyle = ":", lw=1, color = 'black')

# add credits
#CREDIT_1 = "@novalaziz"

#fig.text(
#    0.92, 0.07, f"{CREDIT_1}", size=10,
#    color="#000000",
#    ha="right"
#)

#label for each markers
label = df_gabung.index
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]), color = 'black', ha='center', va='bottom')

plt.show()