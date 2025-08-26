import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# waktu efektif

df = pd.read_csv("./data2526/waktu_efektif.csv")
df["Total Match"] = pd.to_timedelta(df["Total Match"]).dt.seconds
df["Time Home"] = pd.to_timedelta(df["Time Home"]).dt.seconds
df["Time Away"] = pd.to_timedelta(df["Time Away"]).dt.seconds

dfHome = df[["GW", "Tim Home"]].rename(columns={"GW": "Count"}).groupby(["Tim Home"]).count()
dfAway = df[["GW", "Tim Away"]].rename(columns={"GW": "Count"}).groupby(["Tim Away"]).count()
teamCount = dfHome["Count"] + dfAway["Count"]

totalTimeHome = df[["Tim Home", "Total Match"]].rename(columns={"Tim Home": "Team"}).groupby(["Team"]).sum()
totalTimeAway = df[["Tim Away", "Total Match"]].rename(columns={"Tim Away": "Team"}).groupby(["Team"]).sum()

timeHome = df[["Tim Home", "Time Home"]].rename(columns={"Tim Home": "Team"}).groupby(["Team"]).sum()
timeAway = df[["Tim Away", "Time Away"]].rename(columns={"Tim Away": "Team"}).groupby(["Team"]).sum()
teamTime = timeHome["Time Home"] + timeAway["Time Away"]

