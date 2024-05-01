#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 04:21:46 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

os.chdir('/Users/qoidnaufal/Documents/Wyscout/Player data/Liga 1 2022-23')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.fillna(0)

# filtering based on minutes
min_minutes = 0
df = df.loc[df['Minutes played'] >= min_minutes]

list_player = df['Player'].tolist()

# checking contribution
player_name = 'G. Nugraha'
target_team = 'Persik Kediri'

# fixing some potential errors in the data
df.loc[79, 'Player'] = 'Ady Setiawan'
df.loc[164, 'Player'] = 'Arif Setiawan'
df.loc[61, 'Player'] = 'Yakob Sayuri'
df.loc[242, 'Player'] = 'Yance Sayuri'
df.loc[292, 'Position'] = 'CB'

# parameters
player_info = ['Player',
               'Team within selected timeframe',
               'Main position']

goalkeeping = ['Save rate, %',
               'Prevented goals per 90',
               'Duels won, %']

attacking = ['xG per 90',
             'Shots per 90',
             'Shots on target, %',
             'Touches in box per 90',
             'Offensive duels won, %']

passing = ['Passes to final third per 90',
           'Accurate passes to final third, %',
           'Progressive passes per 90',
           'Accurate progressive passes, %'
           ]

playmaking = ['Deep completions per 90',
              'Shot assists per 90',
              'Key passes per 90',
              'Passes to penalty area per 90',
              'Accurate passes to penalty area, %',
              'Smart passes per 90',
              'Accurate smart passes, %',
              'xA per 90']

wingplay = ['Deep completed crosses per 90',
            'Accurate crosses, %']

ballcarrying = ['Dribbles per 90',
                'Successful dribbles, %',
                'Progressive runs per 90']

defending = ['PAdj Sliding tackles',
             'PAdj Interceptions',
             'Defensive duels won, %']



# filtering and grouping the dataframe based on position
position_list = df['Position'].str.split(',').str[0]
df['Position fix'] = position_list

# rename the position for grouping
df.loc[df["Position fix"] == 'GK', "Main position"] = 'GK'
df.loc[df["Position fix"].isin(['RB','LB']), "Main position"] = 'FB'
df.loc[df["Position fix"].str.contains('CB'), "Main position"] = 'CB'
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
                   df_cf[attacking]],
                  axis=1)
df_cf = df_cf.set_index(player_info)

# applying zscore & percentile
function = stats.hmean # idk i just tried to use harmonic mean

# gk
zscore_gk = df_gk.apply(stats.zscore)
percentile_gk = zscore_gk.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_gk['Overall score'] = function(percentile_gk.iloc[:,:],axis=1)

# fb
zscore_fb = df_fb.apply(stats.zscore)
percentile_fb = zscore_fb.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_fb['Overall score'] = function(percentile_fb.iloc[:,:],axis=1)

# wb
zscore_wb = df_wb.apply(stats.zscore)
percentile_wb = zscore_wb.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_wb['Overall score'] = function(percentile_wb.iloc[:,:],axis=1)

# cb
zscore_cb = df_cb.apply(stats.zscore)
percentile_cb = zscore_cb.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_cb['Overall score'] = function(percentile_cb.iloc[:,:],axis=1)

# dmf
zscore_dmf = df_dmf.apply(stats.zscore)
percentile_dmf = zscore_dmf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_dmf['Overall score'] = function(percentile_dmf.iloc[:,:],axis=1)

# cmf
zscore_cmf = df_cmf.apply(stats.zscore)
percentile_cmf = zscore_cmf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_cmf['Overall score'] = function(percentile_cmf.iloc[:,:],axis=1)

# amf
zscore_amf = df_amf.apply(stats.zscore)
percentile_amf = zscore_amf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_amf['Overall score'] = function(percentile_amf.iloc[:,:],axis=1)

# winger
zscore_w = df_w.apply(stats.zscore)
percentile_w = zscore_w.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_w['Overall score'] = function(percentile_w.iloc[:,:],axis=1)

# cf
zscore_cf = df_cf.apply(stats.zscore)
percentile_cf = zscore_cf.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
percentile_cf['Overall score'] = stats.hmean(percentile_cf.iloc[:,:],axis=1)

# overall rating
player_score = pd.concat([percentile_fb['Overall score'],
                          percentile_wb['Overall score'],
                            percentile_cb['Overall score'],
                            percentile_dmf['Overall score'],
                            percentile_cmf['Overall score'],
                            percentile_amf['Overall score'],
                            percentile_w['Overall score'],
                            percentile_cf['Overall score']],
                       axis=0)

player_score = player_score.reset_index()
overall_player = player_score.groupby(['Team within selected timeframe',
                                       'Main position']).mean(numeric_only=True)
overall_player = overall_player.reset_index()
overall_player = overall_player.pivot_table('Overall score',
                                            ['Team within selected timeframe'],
                                            'Main position')

overall_score = overall_player.fillna(0)
overall_score['Team overall score'] = overall_player.sum(axis=1)
overall_score = overall_score.reset_index()

# player contribution check
base_contribution = player_score.groupby(['Team within selected timeframe',
                                          'Main position']).sum(numeric_only=True)

base_contribution.rename(columns={'Overall score':'Position score'}, inplace=True)

base_contribution = base_contribution.reset_index()

player_team = player_score.loc[player_score['Player'] == player_name,
                               'Team within selected timeframe'].values[0]

player_position = player_score.loc[player_score['Player'] == player_name,
                                   'Main position'].values[0]

get_score = player_score.loc[player_score['Player'] == player_name,
                             'Overall score'].values[0]

position_score = base_contribution.loc[(base_contribution['Team within selected timeframe'] == player_team)
                                   & (base_contribution['Main position'] == player_position),
                                   'Position score'].values[0]
target_position_score = base_contribution.loc[(base_contribution['Team within selected timeframe'] == target_team)
                                   & (base_contribution['Main position'] == player_position),
                                   'Position score'].values[0]

team_score = overall_score.loc[overall_score['Team within selected timeframe'] == player_team,
                               'Team overall score'].values[0]
target_team_score = overall_score.loc[overall_score['Team within selected timeframe'] == target_team,
                               'Team overall score'].values[0]

position_contribution = (get_score / position_score) *100
team_contribution = (get_score / team_score) *100

target_position_contribution = (get_score / target_position_score) *100
target_team_contribution = (get_score / target_team_score) *100

print(f'{player_name} contribution in {player_team} is {position_contribution} % as {player_position} and overall is {team_contribution} %')
print(f'{player_name} in {target_team} will add {target_position_contribution} % as {player_position} and overall is {target_team_contribution} %')
# lets try to list the top 10 contribution

