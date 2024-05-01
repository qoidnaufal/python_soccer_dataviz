#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 19:07:56 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
#import scipy.stats as stats
import matplotlib.pyplot as plt
#import numpy as np

competitions = [
    "Liga 1 2022-23",
    "Thai League 1 2022-23",
    "Malaysian Super League 2023",
    "K3 League 2023",
    "Estonia PL 2023",
    "K2 League 2022",
    "Bundesliga 2 2022-23",
    "Premier League 2022-23",
    "J League 2022"
    ]

def parse(competition):
    os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition}')
    extension = 'xlsx'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
    df = df.dropna()
    df = df.rename(columns={
        "Passes / accurate": "Passes",
        "Unnamed: 12": "Passes completed",
        "Unnamed: 13": "Pass completion, %",
        "Recoveries / Low / Medium / High": "Recoveries",
        "Duels / won": "Duels",
        "Unnamed: 24": "Duels won",
        "Sliding tackles / successful": "Sliding tackles",
        "Unnamed: 71": "Tackle success",
        })
    
    Intensity = [
        'Average of Completed Passes per Minute',
        'Recoveries per minute']
    
    df = df.groupby("Match").mean()
    df["Duration"] = df["Duration"] / 2
    
    df["Average of Completed Passes per Minute"] = df["Passes completed"] / df["Duration"]
    
    #df["Interceptions per minute"] = df["Interceptions"] / df["Duration"]
    df["Duels per minute"] = df["Duels"] / df["Duration"]
    
    df["Recoveries per minute"] = df["Recoveries"] / df["Duration"]
    
    #df['Intensity'] = stats.hmean(df[Intensity], axis=1)
    df['Intensity'] = df[Intensity].mean(axis=1)
    
    p = df["Intensity"].mean()
    q = df["Intensity"].std()
    return p, q

#for competition in competitions:
#    d = {competition: parse(competition)}

d = {competition: parse(competition) for competition in competitions}
df = pd.DataFrame(d).transpose().rename(columns= {0: "Intensity", 1: "Std dev"})

fig, ax = plt.subplots(figsize=(11,7))

ax.errorbar(range(len(df.index)), df["Intensity"], df["Std dev"], fmt='o', linewidth=2, capsize=6)
plt.grid(axis = 'y')
ax.set_xticks([])

plt.suptitle("Intensity Index", x=0.5, y=0.950, fontsize=16)
plt.title("How different are Liga 1 games compared to other leagues?",
          x=0.485, fontsize=10)

#label for each markers
#label = df.index
for i, txt in enumerate(df.index):
    ax.annotate(txt, (range(len(df.index))[i], df["Intensity"][i]), color = 'black', ha='center', va='bottom')

plt.show()