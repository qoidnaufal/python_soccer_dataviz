import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("data2526/xg_all_shots.xlsx")
dfShots = df[["Team", "Event"]].groupby(["Team"]).count()
dfAllGoals = df.loc[df["Event"].str.contains("Goal")]
dfTeamGoals = dfAllGoals[["Team", "Event"]].rename(columns={ "Event": "Goal" }).groupby(["Team"]).count()

# ###################################################
#
#                  df Counter Attack
#
# ###################################################

dfCounterAttacks = df.loc[df["Situation"].str.contains("Counter Attack")]
dfCounterAttackGoals = dfCounterAttacks.loc[dfCounterAttacks["Event"].str.contains("Goal")]
dfGoalsScoredFromCounterAttack = dfCounterAttackGoals[["Team", "Event"]].groupby(["Team"]).count()
dfGoalsConcededFromCounterAttack = dfCounterAttackGoals[["Opponent", "Event"]].rename(columns={ "Opponent": "Team", "Event": "Conceded" }).groupby(["Team"]).count()[["Conceded"]]
dfTeamShotsFromCounterAttack = dfCounterAttacks[["Team", "Event"]].groupby(["Team"]).count().rename(columns={ "Event": "Shots" })[["Shots"]]
dfTeamShotsConcededFromCounterAttack = dfCounterAttacks[["Opponent", "Event"]].rename(columns={ "Opponent": "Team", "Event": "SC" }).groupby(["Team"]).count()
dfXGFromCounterAttack = dfCounterAttacks[["Team", "xG"]].groupby(["Team"]).sum()[["xG"]].sort_values(by=["xG"], ascending=False)
dfXGConcededFromCounterAttack = dfCounterAttacks[["Opponent", "xG"]].rename(columns={ "Opponent": "Team" }).groupby(["Team"]).sum()[["xG"]]

# ###################################################
#
#                    df Team Data
#
# ###################################################

dfTeamData = df[["Team", "xG"]].rename(columns={ "xG": "xG Total" }).groupby(["Team"]).sum()
dfTeamData["Goals"] = dfTeamGoals
dfTeamData["Shots"] = dfShots

dfTeamData["CA Shots"] = dfTeamShotsFromCounterAttack
dfTeamData["CA Shots"] = dfTeamData["CA Shots"].fillna(0)
dfTeamData["CA Shots"] = dfTeamData["CA Shots"].astype(int)

dfTeamData["CA Goals"] = dfGoalsScoredFromCounterAttack
dfTeamData["CA Goals"] = dfTeamData["CA Goals"].fillna(0)
dfTeamData["CA Goals"] = dfTeamData["CA Goals"].astype(int)

dfTeamData["CA xG"] = dfXGFromCounterAttack
dfTeamData["CA xG"] = dfTeamData["CA xG"].fillna(0)

# dfTeamData["CA xG/S"] = dfTeamData["CA xG"] / dfTeamData["CA Shots"]
# dfTeamData["CA xG/S"] = dfTeamData["CA xG/S"].fillna(0)
dfTeamData["CA Pro"] = dfTeamData["CA xG"].apply(lambda x: x * 0.7) + dfTeamData["CA Goals"].apply(lambda x: x * 0.3)

dfTeamData["CA SC"] = dfTeamShotsConcededFromCounterAttack
dfTeamData["CA SC"] = dfTeamData["CA SC"].fillna(0)
dfTeamData["CA SC"] = dfTeamData["CA SC"].astype(int)

dfTeamData["CA Ccd"] = dfGoalsConcededFromCounterAttack
dfTeamData["CA Ccd"] = dfTeamData["CA Ccd"].fillna(0)
dfTeamData["CA Ccd"] = dfTeamData["CA Ccd"].astype(int)

dfTeamData["CA xGC"] = dfXGConcededFromCounterAttack
dfTeamData["CA xGC"] = dfTeamData["CA xGC"].fillna(0)

dfTeamData["CA Vuln"] = dfTeamData["CA xGC"].apply(lambda x: x * 0.7) + dfTeamData["CA Ccd"].apply(lambda x: x * 0.3)

# print(dfTeamData[["CA Shots", "CA Goals", "CA xG", "CA SC", "CA Ccd", "CA xGC", "CA Pro", "CA Vuln"]].sort_values(by=["CA Pro"], ascending=False))
print(dfTeamData.sort_values(by=["CA Pro"], ascending=False))

# ###################################################
#
#                 total shots & xG
#
# ###################################################

# xGAllScoredGoals = dfAllGoals["xG"].sum()
totalGoals = dfAllGoals["Player"].count()
totalXG = dfTeamData["xG Total"].sum()
totalShots = df["Event"].count()

# ###################################################
#
#           shots + xG from Counter Attack
#
# ###################################################

xGFromCounterAttacks = dfCounterAttacks["xG"].sum()
# xGScoredFromCounterAttacks = dfCounterAttackGoals["xG"].sum()
totalCounterAttackGoals = dfTeamData["CA Goals"].sum()
totalCounterAttackShots = dfCounterAttacks["Event"].count()

print(f"\ntotal shots: {totalShots}")
print(f"total xG: {totalXG}")
print(f"total goals scored: {totalGoals}")

print(f"\nshots from counter attacks: {totalCounterAttackShots}")
print(f"goals scored from counter attacks: {totalCounterAttackGoals}")
print(f"total xG from counter attacks: {xGFromCounterAttacks}")

