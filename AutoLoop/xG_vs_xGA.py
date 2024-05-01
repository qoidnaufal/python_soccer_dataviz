# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 16:41:07 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

competition = 'Liga 1'
season = '2022-23'

# data to plot
team_name = 'Persija'
x_value = 'Date'
y1_value = 'xG'
y2_value = 'xGA'
rolling_average = 'yes'
rolling_number = 4

y1_color = 'blue'
y2_color = 'red'

# coach change
coach_change = 0

if coach_change >= 1:
    coach1_date = '2022-09-22'
    coach2_date = '2023-02-11'
    coach1_name = ' Rodney Goncalves'
    coach2_name = ' Rahmad Darmawan'
else:
    None

# team filter & plot title
title_string = f'{y1_value} vs {y2_value} Performance | {team_name}'
subtitle_string = f'{competition} | Data from Wyscout | Rolling average every 4 games'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition} {season}')
extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
df = df.loc[(df['Match'].str.contains('nan')==False)]
df = df.reset_index()
df = df.drop(['index'], axis=1)


df.rename(columns = {'Shots / on target':'Shots',
                     'Unnamed: 9':'Shots on target',
                     'Unnamed: 10':'Shots accurate %',
                     'Passes / accurate':'Passes',
                     'Unnamed: 12':'Passes completed',
                     'Unnamed: 13':'Passes accurate %',
                     'Losses / Low / Medium / High':'Ball losses',
                     'Unnamed: 16':'Ball losses low',
                     'Unnamed: 17':'Ball losses medium',
                     'Unnamed: 18':'Ball losses high',
                     'Recoveries / Low / Medium / High':'Recoveries',
                     'Unnamed: 20':'Recoveries low',
                     'Unnamed: 21':'Recoveries medium',
                     'Unnamed: 22':'Recoveries high',
                     'Duels / won':'Duels',
                     'Unnamed: 24':'Duels won',
                     'Unnamed: 25':'Duels won %',
                     'Shots from outside penalty area / on target':'Shots from outside penalty area',
                     'Unnamed: 27':'Shots from outside penalty area on target',
                     'Unnamed: 28':'Shots from outside penalty area accurate %',
                     'Positional attacks / with shots':'Positional attacks',
                     'Unnamed: 30':'Positional attacks with shots',
                     'Unnamed: 31': 'Positional attacks with shots %',
                     'Counterattacks / with shots':'Counterattacks',
                     'Unnamed: 33':'Counterattacks with shots',
                     'Unnamed: 34': 'Counterattacks with shots %',
                     'Set pieces / with shots': 'Set pieces',
                     'Unnamed: 36':'Set pieces with shots',
                     'Unnamed: 37':'Set pieces with shots %',
                     'Corners / with shots':'Corners',
                     'Unnamed: 39': 'Corners with shots',
                     'Unnamed: 40': 'Corners with shots %',
                     'Free kicks / with shots':'Free kicks',
                     'Unnamed: 42':'Free kicks with shots',
                     'Unnamed: 43':'Free kicks with shots %',
                     'Penalties / converted':'Penalties',
                     'Unnamed: 45':'Penalties converted',
                     'Unnamed: 46':'Penalties converted %',
                     'Crosses / accurate':'Crosses',
                     'Unnamed: 48':'Crosses accurate',
                     'Unnamed: 49':'Crosses accurate %',
                     'Penalty area entries (runs / crosses)':'Penalty area entries',
                     'Unnamed: 53':'Penalty area entries via runs',
                     'Unnamed: 54': 'Penalty area entries via crosses',
                     'Offensive duels / won':'Offensive duels',
                     'Unnamed: 57':'Offensive duels won',
                     'Unnamed: 58':'Offensive duels won %',
                     'Shots against / on target':'Shots conceded',
                     'Unnamed: 62':'Shots conceded on target',
                     'Unnamed: 63':'Shots conceded on target %',
                     'Defensive duels / won':'Defensive duels',
                     'Unnamed: 65':'Defensive duels won',
                     'Unnamed: 66':'Defensive duels won %',
                     'Aerial duels / won':'Aerial duels',
                     'Unnamed: 68':'Aerial duels won',
                     'Unnamed: 69':'Aerial duels won %',
                     'Sliding tackles / successful':'Tackles',
                     'Unnamed: 71':'Tackles success',
                     'Unnamed: 72':'Tackles success %',
                     'Forward passes / accurate':'Forward passes',
                     'Unnamed: 79':'Forward passes accurate',
                     'Unnamed: 80':'Forward passes accurate %',
                     'Back passes / accurate':'Back passes',
                     'Unnamed: 82':'Back passes accurate',
                     'Unnamed: 83':'Back passes accurate %',
                     'Lateral passes / accurate':'Lateral passes',
                     'Unnamed: 85':'Lateral passes accurate',
                     'Unnamed: 86':'Lateral passes accurate %',
                     'Long passes / accurate':'Long passes',
                     'Unnamed: 88':'Long passes accurate',
                     'Unnamed: 89':'Long passes accurate %',
                     'Passes to final third / accurate':'Passes to final third',
                     'Unnamed: 91':'Passes to final third accurate',
                     'Unnamed: 92':'Passes to final third accurate %',
                     'Progressive passes / accurate':'Progressive passes',
                     'Unnamed: 94':'Progressive passes accurate',
                     'Unnamed: 95':'Progressive passes accurate %',
                     'Smart passes / accurate':'Smart passes',
                     'Unnamed: 97':'Smart passes accurate',
                     'Unnamed: 98':'Smart passes accurate %',
                     'Throw ins / accurate':'Throw ins',
                     'Unnamed: 100':'Throw ins accurate',
                     'Unnamed: 101':'Throw ins accurate %'                     
                     }, inplace = True)

