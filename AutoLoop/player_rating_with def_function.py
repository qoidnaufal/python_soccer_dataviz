#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:18:53 2023

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
min_minutes = 900
remove_gk = 'yes'
remove_wb = 'no'
merge_mf = 'yes' # pick yes or no

score_1 = 'Normalized score'
score_2 = 'Overall score'
score_to_show = 'all' # pick 1, 2, or all
score_to_plot = score_1
norm_scaler = 100 # pick 1 or 99 or 100

if score_to_show == '1':
    show_score = ['Player','Team within selected timeframe','Main position',f'{score_1}']
elif score_to_show == '2':
    show_score = ['Player','Team within selected timeframe','Main postion',f'{score_2}']
elif score_to_show == 'all':
    show_score = ['Player','Team within selected timeframe','Main position',f'{score_1}',f'{score_2}']

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()

#list_player = df['Player'].tolist()

# fixing some parameters
n_played = df['Minutes played'] / 90
pass_index = df['Passes per 90']

# progressive passes completed per 90
def progpass (*args):
    progpass_total = df['Progressive passes per 90'] * n_played
    progpass_compl = progpass_total * df['Accurate progressive passes, %'] /100
    df['Progressive passes completed per 90'] = (progpass_compl / n_played) /pass_index
    return df['Progressive passes completed per 90']

# passes to final third completed per 90
def pass_final3 (*args):
    f3_total = df['Passes to final third per 90'] * n_played
    f3_compl = f3_total * df['Accurate passes to final third, %'] /100
    df['Passes to final third completed per 90'] = (f3_compl / n_played) /pass_index
    return df['Passes to final third completed per 90']

# dribbles completed per 90
def dribble_90 ():
    dribble_total = df['Dribbles per 90'] * n_played
    dribble_compl = dribble_total * df['Successful dribbles, %'] /100
    df['Dribbles completed per 90'] = dribble_compl / n_played
    return df['Dribbles completed per 90']

# passes to penalty area completed per 90
def box_entry ():
    boxentry_total = df['Passes to penalty area per 90'] * n_played
    boxentry_compl = boxentry_total * df['Accurate passes to penalty area, %'] /100
    df['Passes to penalty area completed per 90'] = boxentry_compl / n_played
    return df['Passes to penalty area completed per 90']

# smart passes completed per 90
def smart_pass ():
    smartp_total = df['Smart passes per 90'] * n_played
    smartp_compl = smartp_total * df['Accurate smart passes, %'] /100
    df['Smart passes completed per 90'] = (smartp_compl / n_played) /pass_index
    return df['Smart passes completed per 90']

# crosses completed per 90
def crosses ():
    cross_total = df['Crosses per 90'] * n_played
    cross_compl = cross_total * df['Accurate crosses, %'] /100
    df['Crosses completed per 90'] = cross_compl / n_played
    return df['Crosses completed per 90']

# filtering based on minutes
def minute_filter ():
    dataframe = pd.concat([progpass(),
                           pass_final3(),
                           dribble_90(),
                           box_entry(),
                           smart_pass(),
                           crosses()],axis=1)
    dataframe = df.loc[df['Minutes played'] >= min_minutes]
    dataframe = dataframe.fillna(0)    
    return dataframe

# rename the position for grouping
def main_position():
    df = minute_filter()
    position_list = df['Position'].str.split(',').str[0]
    df['Position fix'] = position_list
    df.loc[df["Position fix"] == 'GK', "Main position"] = 'GK'
    df.loc[df["Position fix"].isin(['RB','LB']), "Main position"] = 'FB'
    df.loc[df["Position fix"].isin(['CB','LCB','RCB']), "Main position"] = 'CB'
    df.loc[df["Position fix"].isin(['DMF','LDMF','RDMF']), "Main position"] = 'DMF'
    df.loc[df["Position fix"].isin(['CMF','LCMF','RCMF','AMF']), "Main position"] = 'CMF'
    df.loc[df["Position fix"].isin(['RWB','LWB']), "Main position"] = 'WB'
    df.loc[df["Position fix"] == 'AMF', "Main position"] = 'AMF'
    df.loc[df["Position fix"].isin(['LAMF','RAMF','LW','RW','RWF','LWF']), "Main position"] = 'WG'
    df.loc[df["Position fix"] == 'CF', "Main position"] = 'CF'
    if remove_gk == 'yes':
        df = df[df['Main position'] != 'GK']
    else:
        None
    
    return df

