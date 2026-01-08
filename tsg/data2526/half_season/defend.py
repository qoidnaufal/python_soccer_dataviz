import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans
from mplsoccer import Pitch
from matplotlib.colors import ListedColormap

colors = ["#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#d5c4a1","#d65d0e","#665c54"]
gruvbox = ListedColormap(colors)

PITCH_X = 105
PITCH_Y = 68

# ['Gameweek', 'Match', 'Act Name', 'Team', 'Min', 'Action', 'X1', 'Y1', 'X2', 'Y2', 'xG', 'MatchId']
# ['pass failed' 'duel won' 'passing' 'tackle' 'duel lost' 'intercept' 'recovery ball' 'block' 'shoot blocked' 'shoot off target' 'tackle failed' 'shoot on target' 'block cross']

attActions = ['pass failed', 'passing', 'shoot blocked', 'shoot off target', 'shoot on target']
defActions = ['duel lost', 'duel won', 'intercept', 'recovery ball', 'block', 'tackle', 'tackle failed', 'block cross']

def formatTime(secs: int):
    hours, remainder = divmod(secs, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    if seconds < 10:
        return f'0{int(hours)}:{int(minutes)}:0{int(seconds)}'
    else:
        return f'0{int(hours)}:{int(minutes)}:{int(seconds)}'

def parseTime(input: str):
    input = input.strip()
    input = input.split(":")
    min = int(input[0]) * 60
    sec = int(input[1])
    return min + sec

df = pd.read_excel("./20260105_updated.xlsx")

games = df["Match"].unique()
match_ids = {}
for id, game in enumerate(games):
    match_ids[game] = id

df["MatchId"] = df["Match"].map(match_ids)
df["Min"] = df["Min"].apply(lambda x: parseTime(x))
df["X1"] = df["X1"].apply(lambda x: x * PITCH_X/100)
df["X2"] = df["X2"].apply(lambda x: x * PITCH_X/100)
df["Y1"] = df["Y1"].apply(lambda y: y * PITCH_Y/100)
df["Y2"] = df["Y2"].apply(lambda y: y * PITCH_Y/100)

df = df.loc[df["X1"].notna() & df["Y1"].notna()]

font = {'family': 'serif', 'weight': 'normal', 'size': 30, }

def plot(frame: df.DataFrame, k: int):
    total_len = len(frame)

    X = frame[["X1", "X1"]].values
    cluster = KMeans(n_clusters=k, random_state=69)
    labels = cluster.fit_predict(X)
    frame["kvalue"] = labels
    # centroids = cluster.cluster_centers_

    pitch = Pitch(line_color='black', pitch_type = "custom", pitch_length=105, pitch_width=68)
    fig, ax = pitch.draw(figsize=(8, 9))
    pitch.scatter(frame.X1, frame.Y1, alpha=0.4, s=50, c=frame.kvalue, cmap=gruvbox, ax=ax)

    for cluster in np.linspace(0, k-1, k):
        clustered = frame.loc[frame["kvalue"] == cluster]
        count = len(clustered)
        pct_val = round((count / total_len) * 100)
        x_mean = clustered['X1'].mean()
        ax.text(x_mean, PITCH_Y/2, f"{pct_val}%",
                ha='center', va='center', fontsize=30)

    title = plt.title("Defensive Height Clusters\nBRI Super League 2025/26", fontdict=font)

    plt.show()


da = df.loc[df["Action"].isin(defActions)]
plot(da, 4)