col_list = list(df.columns)

def modified_df():
    df_odd = df.loc[1::2].reset_index()
    df_odd = df_odd.drop(['index'], axis=1)
    df_even = df.loc[::2].reset_index()
    df_even = df_even.drop(['index'], axis=1)
    
    df_odd['Opponent'] = df_even['Team']
    df_even['Opponent'] = df_odd['Team']
    df_odd['xGA'] = df_even['xG']
    df_even['xGA'] = df_odd['xG']
    df_odd['PPDA against'] = df_even['PPDA']
    df_even['PPDA against'] = df_odd['PPDA']
    
    df_2 = pd.concat([df_odd, df_even])
    
    df_2['xG difference'] = df_2['xG'] - df_2['xGA']
    df_2['Goals difference'] = df_2['Goals'] - df_2['Conceded goals']
    df_2.loc[df_2["Goals difference"] > 0, "Points gained"] = 3
    df_2.loc[df_2["Goals difference"] == 0, "Points gained"] = 1
    df_2.loc[df_2["Goals difference"] < 0, "Points gained"] = 0
    
    df_2 = df_2.sort_values(by=(['Date', 'Match']), ascending=True).reset_index()
    df_2 = df_2.drop(['index'], axis=1)
    
    return df_2

df_2 = modified_df()

df_team = df_2.loc[df_2['Team'] == team_name]
df_team[f'{y1_value}_rolling'] = df_team.xG.rolling(rolling_number).mean()
df_team[f'{y2_value}_rolling'] = df_team.xGA.rolling(rolling_number).mean()

# PLOT PLOT PLOT
x = df_team[x_value]

if rolling_average == 'yes':
    y1 = df_team[f'{y1_value}_rolling']
    y2 = df_team[f'{y2_value}_rolling']
else:    
    y1 = df_team[y1_value]
    y2 = df_team[y2_value]

x = np.array(x)
y1 = np.array(y1)
y2 = np.array(y2)

# line plot xG difference
fig, ax = plt.subplots(figsize = (20,8))
  
#use plot() method on the dataframe
plt.plot(x, y1, color = y1_color, linewidth=3)
plt.plot(x, y2, color = y2_color, linewidth=3)

# plotting coach change line
if coach_change >= 1:
    def date_1():
        zzzzz = np.where((x > coach1_date))
        zzzzz = np.asarray(zzzzz)
        zzzzz = np.transpose(zzzzz)
        zx = zzzzz[0]
        date1 = x[zx]
        return date1
    
    def date_2():
        zzzzz = np.where((x > coach2_date))
        zzzzz = np.asarray(zzzzz)
        zzzzz = np.transpose(zzzzz)
        zx = zzzzz[0]
        date2 = x[zx]
        return date2
    
    date1 = date_1()
    date2 = date_2()
    
    coach1_xline = (np.array([date1, date1])).ravel()
    coach2_xline = (np.array([date2, date2])).ravel()
    
    y1_min = df_team[f'{y1_value}_rolling'].min()
    y1_max = df_team[f'{y1_value}_rolling'].max()
    y2_min = df_team[f'{y2_value}_rolling'].min()
    y2_max = df_team[f'{y2_value}_rolling'].max()
    
    if y1_min < y2_min:
        a = y1_min
    elif y1_min > y2_min:
        a = y2_min
    else:
        a = y1_min
        
    if y1_max > y2_max:
        b = y1_max
    elif y1_max < y2_max:
        b = y2_max
    else:
        b = y1_max
    
    coach1_yline = np.array([a, b])
    coach2_yline = np.array([a, b])
else:
    None

if coach_change == 2:
    plt.plot(coach1_xline, coach1_yline, color = 'black', lw=1.3, ls='--')
    plt.text(date1, b, coach1_name, fontsize = 12)
    
    plt.plot(coach2_xline, coach2_yline, color = 'black', lw=1.3, ls='--')
    plt.text(date2, b, coach2_name, fontsize = 12)
elif coach_change == 1:
    plt.plot(coach1_xline, coach1_yline, color = 'black', lw=1.3, ls='--')
    plt.text(date1, b, coach1_name, fontsize = 12)
else:
    None

# fill to the area
ax.fill_between(x, y1, y2, where=y1>y2, facecolor= y1_color, alpha=0.6, interpolate=True)
ax.fill_between(x, y1, y2, where=y1<y2, facecolor= y2_color, alpha=0.6, interpolate=True)

plt.xticks(rotation = 'vertical')

plt.suptitle(title_string, y=0.96, fontsize=25)
plt.title(subtitle_string, x=0.484, fontsize=16)
plt.legend([f"{y1_value}", f"{y2_value}"], loc ="lower right")

plt.show()