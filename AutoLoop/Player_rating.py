#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:42:30 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn import preprocessing

competition = 'Liga 1'
season = '2022-23'
remove_wb = 'no'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

list_player = df['Player'].tolist()

# fixing some parameters
n_played = df['Minutes played'] / 90
pass_index = df['Passes per 90']

# progressive passes completed per 90
progpass_total = df['Progressive passes per 90'] * n_played
progpass_compl = progpass_total * df['Accurate progressive passes, %'] /100
df['Progressive passes completed per 90'] = (progpass_compl / n_played) /pass_index

# passes to final third completed per 90
f3_total = df['Passes to final third per 90'] * n_played
f3_compl = f3_total * df['Accurate passes to final third, %'] /100
df['Passes to final third completed per 90'] = (f3_compl / n_played) /pass_index

# dribbles completed per 90
dribble_total = df['Dribbles per 90'] * n_played
dribble_compl = dribble_total * df['Successful dribbles, %'] /100
df['Dribbles completed per 90'] = dribble_compl / n_played

# passes to penalty area completed per 90
boxentry_total = df['Passes to penalty area per 90'] * n_played
boxentry_compl = boxentry_total * df['Accurate passes to penalty area, %'] /100
df['Passes to penalty area completed per 90'] = boxentry_compl / n_played

# smart passes completed per 90
smartp_total = df['Smart passes per 90'] * n_played
smartp_compl = smartp_total * df['Accurate smart passes, %'] /100
df['Smart passes completed per 90'] = (smartp_compl / n_played) /pass_index

# crosses completed per 90
cross_total = df['Crosses per 90'] * n_played
cross_compl = cross_total * df['Accurate crosses, %'] /100
df['Crosses completed per 90'] = cross_compl / n_played

# parameters
player_info = ['Player',
               'Team within selected timeframe',
               'Main position'
               ]

goalkeeping = ['Save rate, %',
               'Prevented goals per 90',
               'Duels won, %'
               ]

attacking = ['xG per 90',
             'Shots per 90',
             'Shots on target, %',
             'Touches in box per 90',
             'Offensive duels won, %'
             ]

passing = ['Passes to final third completed per 90',
           'Progressive passes completed per 90'
           ]

playmaking = ['Deep completions per 90',
              'Shot assists per 90',
              'Key passes per 90',
              'Passes to penalty area completed per 90',
              'Smart passes completed per 90',
              'xA per 90'
              ]

wingplay = ['Deep completed crosses per 90',
            'Accurate crosses, %',
            'Crosses completed per 90'
            ]

ballcarrying = ['Dribbles completed per 90',
                'Progressive runs per 90'
                ]

defending = ['PAdj Sliding tackles',
             'PAdj Interceptions',
             'Defensive duels won, %'
             ]

# filtering based on minutes

min_minutes = 900
df = df.loc[df['Minutes played'] >= min_minutes]
df = df.fillna(0)
# filtering and grouping the dataframe based on position
position_list = df['Position'].str.split(',').str[0]
df['Position fix'] = position_list

# rename the position for grouping
df.loc[df["Position fix"] == 'GK', "Main position"] = 'GK'
df.loc[df["Position fix"].isin(['RB','LB']), "Main position"] = 'FB'
df.loc[df["Position fix"].isin(['CB','LCB','RCB']), "Main position"] = 'CB'
df.loc[df["Position fix"].isin(['DMF','LDMF','RDMF']), "Main position"] = 'MF'
df.loc[df["Position fix"].isin(['CMF','LCMF','RCMF']), "Main position"] = 'MF'
df.loc[df["Position fix"].isin(['RWB','LWB']), "Main position"] = 'WB'
df.loc[df["Position fix"] == 'AMF', "Main position"] = 'MF'
df.loc[df["Position fix"].isin(['LAMF','RAMF','LW','RW','RWF','LWF']), "Main position"] = 'WG'
df.loc[df["Position fix"] == 'CF', "Main position"] = 'CF'

df_gk = df.loc[df['Main position'] == 'GK']
df_fb = df.apply(lambda x: x[df['Position fix'].isin(['RB','LB'])])
df_wb = df.apply(lambda x: x[df['Position fix'].isin(['RWB','LWB'])])
df_cb = df.loc[df['Main position'].str.contains('CB')]
df_dmf = df.apply(lambda x: x[df['Position fix'].isin(['DMF','LDMF','RDMF'])])
df_cmf = df.apply(lambda x: x[df['Position fix'].isin(['CMF','LCMF','RCMF'])])
df_amf = df.loc[df['Position fix'] == 'AMF']
df_w = df.apply(lambda x: x[df['Position fix'].isin(['LAMF','RAMF','W','LW','RW','WF','LWF','RWF'])])
df_cf = df.loc[df['Main position'] == 'CF']

# giving parameters to each positions