# parameters
# player info
def player_info():
    player_info = ['Player',
                   'Team within selected timeframe',
                   'Main position'
                   ]
    return player_info

# goalkeeper
def goalkeeping():
    goalkeeping = ['Save rate, %',
                   'Prevented goals per 90',
                   'Duels won, %'
                   ]
    return goalkeeping

# attacking or goalscoring
def attacking():
    attacking = ['xG per 90',
                 'Shots per 90',
                 'Shots on target, %',
                 'Touches in box per 90',
                 'Offensive duels won, %'
                 ]
    return attacking

# passing
def passing():
    passing = ['Passes to final third completed per 90',
               'Progressive passes completed per 90'
               ]
    return passing

# playmaking
def playmaking():
    playmaking = ['Deep completions per 90',
                  'Shot assists per 90',
                  'Key passes per 90',
                  'Passes to penalty area completed per 90',
                  'Smart passes completed per 90',
                  'xA per 90'
                  ]
    return playmaking

# wingplay
def wingplay():
    wingplay = ['Deep completed crosses per 90',
                'Accurate crosses, %',
                'Crosses completed per 90'
                ]
    return wingplay

# ballcarrying
def ballcarrying():
    ballcarrying = ['Dribbles completed per 90',
                    'Progressive runs per 90'
                    ]
    return ballcarrying

# defending
def defending():
    defending = ['PAdj Sliding tackles',
                 'PAdj Interceptions',
                 'Defensive duels won, %'
                 ]
    return defending

# specifying parameters into each position to get z-score & percentile rank
# main function
function = stats.hmean

