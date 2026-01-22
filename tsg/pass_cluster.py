import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.cluster import KMeans
from mplsoccer import Pitch
from numpy import linalg as la
from matplotlib.colors import ListedColormap
from sklearn.metrics import pairwise_distances

PASS_FAILED = 0
PASS_SUCCESS = 1

PITCH_X = 105
PITCH_Y = 68

colors = ["#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#d5c4a1","#d65d0e","#665c54"]
gruvbox = ListedColormap(colors)

def passOutput(input):
    if input == "passing":
        return PASS_SUCCESS
    else:
        return PASS_FAILED

def length(frame):
    dx = frame["X2"] - frame["X1"]
    dy = frame["Y2"] - frame["Y1"]
    return dx.apply(lambda x: x**2) + dy.apply(lambda y: y**2)

def startEnd(x1, y1, x2, y2):
    dx1 = (PITCH_X - x1)**2
    dx2 = (PITCH_X - x2)**2
    dy1 = (y1 - PITCH_Y / 2)**2
    dy2 = (y2 - PITCH_Y / 2)**2

    start = np.sqrt(dx1 + dy1)
    end = np.sqrt(dx2 + dy2)

    return start, end
    
def distanceProgressed(x1, y1, x2, y2):
    start, end = startEnd(x1, y1, x2, y2)
    return start - end

def percentProgressed(x1, y1, x2, y2):
    start, end = startEnd(x1, y1, x2, y2)
    dist = start - end
    return dist * 100 / start

def prog(x1, y1, x2, y2):
    start, end = startEnd(x1, y1, x2, y2)
    threshold = 100

    if x1 < 52.5 and x2 < 52.5:
        threshold = 30
    elif x1 < 52.5 and x2 >= 52.5:
        threshold = 15
    elif x1 >= 52.5 and x2 >= 52.5:
        threshold = 10

    if threshold > start - end:
        return False
    else:
        return True

def isCorner(x1, y1):
    x = x1 == PITCH_X
    bot = y1 == PITCH_Y
    top = y1 == 0

    return (x & bot) | (x & top)

xT = pd.read_csv('/Users/qoidnaufal/Documents/LearnPython/xT_DS.csv',header=None)
xT = np.array(xT)
xT_rows, xT_cols = xT.shape

df = pd.read_excel("./data2526/half_season/half_season.xlsx")

for idx, game in enumerate(df["Match"]):
    teams = game.split("vs")
    teams = [x.strip() for x in teams]

    opponent = ""

    if df.at[idx, "Team"] == teams[0]:
        opponent = teams[1]
    else:
        opponent = teams[0]

    df.at[idx, "Opponent"] = opponent

teams = df["Team"].unique()
opponents = df["Opponent"].unique()

# team_ids = {}

# for id, team in enumerate(teams):
#     team_ids[team] = id

# df["TeamId"] = df["Team"].map(team_ids)
week = df["Gameweek"].max()

passes = df.loc[df["Action"].str.contains("pass")][["Team", "Opponent", "Action", "X1", "Y1", "X2", "Y2"]].copy()
passes = passes.dropna()

passes["Action"] = passes["Action"].apply(lambda x: passOutput(x))
passes["X1"] = passes["X1"].apply(lambda x: x * PITCH_X/100)
passes["X2"] = passes["X2"].apply(lambda x: x * PITCH_X/100)
passes["Y1"] = passes["Y1"].apply(lambda y: y * PITCH_Y/100)
passes["Y2"] = passes["Y2"].apply(lambda y: y * PITCH_Y/100)

passes = passes.loc[passes.apply(lambda row: isCorner(row["X1"], row["Y1"]) == False, axis=1)]
passes = passes.reset_index(drop=True)

passes["angle"] = np.arctan2(passes["Y2"] - passes["Y1"], passes["X2"] - passes["X1"]) * 180/np.pi
passes["length"] = length(passes).apply(lambda d: math.sqrt(d))
passes["prog"] = passes.apply(lambda row : prog(row["X1"], row["Y1"], row["X2"], row["Y2"]), axis = 1)
passes["prog_distance"] = passes.apply(lambda row : distanceProgressed(row["X1"], row["Y1"], row["X2"], row["Y2"]), axis = 1)
passes["prog_percent"] = passes.apply(lambda row : percentProgressed(row["X1"], row["Y1"], row["X2"], row["Y2"]), axis = 1)

