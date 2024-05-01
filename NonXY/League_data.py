# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:24:56 2023

@author: 62878
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math
import numpy as np

from mplsoccer import Bumpy, FontManager, add_image

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
                     'Unnamed: 18':'Ball loses high',
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

#col_list = list(df.columns)

league = df.loc[0]['Competition']
year = '2022-23'
team = 'PSIS Semarang'
date = '2023-02-25'

subtitle_string = f"{league} | {year}"
title_string = 'xG Difference Distributions \n%s' % (subtitle_string)

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

df_2 = pd.concat([df_odd, df_even])
df_2['xG difference'] = df_2['xG'] - df_2['xGA']
df_2['Rank'] = ''
df_2['Opponent Rank'] = ''
#list_team = df_2['Team'].tolist()

df_2.loc[df_2["Team"] == 'PSM', "Rank"] = 1
df_2.loc[df_2["Team"] == 'Persib', "Rank"] = 2
df_2.loc[df_2["Team"] == 'Persija', "Rank"] = 3
df_2.loc[df_2["Team"] == 'Borneo FC', "Rank"] = 4
df_2.loc[df_2["Team"] == 'Madura United', "Rank"] = 5
df_2.loc[df_2["Team"] == 'Bali United', "Rank"] = 6
df_2.loc[df_2["Team"] == 'Bhayangkara F.C.', "Rank"] = 7
df_2.loc[df_2["Team"] == 'Persita', "Rank"] = 8
df_2.loc[df_2["Team"] == 'Persis Solo', "Rank"] = 9
df_2.loc[df_2["Team"] == 'Persebaya Surabaya', "Rank"] = 10
df_2.loc[df_2["Team"] == 'Arema', "Rank"] = 11
df_2.loc[df_2["Team"] == 'Persik Kediri', "Rank"] = 12
df_2.loc[df_2["Team"] == 'PSIS Semarang', "Rank"] = 13
df_2.loc[df_2["Team"] == 'Persikabo 1973', "Rank"] = 14
df_2.loc[df_2["Team"] == 'Dewa United', "Rank"] = 15
df_2.loc[df_2["Team"] == 'PSS Sleman', "Rank"] = 16
df_2.loc[df_2["Team"] == 'Barito Putera', "Rank"] = 17
df_2.loc[df_2["Team"] == 'Rans Nusantara', "Rank"] = 18

df_2.loc[df_2["Opponent"] == 'PSM', "Opponent Rank"] = 1
df_2.loc[df_2["Opponent"] == 'Persib', "Opponent Rank"] = 2
df_2.loc[df_2["Opponent"] == 'Persija', "Opponent Rank"] = 3
df_2.loc[df_2["Opponent"] == 'Borneo FC', "Opponent Rank"] = 4
df_2.loc[df_2["Opponent"] == 'Madura United', "Opponent Rank"] = 5
df_2.loc[df_2["Opponent"] == 'Bali United', "Opponent Rank"] = 6
df_2.loc[df_2["Opponent"] == 'Bhayangkara F.C.', "Opponent Rank"] = 7
df_2.loc[df_2["Opponent"] == 'Persita', "Opponent Rank"] = 8
df_2.loc[df_2["Opponent"] == 'Persis Solo', "Opponent Rank"] = 9
df_2.loc[df_2["Opponent"] == 'Persebaya Surabaya', "Opponent Rank"] = 10
df_2.loc[df_2["Opponent"] == 'Arema', "Opponent Rank"] = 11
df_2.loc[df_2["Opponent"] == 'Persik Kediri', "Opponent Rank"] = 12
df_2.loc[df_2["Opponent"] == 'PSIS Semarang', "Opponent Rank"] = 13
df_2.loc[df_2["Opponent"] == 'Persikabo 1973', "Opponent Rank"] = 14
df_2.loc[df_2["Opponent"] == 'Dewa United', "Opponent Rank"] = 15
df_2.loc[df_2["Opponent"] == 'PSS Sleman', "Opponent Rank"] = 16
df_2.loc[df_2["Opponent"] == 'Barito Putera', "Opponent Rank"] = 17
df_2.loc[df_2["Opponent"] == 'Rans Nusantara', "Opponent Rank"] = 18

df_2['Rank'] = pd.to_numeric(df_2['Rank'])
df_2['Opponent Rank'] = pd.to_numeric(df_2['Opponent Rank'])

df_2.loc[df_2["Opponent Rank"] <= 9, "Opponent Status"] = 'Top 9 teams'
df_2.loc[df_2["Opponent Rank"] > 9, "Opponent Status"] = 'Bottom 9 teams'

df_top9 = df_2.loc[df_2['Opponent Status'] == 'Top 9 teams']
df_bottom9 = df_2.loc[df_2['Opponent Status'] == 'Bottom 9 teams']

df_grouped_top9 = df_top9.groupby('Team').mean()
df_grouped_bottom9 = df_bottom9.groupby('Team').mean()

# preparing ingredients
df_grouped_top9.rename(columns = {'xG difference':'xGD/match vs top 9'}, inplace=True)
df_grouped_bottom9.rename(columns = {'xG difference':'xGD/match vs botttom 9'}, inplace=True)
y_value = 'xGD/match vs top 9'
x_value = 'xGD/match vs botttom 9'

# scatter plot
x = df_grouped_bottom9[x_value]
y = df_grouped_top9[y_value]


fig, ax = plt.subplots(figsize = (9,9))
points = ax.scatter(x, y, s=100, cmap="summer_r")
#ax.get_xaxis().set_ticks([])
#ax.get_yaxis().set_ticks([])

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

# add credits
CREDIT_1 = "Data: wyscout"
CREDIT_2 = "@novalaziz"

fig.text(
    0.9, 0.04, f"{CREDIT_1}\n{CREDIT_2}", size=10,
    color="#000000",
    ha="right"
)

#description for each quadrants
#ax.text(xq_left,y_max,"Nerds",size="10",ha='right')
#ax.text(xq_right,y_min,"Ball?? Are you nerd???",size="10")
#ax.text(xq_left,y_min,"Dude!?!?",size="10",ha='right')
#ax.text(xq_right,y_max,"Lets do both, we're supermen!",size="10")

#label for each markers
label = df_grouped_top9.index
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]), color = 'black', ha='center', va='bottom')
plt.show()