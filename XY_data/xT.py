# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 15:05:03 2022

@author: 62878
"""

import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

""" Filters """
position = [2, 34, 5, 6, 8, 10, 7, 9, 11]
minimum_minutes_played = 10
avg_minutes = 10
Team_name = 'PSIS'
Match = 20220617
Line_height = 70

""" Main dataframe """
os.chdir('/Users/qoidnaufal/Documents/Learn Python/Piala Presiden')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
df = pd.concat([pd.read_csv(f) for f in all_filenames])

df = df.loc[df['Position_id'].isin(position)]
df = df.loc[df['Team'].isin([Team_name])]
#df = df.loc[df['Match_id'].isin([Match])]

""" the xT grid """
xT = pd.read_csv('/Users/qoidnaufal/Documents/Learn Python/xT_DS.csv',header=None)
#And then change it into an array
xT = np.array(xT)
xT_rows,xT_cols = xT.shape
xT_cols
xT_rows

def minutes_played():
    mp = df.loc[df['Event'].isin(['Play_in','Play_out'])]
    mp = mp.groupby(['Team','Player','Position_id','Match_id','Half_id','Event']).sum()
    mp = pd.pivot_table(data=mp, values=['Mins'], index=['Team','Player'], columns=['Event'], aggfunc='sum')
    mp['Total'] = mp[('Mins','Play_out')] - mp[('Mins','Play_in')]
    mp['p%s' % (avg_minutes)] = np.divide(mp[('Total','')],avg_minutes)
    
    mp = pd.DataFrame(mp)
        
    return mp

total_minutes = minutes_played()

""" Event filters """
Actions_1 = ['Pass_success', 'Cross_success', 'Carry']
Actions_2 = ['Pass_success', 'Cross_success']
Actions_3 = ['Pass_success', 'Carry']

def xT_pivot():  
    df_1 = df.loc[df['Event'].isin(Actions_1)]
    #df_x = df.loc[df['Event'].isin(['Pass_failed'])]

    df_1 = df_1[df_1.X2.apply(lambda x: x.isnumeric())]
    df_1['X2'] = df_1['X2'].astype(float)
    df_1['Y2'] = df_1['Y2'].astype(float)

    direct_1 = df_1.loc[df_1['Direction_id'] == 1]
    direct_2 = df_1.loc[df_1['Direction_id'] == 2]

    #conversion for sliced dataframe
    
    direct_2['X'] = direct_2['X'].apply(lambda x: 100-x)
    direct_1['Y'] = direct_1['Y'].apply(lambda x: 100-x)
    direct_2['X2'] = direct_2['X2'].apply(lambda x: 100-x)
    direct_1['Y2'] = direct_1['Y2'].apply(lambda x: 100-x)

    df_2 = pd.concat([direct_1, direct_2])
    
    #line height filters
    #df_2 = df_2.loc[df_2['X'] > (Line_height)]

    df_2['x1_bin'] = pd.cut(df_2['X'], bins = xT_cols, labels = False)
    df_2['y1_bin'] = pd.cut(df_2['Y'], bins = xT_rows, labels = False)
    df_2['x2_bin'] = pd.cut(df_2['X2'], bins = xT_cols, labels = False)
    df_2['y2_bin'] = pd.cut(df_2['Y2'], bins = xT_rows, labels = False)

    df_2['start_zone_value'] = df_2[['x1_bin','y1_bin']].apply(lambda x: xT[x[1]][x[0]],axis=1)
    df_2['end_zone_value'] = df_2[['x2_bin','y2_bin']].apply(lambda x: xT[x[1]][x[0]],axis=1)

    df_2['xT'] = np.subtract(df_2['end_zone_value'],df_2['start_zone_value'])
    
    #can swap the index between ['Player'] or ['Player','Team'] or ['Team','Player']
    
    xT_pivot = pd.pivot_table(data=df_2, values=['xT'], index=['Team','Player'], columns=['Event'], aggfunc='sum')
    xT_pivot = xT_pivot.fillna(0)
    xT_pivot['Carry_p%s' % (avg_minutes)] = np.divide(xT_pivot[('xT','Carry')],total_minutes['p%s' % (avg_minutes),''])
    xT_pivot['Pass_p%s' % (avg_minutes)] = np.divide(xT_pivot[('xT','Pass_success')],total_minutes['p%s' % (avg_minutes),''])
    xT_pivot['Cross_p%s' % (avg_minutes)] = np.divide(xT_pivot[('xT','Cross_success')],total_minutes['p%s' % (avg_minutes),''])
    
    xT_pivot = pd.concat([total_minutes, xT_pivot], axis=1)
    
    return xT_pivot

xT_pivot = xT_pivot()
xT_pivot = xT_pivot[xT_pivot['Total','']>=minimum_minutes_played]

#xT_pivot = xT_pivot.filter(like = (Team_name), axis=0)
label = xT_pivot.index

#(df['Event']=='Pass_success').sum()

""" Histogram """
#xT_pivot.hist(('Pass_p%s' % (avg_minutes),''), bins=10)
#xT_pivot.hist(('Cross_p%s' % (avg_minutes),''), bins=10)
#xT_pivot.hist(('Carry_p%s' % (avg_minutes),''), bins=10)

""" BAR PLOT """
xT_pivot.sort_values(('Pass_p%s' % (avg_minutes), '')).plot(kind='barh',y=('Pass_p%s' % (avg_minutes),''),color='green',figsize=(20,20))
xT_pivot.sort_values(('Cross_p%s' % (avg_minutes), '')).plot(kind='barh',y=('Cross_p%s' % (avg_minutes),''),color='green',figsize=(20,20))
xT_pivot.sort_values(('Carry_p%s' % (avg_minutes), '')).plot(kind='barh',y=('Carry_p%s' % (avg_minutes),''),color='green',figsize=(20,20))


""" SCATTER PLOT """
x = xT_pivot[('Carry_p%s' % (avg_minutes),'')]
y = xT_pivot[('Pass_p%s' % (avg_minutes),'')]

fig, ax = plt.subplots(figsize = (13,9))
plt.plot(x,y,"o")
#ax.set_title("Karakter Main %s" % (position), size="22")
ax.set_xlabel("Kemampuan dribble ke depan")
ax.set_ylabel("Kemampuan passing ke depan")

x_min = x.min()*1.1
x_max = x.max()*1.1
y_min = y.min()*1.1
y_max = y.max()*1.1

#the xy mean line to cluster the plot into quadrants
plt.plot([x.mean(),x.mean()],[y_max,y_min],'k-', linestyle = ":", lw=1)
plt.plot([x_min,x_max],[y.mean(),y.mean()],'k-', linestyle = ":", lw=1)

#description for each quadrants
ax.text(x_min,y_max,"Jago passing ke depan",color="blue",size="10")
ax.text(x_max,y_min,"Jago dribbling ke depan",color="blue",size="10",ha='right')
ax.text(x_min,y_min,"Cuma main aman",color="red",size="10")
ax.text(x_max,y_max,"Jago dribble & passing ke depan",color="green",size="10",ha='right')

#label for each markers
for i, txt in enumerate(label):
    ax.annotate(txt, (x[i], y[i]), color = 'black')
plt.show()