# ###################################################
#
#                   Player Section
#
# ###################################################

dfPlayerData = dfCounterAttacks[["Player", "Event"]].groupby(["Player"]).count().rename(columns={ "Event": "CA Shots" })
dfPlayerXGFromCounterAttack = dfCounterAttacks[["Player", "xG"]].groupby(["Player"]).sum()
dfPlayerData["CA xG"] = dfPlayerXGFromCounterAttack
dfPlayerData["CA xG/Shot"] = dfPlayerData["CA xG"] / dfPlayerData["CA Shots"]
dfPlayerData["CA Goals"] = dfCounterAttackGoals[["Player", "Event"]].rename(columns={ "Event": "CA Goals" }).groupby("Player").count()
dfPlayerData["CA Goals"] = dfPlayerData["CA Goals"].fillna(0)
dfPlayerData["CA Goals"] = dfPlayerData["CA Goals"].astype(int)
dfPlayerData["CA Threat"] = dfPlayerData["CA Goals"].apply(lambda x: x * 0.3) + dfPlayerData["CA xG"].apply(lambda x: x * 0.7)

topTenShooter = dfPlayerData.sort_values(by = ["CA Shots"], ascending=False).head(10)
# topTenXG = dfPlayerData.sort_values(by = ["CA xG"], ascending=False).head(10)
topTenThreat = dfPlayerData.sort_values(["CA Threat"], ascending=False).head(10)

print(f"\nTop Ten Counter Attack Outlet (Shots):\n{topTenShooter}")
# print(f"\nTop Ten Counter Attack Outlet (xG):\n{topTenXG}")
print(f"\nTop Ten Counter Attack Outlet (Threat):\n{topTenThreat}")

# ###################################################
#
#                Plot Shots vs CA Shots
#
# ###################################################

"""
dfTeamData = dfTeamData.sort_values(by=["Shots"], ascending=False)
fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
width = 0.4
idx = np.arange(len(dfTeamData))

shots_label = dfTeamData["Shots"].to_list()
shots = ax.barh(idx-width/2, dfTeamData["Shots"], width, color="#04519f")
ax.bar_label(shots, labels=shots_label, padding=3)

ca_label = dfTeamData["CA Shots"].to_list()
ca_shots = ax.barh(idx+width/2, dfTeamData["CA Shots"], width, color="orange")
ax.bar_label(ca_shots, labels=ca_label, padding=3)

ax.set_yticks(idx, dfTeamData.index)
ax.invert_yaxis()

ax.spines[["top", "right"]].set_visible(False)
ax.get_xaxis().set_visible(False)
ax.margins(y=-0.0005)

ax.legend(["Semua tembakan", "Tembakan dari counter attack"])
title = ax.set_title("Kontribusi Serangan Balik\nTerhadap Total Tembakan")
title.set(fontsize='xx-large', fontweight='bold')

plt.show()
"""

# ###################################################
#
#                  export to excell
#
# ###################################################

# dfTeamData.sort_values(by=["CA Pro"], ascending=False).to_excel("./data2526/team_data_output.xlsx")
# dfPlayerData.sort_values(by = ["CA Shots"], ascending=False).head(10).to_excel("./data2526/player_data_shots.xlsx")
# dfPlayerData.sort_values(by = ["CA Threat"], ascending=False).head(10).to_excel("./data2526/player_data_threat.xlsx")

# ###################################################
#
#                Plot Shots vs CA Shots
#
# ###################################################

"""
fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')

x = dfTeamData["CA Vuln"]
y = dfTeamData["CA Pro"]
points = ax.scatter(x, y, s=150)

# ax.invert_xaxis()
ax.set_xlabel("Rentan serangan balik", size='14', labelpad=12)
ax.set_ylabel("Jago serangan balik", size='14', labelpad=12)

ax.plot([x.mean(),x.mean()],[y.max(),y.min()], color="black", linestyle = ":", lw=1)
ax.plot([x.min(),x.max()],[y.mean(),y.mean()], color="black", linestyle = ":", lw=1)

label = dfTeamData.index
bbox = dict(boxstyle="round", fc="0.8")

angleA = 0
angleB = 90

for i, txt in enumerate(label):
    xpos = x.iloc[i]
    ypos = y.iloc[i]

    offsetx = 0
    offsety = 10

    if txt == "Semen Padang FC" or txt == "PSIM Yogyakarta":
        offsetx = 60
        offsety = -5
    elif txt == "Bhayangkara Presisi Lampung FC":
        offsetx += 10
        offsety = 20
    elif txt == "Borneo FC Samarinda":
        offsetx = 40
        offsety = 30
    elif txt == "Arema FC":
        offsetx = -45
        offsety = -30
    elif txt == "PERSIB" or txt == "PSM Makassar":
        offsety = -25

    ax.annotate(
        txt,
        xy=(xpos, ypos),
        xytext=(offsetx, offsety),
        color = 'black',
        ha='center',
        va='bottom',
        textcoords="offset points",
        bbox=bbox,
        arrowprops=dict(
            arrowstyle="-",
            connectionstyle=f"angle,angleA={angleA},angleB={angleB},rad=0"
        )
    )
    angleA = 0
    angleB = 90

title = ax.set_title("Perbandingan Ancaman vs Kerentanan Serangan Balik")
title.set(fontsize='xx-large', fontweight='bold')
plt.show()
"""
