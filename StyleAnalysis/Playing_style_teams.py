# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 22:20:07 2023

@author: 62878

WARNING: something is wrong with date filtering
idk why, fuck
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math

competition = 'Liga 1'
year = '2022-23'

x_value = 'PPDA'
y_value = 'Average passes per possession'
c_value = 'xG difference'
s_value = 'xG'

date_filter = 'no'
date = '2023-01-11'
#team_highlight = 'Barito Putera'

os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition} {year}')
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

col_list = list(df.columns)

def modified_df():
    #odd = df.index[1::2]
    #even = df.index[::2]
    df_odd = df.loc[1::2].reset_index()
    df_odd = df_odd.drop(['index'], axis=1)
    df_even = df.loc[::2].reset_index()
    df_even = df_even.drop(['index'], axis=1)
    
    df_odd['xGA'] = df_even['xG']
    df_even['xGA'] = df_odd['xG']
    df_odd['Opponent'] = df_even['Team']
    df_even['Opponent'] = df_odd['Team']
    df_odd['Opponent possession'] = df_even['Possession, %']
    df_even['Opponent possession'] = df_odd['Possession, %']
    df_odd['Opponent shots'] = df_even['Shots']
    df_even['Opponent shots'] = df_odd['Shots']
    df_odd['Opponent touches in penalty area'] = df_even['Touches in penalty area']
    df_even['Opponent touches in penalty area'] = df_odd['Touches in penalty area']
    
    df_xGA = pd.concat([df_odd, df_even])
    df_xGA = df_xGA.loc[df_xGA['Date'] >= date] # use to filter from specific date
    df_xGA['xG difference'] = df_xGA['xG'] - df_xGA['xGA']
    
    ptf3 = df_xGA['Passes to final third accurate']
    pae = df_xGA['Penalty area entries']
    pp = df_xGA['Progressive passes accurate']
    bl = df_xGA['Ball losses']

    pt = df_xGA['Touches in penalty area']
    pto = df_xGA['Opponent touches in penalty area']

    bp = df_xGA['Possession, %']
    bpo = df_xGA['Opponent possession']
    dcp = df_xGA['Deep completed passes']
    dcc = df_xGA['Deep completed crosses']

    df_xGA['Passes to final third per possession'] = ptf3/bp
    df_xGA['Progressive passes per possession'] = pp/bp
    df_xGA['Ball losses per possession'] = bl/bp/100

    df_xGA['Touches in penalty area per possession'] = pt/bp
    df_xGA['Touches in penalty area per successful final third pass'] = pt/ptf3

    df_xGA['Deep completion per possession'] = (dcp+dcc)/bp
    df_xGA['Adjusted recoveries high'] = df_xGA['Recoveries high']/bp

    df_xGA['xGA/shot'] = df_xGA['xGA']/df_xGA['Opponent shots']
    
    return df_xGA

df_xGA = modified_df()

#league = df.loc[0]['Competition']
suptitle_string  = f"Playing Style - {competition} {year}"
if date_filter == 'yes':
    title_string = f'Different playing style based on press intensity & tendency to retain possession \nData from Wyscout | filtered from {date}'
    df_date = df_xGA.loc[df_xGA['Date'] >= date]
else:
    title_string = 'Different playing style based on press intensity & tendency to retain possession \nData from Wyscout | no date filter'
    df_date = df_xGA

df_grouped_sum = df_date.groupby('Team').sum(numeric_only=True)
df_grouped_mean = df_date.groupby('Team').mean(numeric_only=True)

# scatter plot
x = df_grouped_mean[x_value]
y = df_grouped_mean[y_value]
c = df_grouped_sum[c_value].tolist()
ds = df_grouped_mean[s_value]
s = (((ds + (math.fabs(ds.min())*2.6))**5.2)).tolist()

fig, ax = plt.subplots(figsize = (12,12))
points = ax.scatter(x, y, c=c, s=150, cmap="summer_r")

ax.invert_xaxis()
#ax.invert_yaxis()

plt.suptitle(suptitle_string, x=0.433, y=0.95, fontsize=25)
plt.title(title_string, x=0.484, fontsize=14)

#ax.set_title(title_string, size="22")
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
CREDIT_1 = "Dot size = %s" % (s_value)
CREDIT_3 = "@novalaziz"

fig.text(
    0.85, 0.07, f"{CREDIT_3}", size=10,
    color="#000000",
    ha="right"
)

#label for each markers
label = df_grouped_mean.index
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]), color = 'black', ha='center', va='bottom')
plt.show()