# fullback
def fb (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'FB'])
    ab = pd.concat([df[passing()],
                    df[playmaking()],
                    df[wingplay()],
                    df[ballcarrying()],
                    df[defending()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# centerback
def cb (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'CB'])
    ab = pd.concat([df[passing()],
                    df[ballcarrying()],
                    df[defending()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# wingbacks
def wb (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'WB'])
    ab = pd.concat([df[passing()],
                    df[playmaking()],
                    df[wingplay()],
                    df[ballcarrying()],
                    df[defending()],
                    df[attacking()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# defensive midfielders
def dmf (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'DMF'])
    ab = pd.concat([df[passing()],
                    df[ballcarrying()],
                    df[defending()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# center midfielders
def cmf (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'CMF'])
    ab = pd.concat([df[passing()],
                    df[playmaking()],
                    df[ballcarrying()],
                    df[defending()],
                    df[attacking()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# attacking midfielders
def amf (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'AMF'])
    ab = pd.concat([df[playmaking()],
                    df[ballcarrying()],
                    df[attacking()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# wingers
def wg (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'WG'])
    ab = pd.concat([df[playmaking()],
                    df[wingplay()],
                    df[ballcarrying()],
                    df[attacking()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# strikers
def cf (*args):
    df = main_position()
    df = df.apply(lambda x: x[df['Main position'] == 'CF'])
    ab = pd.concat([df[playmaking()],
                    df[ballcarrying()],
                    df[attacking()]],
                   axis=1)
    ab = ab.fillna(0)
    zscore = ab.apply(stats.zscore)
    percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))
    percentile['Overall score'] = function(percentile.iloc[:,:],axis=1)
    df = pd.concat([df[player_info()],percentile],axis=1)
    xmax = df['Overall score'].max()
    xmin = df['Overall score'].min()
    norm = df['Overall score'].apply(lambda i: (i-xmin)/(xmax-xmin) *norm_scaler)
    df['Normalized score'] = norm
    return df

# compiling all player into one dataframe
def player_score():
    
    if remove_wb == 'yes':
        score = pd.concat([
            cb()[show_score],
            fb()[show_score],
            dmf()[show_score],
            cmf()[show_score],
            amf()[show_score],
            wg()[show_score],
            cf()[show_score]
            ],axis=0)
    else:
        score = pd.concat([
           cb()[show_score],
           fb()[show_score],
           wb()[show_score],
           dmf()[show_score],
           cmf()[show_score],
           amf()[show_score],
           wg()[show_score],
           cf()[show_score]
           ],axis=0)
#    score = score.set_index(['Player'])
#    info['Overall score'] = [score.loc[i] for i in zip(info['Player'])]
    return score

zzy = player_score()

def plotdata():
    zzz = player_score()
    if merge_mf == 'yes':
        zzz['Main position'].replace(['DMF','CMF','AMF'], 'MF', inplace=True)
    else:
        zzz
    rating = zzz.groupby(['Team within selected timeframe',
                          'Main position']).mean(numeric_only=True)
    rating = rating.reset_index()
    rating = rating.pivot_table(score_to_plot,
                                ['Team within selected timeframe'],
                                'Main position')
    
    # normalizing the data
    sort_value = rating.mean(axis=1, skipna=True) # normalizing factor as well as sorting factor
    sum_value = rating.sum(axis=1) # this one is the normalizing factor
    rating = rating.apply(lambda x: (x/sum_value)*sort_value) # this is how i normalize it
    
    rating['Sort value'] = sort_value # insert the sorting factor into dataframe
    rating = rating.sort_values('Sort value')
    rating = rating.fillna(0) # replace nan with 0 because they cant be plotted
    return rating

zzz = plotdata()

# PLOT PLOT PLOT
teams_name = list(plotdata().index)
if remove_wb == 'no' and merge_mf == 'yes':
    rank_param = ['CB','FB','WB','MF','WG','CF']
    colors_all = ['#1D2F6F', '#0D98BA', '#93C572', '#FAC748', '#D9544D', '#5C4033']
elif remove_wb == 'no' and merge_mf == 'no':
    rank_param = ['CB','FB','WB','DMF','CMF','AMF','WG','CF']
    colors_all = ['#1D2F6F', '#0D98BA', '#93C572', '#F3E5AB', '#FAC748', '#DAA520', '#D9544D', '#5C4033']
elif remove_wb == 'yes' and merge_mf == 'yes':
    rank_param = ['CB','FB','MF','WG','CF']
    colors_all = ['#1D2F6F', '#0D98BA', '#FAC748', '#D9544D', '#5C4033']
else:
    rank_param = ['CB','FB','DMF','CMF','AMF','WG','CF']
    colors_all = ['#1D2F6F', '#0D98BA', '#F3E5AB', '#FAC748', '#DAA520', '#D9544D', '#5C4033']
    
rank_values = plotdata().loc[teams_name, :].values.tolist()
fields = rank_param

labels = teams_name

# figure and axis
fig, ax = plt.subplots(1, figsize=(12, 10), ncols=1, sharey=True)
fig.tight_layout() # not needed actually, unless you try 2 columns plot
plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.67, right=1.44) # to adjust spacing if i use 2 columns

# plot bars
left = len(plotdata()) * [1]
for idx, i in enumerate(fields):
    plt.barh(plotdata().index, plotdata()[i],left = left, color=colors_all[idx])
    left = left + plotdata()[i]

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
SUB_4 = f'{score_to_plot}'

fig.text(
    0.99, 0.9, f"{SUB_1} | {SUB_2} | {SUB_3} | {SUB_4}",
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
ax.legend(fields, bbox_to_anchor=([0.0000001, 1, 1, 0]), ncol=8, frameon=False)

# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')

plt.show()