# gk
df_gk = pd.concat([df_gk[player_info],
                   df_gk[goalkeeping]],
                  axis=1)
df_gk = df_gk.set_index(player_info)

# fb
df_fb = pd.concat([df_fb[player_info],
                   df_fb[passing],
                   df_fb[playmaking],
                   df_fb[wingplay],
                   df_fb[ballcarrying],
                   df_fb[defending]],
                  axis=1)
df_fb = df_fb.set_index(player_info)

# wb
df_wb = pd.concat([df_wb[player_info],
                   df_wb[passing],
                   df_wb[playmaking],
                   df_wb[wingplay],
                   df_wb[ballcarrying],
                   df_wb[defending],
                   df_wb[attacking]],
                  axis=1)
df_wb = df_wb.set_index(player_info)

# cb
df_cb = pd.concat([df_cb[player_info],
                   df_cb[passing],
                   df_cb[ballcarrying],
                   df_cb[defending]],
                  axis=1)
df_cb = df_cb.set_index(player_info)

# dmf
df_dmf = pd.concat([df_dmf[player_info],
                    df_dmf[passing],
                    df_dmf[ballcarrying],
                    df_dmf[defending]],
                  axis=1)
df_dmf = df_dmf.set_index(player_info)

# cmf
df_cmf = pd.concat([df_cmf[player_info],
                    df_cmf[passing],
                    df_cmf[playmaking],
                    df_cmf[ballcarrying],
                    df_cmf[defending],
                    df_cmf[attacking]],
                   axis=1)
df_cmf = df_cmf.set_index(player_info)

# amf
df_amf = pd.concat([df_amf[player_info],
                    df_amf[passing],
                    df_amf[playmaking],
                    df_amf[ballcarrying],
                    df_amf[attacking]],
                   axis=1)
df_amf = df_amf.set_index(player_info)

# winger
df_w = pd.concat([df_w[player_info],
                  df_w[playmaking],
                  df_w[wingplay],
                  df_w[ballcarrying],
                  df_w[attacking]],
                 axis=1)
df_w = df_w.set_index(player_info)

# cf
df_cf = pd.concat([df_cf[player_info],
                   df_cf[playmaking],
                   df_cf[ballcarrying],
                   df_cf[attacking]],
                  axis=1)
#df_cf[attacking] = df_cf[attacking].apply(lambda x: x**2)
df_cf = df_cf.set_index(player_info)

# applying zscore & percentile
function = stats.hmean # idk i just tried to use harmonic mean

# gk
zscore_gk = df_gk.apply(stats.zscore)
percentile_gk = zscore_gk.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_gk['Overall score'] = function(percentile_gk.iloc[:,:],axis=1)
norm_gk = percentile_gk['Overall score'].apply(lambda i: (i-(percentile_gk['Overall score'].min()))/((percentile_gk['Overall score'].max())-(percentile_gk['Overall score'].min())))

# fb
zscore_fb = df_fb.apply(stats.zscore)
percentile_fb = zscore_fb.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_fb['Overall score'] = function(percentile_fb.iloc[:,:],axis=1)
norm_fb = percentile_fb['Overall score'].apply(lambda i: (i-(percentile_fb['Overall score'].min()))/((percentile_fb['Overall score'].max())-(percentile_fb['Overall score'].min())))

# wb
if remove_wb == 'no':
    zscore_wb = df_wb.apply(stats.zscore)
    percentile_wb = zscore_wb.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile_wb['Overall score'] = function(percentile_wb.iloc[:,:],axis=1)
    norm_wb = percentile_wb['Overall score'].apply(lambda i: (i-(percentile_wb['Overall score'].min()))/((percentile_wb['Overall score'].max())-(percentile_wb['Overall score'].min())))
else:
    None

# cb
zscore_cb = df_cb.apply(stats.zscore)
percentile_cb = zscore_cb.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_cb['Overall score'] = function(percentile_cb.iloc[:,:],axis=1)
norm_cb = percentile_cb['Overall score'].apply(lambda i: (i-(percentile_cb['Overall score'].min()))/((percentile_cb['Overall score'].max())-(percentile_cb['Overall score'].min())))

# dmf
zscore_dmf = df_dmf.apply(stats.zscore)
percentile_dmf = zscore_dmf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_dmf['Overall score'] = function(percentile_dmf.iloc[:,:],axis=1)
norm_dmf = percentile_dmf['Overall score'].apply(lambda i: (i-(percentile_dmf['Overall score'].min()))/((percentile_dmf['Overall score'].max())-(percentile_dmf['Overall score'].min())))

# cmf
zscore_cmf = df_cmf.apply(stats.zscore)
percentile_cmf = zscore_cmf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_cmf['Overall score'] = function(percentile_cmf.iloc[:,:],axis=1)
norm_cmf = percentile_cmf['Overall score'].apply(lambda i: (i-(percentile_cmf['Overall score'].min()))/((percentile_cmf['Overall score'].max())-(percentile_cmf['Overall score'].min())))