def formatTime(secs: int):
    hours, remainder = divmod(secs, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    if seconds < 10:
        return f'0{int(hours)}:{int(minutes)}:0{int(seconds)}'
    else:
        return f'0{int(hours)}:{int(minutes)}:{int(seconds)}'

dfTime = totalTimeHome + totalTimeAway
dfTime = dfTime.rename(columns={"Total Match": "Match Time (raw)"})
dfTime["Avg Match Time (raw)"] = dfTime["Match Time (raw)"] / teamCount
dfTime["Own Time (raw)"] = teamTime / teamCount
dfTime["Opp Time (raw)"] = dfTime["Avg Match Time (raw)"] - dfTime["Own Time (raw)"]

dfPrint = pd.DataFrame(dfTime["Avg Match Time (raw)"].apply(lambda x: formatTime(x))).rename(columns={"Avg Match Time (raw)":"Avg Match Time"})
dfPrint["Own Time"] = dfTime["Own Time (raw)"].apply(lambda x: formatTime(x))
dfPrint["Opp Time"] = dfTime["Opp Time (raw)"].apply(lambda x: formatTime(x))

# def actions

dfDefActions = pd.read_csv("./data2526/da.csv")
dfDefActions = dfDefActions[["Team", "Tackle", "Intercept", "Clearance", "Recovery", "Foul"]].groupby(["Team"]).sum()
dfDefActions["Def Actions"] = dfDefActions.eval("Tackle + Intercept + Clearance + Recovery")
dfDefActions = dfDefActions[["Def Actions", "Foul"]]

dfTeam = pd.read_csv("./data2526/bp.csv")
dfTeam = dfTeam.set_index("Team")
dfTeam["Ball Possession"] = dfTeam["Ball Possession"].apply(lambda x: round(x, 2))
dfTeam["Def Actions"] = dfDefActions["Def Actions"]
dfTeam["Foul"] = dfDefActions["Foul"]

dfTeam["PAdj Def Actions"] = dfTeam["Def Actions"] * 50 / (100 - dfTeam["Ball Possession"])
dfTeam["PAdj Def Actions"] = dfTeam["PAdj Def Actions"].apply(lambda x: round(x))
dfTeam["Foul/min"] = dfTeam["Foul"] / dfTime["Avg Match Time (raw)"] * 60
dfTeam["Foul/min"] = dfTeam["Foul/min"].apply(lambda x: round(x, 2))
dfTeam["Foul/Opp Effective Time"] = dfTeam["Foul"] / dfTime["Opp Time (raw)"] * 60
dfTeam["Foul/Opp Effective Time"] = dfTeam["Foul/Opp Effective Time"].apply(lambda x: round(x, 2))
dfTeam["Avg Time"] = dfPrint["Avg Match Time"]

dfTeam = dfTeam.sort_values(["Foul/min"], ascending=False)
dfTeam["Color"] = "#04519f"

xValue = "PAdj Def Actions"
yValue = "Foul/Opp Effective Time"

x = dfTeam[xValue]
y = dfTeam[yValue]
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

mostFoul = dfTeam["Foul"].idxmax()
minFoul = dfTeam["Foul"].idxmin()

for name, limit, y in zip(dfTeam.index, p(x), y):
    if name == mostFoul:
        dfTeam.loc[dfTeam.index == name, "Color"] = "red"
    elif name == minFoul:
        dfTeam.loc[dfTeam.index == name, "Color"] = "green"
    elif y >= limit:
        dfTeam.loc[dfTeam.index == name, "Color"] = "orange"

fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')

x1 = dfTeam[xValue]
y1 = dfTeam[yValue]
cmap = dfTeam["Color"]

points1 = ax.scatter(x1, y1, c=cmap, s=150)

#add trendline to plot
ax.plot(x, p(x), color="black", linestyle="solid", linewidth=2)

bbox = dict(boxstyle="round", fc="0.8")

maxFouls = dfTeam["Foul"].loc[mostFoul]
avgTimeOfMaxFouls = dfTeam["Avg Time"].loc[mostFoul]
ax.annotate(
    f"fouls: {maxFouls}\naverage effective time: {avgTimeOfMaxFouls}",
    (x1.loc[mostFoul], y1.loc[mostFoul]),
    xytext=(10, -5),
    color = 'black',
    ha='left',
    va='bottom',
    size=10,
    textcoords="offset points",
    # bbox=bbox,
    arrowprops=dict(
        arrowstyle="-",
        connectionstyle=f"angle,angleA=0,angleB=90,rad=0"
    )
)

minFouls = dfTeam["Foul"].loc[minFoul]
avgTimeOfMinFouls = dfTeam["Avg Time"].loc[minFoul]
ax.annotate(
    f"fouls: {minFouls}\naverage effective time: {avgTimeOfMinFouls}",
    (x1.loc[minFoul], y1.loc[minFoul]),
    xytext=(10, -20),
    color = 'black',
    ha='left',
    va='bottom',
    size=10,
    textcoords="offset points",
    # bbox=bbox,
    arrowprops=dict(
        arrowstyle="-",
        connectionstyle=f"angle,angleA=0,angleB=90,rad=0"
    )
)

for i, txt in enumerate(dfTeam.index):
    offsetx = 0
    offsety = 10
    angleA = 90
    angleB = 0
    if txt == "Bali United FC" or txt == "PSIM Yogyakarta" or txt == "PERSIB":
        offsety = -20
    # elif txt == "Bhayangkara Presisi Lampung FC":
    #     offsetx = 75
    #     offsety = 10
    # elif txt == "Borneo FC Samarinda":
    #     offsety = -20
    elif txt == "PERSEBAYA Surabaya":
        offsetx = 75
        offsety = -5
        angleA = 0
        angleB = 90
    elif txt == "Arema FC":
        offsety = -20
    elif txt == "Dewa United Banten FC":
        offsety = -20

        # offsetx = -80
        # offsety = -5
        # angleA = 0
        # angleB = 90

        # offsety = 30
    elif txt == "Madura United FC":
        offsety = -20
        # offsety = 20

    ax.annotate(
        txt,
        (x1.iloc[i], y1.iloc[i]),
        xytext=(offsetx, offsety),
        color = 'black',
        ha='center',
        va='bottom',
        size=10,
        textcoords="offset points",
        bbox=bbox,
        arrowprops=dict(
            arrowstyle="-",
            connectionstyle=f"angle,angleA={angleA},angleB={angleB},rad=0"
        )
    )

title = ax.set_title("Kecenderungan Melakukan Pelanggaran Masing-masing Tim")
title.set(fontsize='xx-large', fontweight='bold')
ax.set_xlabel(xValue, size='11', labelpad=12)
ax.set_ylabel(yValue, size='11', labelpad=12)

plt.show()
