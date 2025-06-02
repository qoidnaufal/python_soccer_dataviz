#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 20:55:01 2024

@author: qoidnaufal
"""

import glob
import os
import pandas as pd

class League:
    def __init__(self, competition: str, season: str):
       self.competition = competition
       self.season = season
       
    def dataFrame(self):
        os.chdir(f'/Users/qoidnaufal/Documents/Wyscout/Player data/{self.competition} {self.season}')
        extension = 'xlsx'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))] # explain for loop & range + len
        df = pd.concat([pd.read_excel(f) for f in all_filenames]).drop_duplicates()
        return df
    
    def col_list(self):
        return list(self.dataFrame().columns)
    
    def calc(self):
        df = self.dataFrame()
        df["Accurate passes per 90"] = df["Passes per 90"] * df["Accurate passes, %"] / 100
        df["Average minutes per game"] = df["Minutes played"] / df["Matches played"]
        
        df = df.loc[(
                #(df['Position'].str.contains("CB")) &
                (df["Minutes played"] >= 450)
                & (df["Average minutes per game"] >= 45)
            )]
        
        return df

efbet = League("Bulgarian EfBet", "2023-24")
liga1 = League("Liga 1", "2022-23")

col_list = efbet.col_list()

df_efbet = efbet.calc()
df_liga1 = liga1.calc()

avg_pass_efbet = df_efbet.loc[:, "Accurate passes per 90"].mean() * 22
avg_pass_liga1 = df_liga1.loc[:, "Accurate passes per 90"].mean() * 22