# amf
zscore_amf = df_amf.apply(stats.zscore)
percentile_amf = zscore_amf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_amf['Overall score'] = function(percentile_amf.iloc[:,:],axis=1)
norm_amf = percentile_amf['Overall score'].apply(lambda i: (i-(percentile_amf['Overall score'].min()))/((percentile_amf['Overall score'].max())-(percentile_amf['Overall score'].min())))

# winger
zscore_w = df_w.apply(stats.zscore)
percentile_w = zscore_w.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_w['Overall score'] = function(percentile_w.iloc[:,:],axis=1)
norm_w = percentile_w['Overall score'].apply(lambda i: (i-(percentile_w['Overall score'].min()))/((percentile_w['Overall score'].max())-(percentile_cb['Overall score'].min())))

# cf
zscore_cf = df_cf.apply(stats.zscore)
percentile_cf = zscore_cf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_cf['Overall score'] = stats.hmean(percentile_cf.iloc[:,:],axis=1)
norm_cf = percentile_cf['Overall score'].apply(lambda i: (i-(percentile_cf['Overall score'].min()))/((percentile_cf['Overall score'].max())-(percentile_cf['Overall score'].min())))

# overall rating
# dataframe to use: pick percentile or norm
data = 'norm'
if remove_wb == 'no':
    player_score = pd.concat([percentile_fb['Overall score'],
                              percentile_wb['Overall score'],
                              percentile_cb['Overall score'],
                              percentile_dmf['Overall score'],
                              percentile_cmf['Overall score'],
                              percentile_amf['Overall score'],
                              percentile_w['Overall score'],
                              percentile_cf['Overall score']],
                           axis=0)
else:
   player_score = pd.concat([percentile_fb['Overall score'],
                             percentile_cb['Overall score'],
                             percentile_dmf['Overall score'],
                             percentile_cmf['Overall score'],
                             percentile_amf['Overall score'],
                             percentile_w['Overall score'],
                             percentile_cf['Overall score']],
                          axis=0) 

# getting overall score for each position and invert row to column for plotting
player_score = player_score.reset_index()
overall_player = player_score.groupby(['Team within selected timeframe',
                                       'Main position']).mean(numeric_only=True)
overall_player = overall_player.reset_index()
overall_player = overall_player.pivot_table('Overall score',
                                            ['Team within selected timeframe'],
                                            'Main position')

# normalizing the data
sort_value = overall_player.mean(axis=1, skipna=True) # normalizing factor as well as sorting factor
sum_value = overall_player.sum(axis=1) # this one is the normalizing factor
overall_player = overall_player.apply(lambda x: (x/sum_value)*sort_value) # this is how i normalize it

overall_player['Sort value'] = sort_value # insert the sorting factor into dataframe
overall_player = overall_player.sort_values('Sort value')
overall_player = overall_player.fillna(0) # replace nan with 0 because they cant be plotted

# PLOT PLOT PLOT
teams_name = list(overall_player.index)
if remove_wb == 'no':
    rank_param = ['CB','FB','WB','MF','WG','CF']
else:
    rank_param = ['CB','FB','MF','WG','CF'] # use for league with no wingback detected
rank_values = overall_player.loc[teams_name, :].values.tolist()
fields = rank_param
colors_all = ['#1D2F6F','#8390FA', '#6EAF46', '#FAC748', '#D9544D', '#5C4033']
labels = teams_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(12, 10), ncols=1, sharey=True)
fig.tight_layout() # not needed actually, unless you try 2 columns plot
plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.67, right=1.44) # to adjust spacing if i use 2 columns

# plot bars
left = len(overall_player) * [1]
for idx, i in enumerate(fields):
    plt.barh(overall_player.index, overall_player[i],left = left, color=colors_all[idx])
    left = left + overall_player[i]

# remove spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

#remove those stupid numbers below
ax.get_xaxis().set_ticks([])

# title, subtitle, legend, labels
# add title
fig.text(
    0.99, 0.92, 'Non-GK Main Squad Performance Comparison', size=17,
    ha="center", color="#000000"
)

# add subtitle
SUB_1 = f'{competition} {season}'
SUB_2 = 'Data from Wyscout'
SUB_3 = 'Minimum %s minutes played' % (min_minutes)

fig.text(
    0.99, 0.9, f"{SUB_1} | {SUB_2} | {SUB_3}",
    size=12,
    ha="center", color="#000000"
)

# add credits
CREDIT_1 = "@novalaziz"

fig.text(
    1.43, 0.1, f"{CREDIT_1}", size=10,
    color="#000000",
    ha="right"
)

# legend
ax.legend(fields, bbox_to_anchor=([0.0000001, 1, 1, 0]), ncol=6, frameon=False)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()