x1_bin = pd.cut(passes['X1'], bins = xT_cols, labels = False)
y1_bin = pd.cut(passes['Y1'], bins = xT_rows, labels = False)
x2_bin = pd.cut(passes['X2'], bins = xT_cols, labels = False)
y2_bin = pd.cut(passes['Y2'], bins = xT_rows, labels = False)

v1 = xT[y1_bin, x1_bin]
v2 = xT[y2_bin, x2_bin]
passes['xT'] = np.subtract(v2, v1)

# print(passes.head(30))
def font(size: int):
    return {'family': 'serif',
            'weight': 'normal',
            'size': size,
            }

def plotHist():
    fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
    # data = passes['prog_percent'].apply(lambda x: modifyPct(x))
    fwd = passes.loc[passes["prog_percent"] >= 0]["prog_percent"]
    median = np.median(fwd) # 20%

    style = {'edgecolor': '#282828', 'linewidth': 2}
    n, a, b = ax.hist(fwd, bins=10, **style)
    max = np.max(n)
    print(min, max)
    ax.plot([median,median],[0,max], "#d65d0e", linestyle = "--", lw=2)
    ax.annotate(
        f"median:\n{np.round(median)}%",
        (median, max),
        color = 'black',
        ha='left',
        va='center',
        size=10,
        )
    plt.title(f"Histogram Persentase Jarak Progresi melalui Passing ke Depan\nBRI Super League 2025/26 hingga pekan ke-{week}", fontdict=font(15))
    plt.xlabel("Persentase Jarak Progresi")
    plt.ylabel("Frekuensi")
    plt.show()

def elbowMethod():
    filter = ["X1", "Y1", "xT"]
    median = np.median(passes.loc[passes["prog_percent"] >= 0]["prog_percent"])
    data = passes.loc[passes["prog_percent"] > median]
    data = data.loc[data["Action"] == PASS_SUCCESS].copy()

    K = np.linspace(1, 20, 20)
    X = data[filter].values
    elbow = {"sse": [], "k": []}
    for k in K:
        cluster = KMeans(n_clusters = int(k), random_state = 69)
        labels = cluster.fit_predict(X)
        elbow["sse"].append(cluster.inertia_)
        elbow["k"].append(k)

    fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')

    ax.scatter(elbow["k"], elbow["sse"])
    ax.plot(elbow["k"], elbow["sse"])
    ax.scatter([5,11],[elbow["sse"][4],elbow["sse"][10]], c="#d65d0e")

    plt.xticks(np.linspace(1, 20, 20))
    plt.xlabel("K")
    plt.ylabel("SSE")
    plt.title("Elbow Method", fontdict=font(20))

    plt.show()

def findClosest(centroids, data, count: int):
    distances = pairwise_distances(centroids, data, metric='euclidean')
    indices = [np.argpartition(i, count)[:count] for i in distances]
    closest = [data[idx] for idx in indices]
    return closest

def unpack(frame, c):
    # cond1 = frame[filter[0]] == c[0]
    # cond2 = frame[filter[1]] == c[1]
    cond3 = frame[filter[2]] == c[2]
    return frame.loc[cond3]
    # max = np.max(frame[filter[2]])
    # return frame.loc[frame[filter[2]] == max]

