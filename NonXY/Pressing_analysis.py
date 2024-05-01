# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 12:21:28 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

competition = 'Liga 1'
season = '2022-23'

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

league = df.loc[0]['Competition']
year = '2022-23'
team_name = 'PSS Sleman'
#date_ridwan = '2023-01-16'
date_new = '2023-03-07'

subtitle_string = f"{team_name} - {year}"
#subtitle_string = f"{league} | starting from {date}"
title_string = '%s performance' % (subtitle_string)

#odd = df.index[1::2]
#even = df.index[::2]
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

df_odd['Positional attacks opponent'] = df_even['Positional attacks']
df_even['Positional attacks opponent'] = df_odd['Positional attacks']
df_odd['Counterattacks opponent'] = df_even['Counterattacks']
df_even['Counterattacks opponent'] = df_odd['Counterattacks']

df_odd['Opponent positional attacks with shots'] = df_even['Positional attacks with shots']
df_even['Opponent positional attacks with shots'] = df_odd['Positional attacks with shots']
df_odd['Opponent counterattacks with shots'] = df_even['Counterattacks with shots']
df_even['Opponent counterattacks with shots'] = df_odd['Counterattacks with shots']

df_odd['Opponent positional attacks with shots %'] = df_even['Positional attacks with shots %']
df_even['Opponent positional attacks with shots %'] = df_odd['Positional attacks with shots %']
df_odd['Opponent counterattacks with shots %'] = df_even['Counterattacks with shots %']
df_even['Opponent counterattacks with shots %'] = df_odd['Counterattacks with shots %']

df_odd['Possession opponent'] = df_even['Possession, %']
df_even['Possession opponent'] = df_odd['Possession, %']
df_odd['Opponent passes to final third accurate'] = df_even['Passes to final third accurate']
df_even['Opponent passes to final third accurate'] = df_odd['Passes to final third accurate']
df_odd['Opponent penalty area entries'] = df_even['Penalty area entries']
df_even['Opponent penalty area entries'] = df_odd['Penalty area entries']
df_odd['Opponent touches in penalty area'] = df_even['Touches in penalty area']
df_even['Opponent touches in penalty area'] = df_odd['Touches in penalty area']

df_2 = pd.concat([df_odd, df_even])
df_2['xG difference'] = df_2['xG'] - df_2['xGA']

# team filter
df_team = df_2.loc[(df_2['Team'] == team_name)
#                   & (df_2['Date'] >= date_new)
                   ]
df_team = df_team.sort_values(by=['Date'], ascending=True).reset_index()
df_team = df_team.drop(['index'], axis=1)

# date-based filter
#df_date = df_xGA.loc[df_xGA['Date'] >= date]
#df_grouped_sum = df_date.groupby('Team').sum()
#df_grouped_mean = df_date.groupby('Team').mean()

# ingredients
ptf3 = df_team['Passes to final third accurate']
pae = df_team['Penalty area entries']
ptf3o = df_team['Opponent passes to final third accurate']
paeo = df_team['Opponent penalty area entries']
pt = df_team['Touches in penalty area']
pto = df_team['Opponent touches in penalty area']
paec = df_team['Penalty area entries via crosses']

bp = df_team['Possession, %']
bpo = df_team['Possession opponent']
pa = df_team['Positional attacks']
ca = df_team['Counterattacks']
bll = df_team['Ball losses low']
blm = df_team['Ball losses medium']
pao = df_team['Positional attacks opponent']
cao = df_team['Counterattacks opponent']

df_team['Goals difference'] = df_team['Goals'] - df_team['Conceded goals']
df_team['Passes to final third per possession'] = ptf3/bp
df_team['Touches in penalty area per possession'] = pt/bp
df_team['Touches in penalty area per successful final third pass'] = pt/ptf3
df_team['Penalty area entries via crosses %'] = paec/pae

df_team['Opponent passes to final third per possession'] = ptf3o/bpo
df_team['Opponent touches in penalty area per successful final third pass'] = pto/ptf3o

df_team['Positional attacks tendency'] = (pa/(pa+ca))*bp
df_team['Counterattacks tendency'] = (ca/(ca+pa))/bp
df_team['Opponent positional attacks tendency'] = (pao/(pao+cao))*bpo
df_team['Opponent counterattacks tendency'] = (cao/(cao+pao))/bpo

df_team['Ball losses medium + low per possession'] = (bll+blm)/bp
df_team['Ball losses low per possession'] = bll/bp


df_team.loc[df_team["Goals difference"] > 0, "Points gained"] = 3
df_team.loc[df_team["Goals difference"] == 0, "Points gained"] = 1
df_team.loc[df_team["Goals difference"] < 0, "Points gained"] = 0

x_value = 'PPDA'
y_value = 'Opponent passes to final third per possession'
c_value = 'xGA'
s_value = 'PPDA'

# scatter plot
x = df_team[x_value]
y = df_team[y_value]
c = df_team[c_value].tolist()
#ds = df_team[s_value]
#s = (((ds + (math.fabs(ds.min())*1.7))**2.7)).tolist()

fig, ax = plt.subplots(figsize = (12,12))
points = ax.scatter(x, y, c=c, s=150, cmap="summer")
#ax.get_xaxis().set_ticks([])
#ax.get_yaxis().set_ticks([])
#ax.invert_xaxis()
#ax.invert_yaxis()

ax.set_title(title_string, size="22")
ax.set_xlabel(x_value, size='14', labelpad=12)
ax.set_ylabel(y_value, size='14', labelpad=12)

# add xy mean line to cluster the plot into quadrants
x_min = x.min()
x_max = x.max()
y_min = y.min()
y_max = y.max()
xq_right = x.mean() + x.mean()/100
xq_left = x.mean() - x.mean()/100


plt.plot([x.mean(),x.mean()],[y_max,y_min],'k-', linestyle = ":", lw=1)
plt.plot([x_min,x_max],[y.mean(),y.mean()],'k-', linestyle = ":", lw=1)

# labels & legends
fig.colorbar(points, shrink=0.35, label=c_value)

# add credits
#CREDIT_1 = "Dot size = %s" % (s_value)
CREDIT_2 = "Data: wyscout"
CREDIT_3 = "@novalaziz"

fig.text(
    0.85, 0.07, f"{CREDIT_2}\n{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

#description for each quadrants
#ax.text(xq_left,y_max,"Nerds",size="10",ha='right')
#ax.text(xq_right,y_min,"Ball?? Are you nerd???",size="10")
#ax.text(xq_left,y_min,"Dude!?!?",size="10",ha='right')
#ax.text(xq_right,y_max,"Lets do both, we're supermen!",size="10")

# date-based filter
df_date = df_team.loc[df_team['Date'] >= date_new]
#df_grouped_sum = df_date.groupby('Team').sum()
#df_grouped_mean = df_date.groupby('Team').mean()

#label for each markers
label = df_team['Opponent']
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]), color = 'black', ha='center', va='bottom')
plt.show()