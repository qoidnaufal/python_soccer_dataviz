#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 19:07:56 2023

@author: qoidnaufal
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

competition_1 = "Liga 1 2022-23"
competition_2 = "Thai League 1 2022-23"
competition_3 = "Malaysian Super League 2023"
competition_4 = "K3 League 2023"
competition_5 = "Estonia PL 2023"
competition_6 = "K2 League 2022"
competition_7 = "Premier League 2022-23"

things_to_check = "Average of Completed Passes per Minute"

def parse1(competition):
    os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Team data/{competition}')
    extension = 'xlsx'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
    df = df.dropna()
    df = df.rename(columns={
        "Passes / accurate": "Passes",
        "Unnamed: 12": "Passes completed",
        "Unnamed: 13": "Pass completion, %",
        "Recoveries / Low / Medium / High": "Recoveries"
        })
    df = df.groupby("Match").mean()
    df["Duration"] = df["Duration"] / 2
    #df = df[["Team","Duration","Passes","Passes completed","Possession, %"]]
    df["Passes normalized by minute"] = df["Passes completed"] * 90 / df["Duration"]
    #df["Passes normalized"] = df["Passes normalized by minutes"] * 50 / df["Possession, %"]
    df["Average of Completed Passes per Minute"] = df["Passes normalized by minute"] / 90
    
    #average_pass_perminute = df["Average pass per minute"].mean()
    #standard_deviation = df["Average pass per minute"].std()
    
    p = df[things_to_check].mean()
    q = df[things_to_check].std()
    return p, q

a = parse1(competition_1)
b = parse1(competition_2)
c = parse1(competition_3)
d = parse1(competition_4)
e = parse1(competition_5)
f = parse1(competition_6)
g = parse1(competition_7)

df = pd.DataFrame.from_records(
    [(f"{competition_1}", *a),
     (f"{competition_2}", *b),
     (f"{competition_3}", *c),
     (f"{competition_4}", *d),
     (f"{competition_5}", *e),
     (f"{competition_6}", *f),
     (f"{competition_7}", *g)],
    columns=["Competition", things_to_check, 'Std Dev']
    )

fig, ax = plt.subplots(figsize=(11,7))

ax.errorbar((1, 2, 3, 4, 5, 6, 7), df[things_to_check], df["Std Dev"], fmt='o', linewidth=2, capsize=6)

ax.set(xlim=(0, 4), xticks=np.arange(1, 9),
       ylim=((df[things_to_check].min() - df["Std Dev"].max() - 0.5),
             (df[things_to_check].max() + df["Std Dev"].max() + 0.5)),
       yticks=np.arange((df[things_to_check].min() - df["Std Dev"].max() - 0.5),
                        (df[things_to_check].max() + df["Std Dev"].max() + 0.5))
       )
ax.set_xticks([])
plt.suptitle(f"{things_to_check}", x=0.5, y=0.950, fontsize=16)
plt.title("How different are Liga 1 games compared to other leagues?",
          x=0.485, fontsize=10)

plt.grid(axis = 'y')

# add credits
CREDIT_1 = "Data: Wyscout"
CREDIT_2 = "@novalaziz"

fig.text(
    0.889, 0.135, f"{CREDIT_1}\n{CREDIT_2}", size=8,
    color="#000000",
    ha="right"
)

#label for each markers
label = df["Competition"]
for i, txt in enumerate(label):
    ax.annotate(txt, ([1, 2, 3, 4, 5, 6, 7][i], df[things_to_check][i]), color = 'black', ha='center', va='bottom')

plt.show()