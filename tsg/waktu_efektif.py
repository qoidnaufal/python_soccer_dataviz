import pandas as pd

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

print(dfTime)
print(dfPrint)