def plotDistributed(k, n_col, n_row):
    filter = ["X1", "Y1", "xT"]
    median = np.median(passes.loc[passes["prog_percent"] >= 0]["prog_percent"])
    data = passes.loc[passes["prog_percent"] > median]
    data = data.loc[data["Action"] == PASS_SUCCESS].copy()

    X = data[filter].values
    cluster = KMeans(n_clusters=int(k), random_state=69)
    labels = cluster.fit_predict(X)
    centroids = cluster.cluster_centers_
    data["label"] = labels

    closest = findClosest(centroids, X, 2)

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=n_col, nrows=n_row, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    for i, (clust, ax) in enumerate(zip(np.linspace(0, k-1, k), axs['pitch'].flat[:k])):
        clustered = data.loc[data["label"] == clust]
        param = clustered["xT"]
        n = "{0:,.2f}".format(np.mean(param) * 100)

        ax.text(52.5, 74, f"xT per 100 pass: {n}",
                ha='center', va='center', fontsize=10)
        # ax.text(52.5, 74, f"[Cluster {int(clust+1)}] xT per 100 pass: {n}",
        #         ha='center', va='center', fontsize=10)
    
        pitch.scatter(clustered.X1, clustered.Y1, alpha=0.1, s=10, c=colors[i % len(colors)], ax=ax)

        # for c in closest[i]:
        #     row = unpack(clustered, c)[["X1", "Y1", "X2", "Y2"]]
        #     ax.quiver(row.X1, row.Y1, row.X2, row.Y2)

    axs['title'].text(
        0.5, 0.5,
        f'{k} Cluster Sumber Passing Progresif\nBRI Super League 2025/26 hingga pekan ke-{week}',
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotPerTeam(k):
    filter = ["X1", "Y1", "angle"]
    data = passes.loc[(passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)]
    # median = np.median(progs["prog_percent"])
    # data = passes.loc[passes["prog_percent"] > median]
    # data = data.loc[data["Action"] == PASS_SUCCESS]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    for i, (team, ax) in enumerate(zip(teams, axs['pitch'].flat[:18])):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Team"] == team].copy()
        X = team_data[filter].values
        cluster = KMeans(n_clusters=int(k), random_state=69)
        labels = cluster.fit_predict(X)
        team_data["label"] = labels

        def max_2():
            # xt_means = team_data[["label", "xT"]].groupby('label').mean()
            # xt_means = xt_means.sort_values(by="xT", ascending=False)
            # return xt_means.head(2)
            count = team_data['label'].value_counts()
            count = count.sort_values(ascending=False)
            return count.head(2)

        max_2 = max_2()

        for j, clust in enumerate(max_2.index):
            clustered = team_data.loc[team_data['label'] == clust]
            # pitch.scatter(clustered.X1, clustered.Y1, alpha=0.4, s=10, c=colors[(i + j) % len(colors)], ax=ax)
            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.5,
            )

    axs['title'].text(
        0.5, 0.5,
        "Top 2 Most Played Progressive Passes by Super League Teams",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotFacedThreat(k):
    param = ["X1", "Y1", "angle"]
    data = passes.loc[(passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)]
    # median = np.median(progs["prog_percent"])
    # data = progs.loc[(progs["prog_percent"] > median) & (passes["Action"] == PASS_SUCCESS)]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)
    
    for i, (opp, ax) in enumerate(zip(opponents, axs['pitch'].flat[:18])):
        ax.text(52.5, 74, f"{opp}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Opponent"] == opp].copy()
        X = team_data[param].values
        cluster = KMeans(n_clusters=int(k), random_state=69)
        labels = cluster.fit_predict(X)
        team_data["label"] = labels

        def max_2():
            count = team_data['label'].value_counts()
            count = count.sort_values(ascending=False)
            return count.head(2)
            # xt_means = team_data[["label", "xT"]].groupby('label').mean()
            # xt_means = xt_means.sort_values(by="xT", ascending=False)
            # return xt_means.head(2)

        max_2 = max_2()

        for j, clust in enumerate(max_2.index):
            clustered = team_data.loc[team_data['label'] == clust]
            # pitch.scatter(clustered.X1, clustered.Y1, alpha=0.4, s=10, c=colors[(i + j) % len(colors)], ax=ax)
            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.5,
            )

    axs['title'].text(
        0.5, 0.5,
        "2 Most Faced Progressive Passes by Super League Teams",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotOnce(k):
    filter = ["X1", "Y1", "xT"]
    src = KMeans(k)
    src.fit(passes[["X1", "Y1", "xT"]])
    src_centroids = src.cluster_centers_

    dst = KMeans(k)
    dst.fit(passes[["X2", "Y2", "xT"]])
    dst_centroids = dst.cluster_centers_

    pitch = Pitch(line_color='black', pitch_type = "custom", pitch_length=105, pitch_width=68)
    fig, ax = pitch.draw(figsize=(8, 9))
    pitch.scatter(passes.X1, passes.Y1, alpha=0.4, s=50, c=src.labels_, cmap=gruvbox, ax=ax)
    ax.quiver(src_centroids[:,0], src_centroids[:,1], dst_centroids[:,0], dst_centroids[:,1])

    title = plt.title("Progressive Pass Clusters BRI Super League 2025/26", fontdict=font(15))

    plt.show()


# plotHist()
# elbowMethod()
# plotDistributed(11, 4, 3)
# plotOnce(11)
plotPerTeam(11)
# plotFacedThreat(11)
