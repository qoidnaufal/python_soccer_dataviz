import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.cluster import KMeans
from mplsoccer import Pitch
from numpy import linalg as la
from matplotlib.colors import ListedColormap

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
    dy1 = (PITCH_Y / 2 - y1)**2
    dy2 = (PITCH_Y / 2 - y2)**2

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

df = pd.read_excel("../data2526/workshop/data.xlsx")

passes = df.loc[df["Action"].str.contains("pass")][["Action", "X1", "Y1", "X2", "Y2"]].copy()
passes = passes.dropna()

passes["Action"] = passes["Action"].apply(lambda x: passOutput(x))
passes["X1"] = passes["X1"].apply(lambda x: x * PITCH_X/100)
passes["X2"] = passes["X2"].apply(lambda x: x * PITCH_X/100)
passes["Y1"] = passes["Y1"].apply(lambda y: y * PITCH_Y/100)
passes["Y2"] = passes["Y2"].apply(lambda y: y * PITCH_Y/100)

passes = passes.loc[passes.apply(lambda row: isCorner(row["X1"], row["Y1"]) == False, axis=1)]
passes = passes.reset_index(drop=True)

passes["angle"] = abs(np.arctan2(passes["Y2"] - passes["Y1"], passes["X2"] - passes["X1"]) * 180/np.pi)
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
font = {'family': 'serif',
        'weight': 'normal',
        'size': 30,
        }

def plotHist():
    fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
    data = passes.loc[passes["prog_percent"] >= 0]["prog_percent"]
    median = np.median(data) # 20%

    style = {'edgecolor': '#282828', 'linewidth': 2}
    n, a, b = ax.hist(data, bins=10, **style)
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
    plt.title("Histogram of Pass Towards the Goal\nBRI Super League 2025/26", fontdict=font)
    plt.show()

filter = ["X1", "Y1", "xT"]

def elbowMethod():
    median = np.median(passes.loc[passes["prog_percent"] >= 0])
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
    plt.xticks(np.linspace(1, 20, 20))
    plt.xlabel("K")
    plt.ylabel("SSE")
    plt.title("Elbow Method", fontdict=font)
    plt.show()

from sklearn.metrics import pairwise_distances
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
    median = np.median(passes.loc[passes["prog_percent"] >= 0])
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
        str(int(k)) + ' Clusters of Progressive Pass Origin in BRI Super League 2025/26',
        ha='center',
        va='center',
        fontsize=30
    )

    plt.show()

def plotOnce(k):
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

    title = plt.title("Progressive Pass Clusters BRI Super League 2025/26", fontdict=font)

    plt.show()


# plotHist()
# elbowMethod()
plotDistributed(12, 4, 3)
# plotOnce(11)
