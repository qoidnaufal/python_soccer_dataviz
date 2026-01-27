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

PENALTY_BOX_DEPTH = 16.5
PENALTY_BOX_WIDTH = 40.3

PENALTY_BOX_X = PITCH_X - PENALTY_BOX_DEPTH
PENALTY_BOX_Y_MAX = PITCH_Y/2 + PENALTY_BOX_WIDTH/2
PENALTY_BOX_Y_MIN = PITCH_Y/2 - PENALTY_BOX_WIDTH/2

colors = ["#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#d5c4a1","#d65d0e","#665c54"]
gruvbox = ListedColormap(colors)

def font(size: int):
    return {'family': 'serif',
            'weight': 'normal',
            'size': size,
            }

def passOutput(input):
    if input == "passing":
        return PASS_SUCCESS
    else:
        return PASS_FAILED

def length(frame: pd.DataFrame):
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
    return (x & bot) or (x & top)

df = pd.read_excel("./data2526/half_season/half_season.xlsx")
df = df.rename(columns={"Act Name": "Player"})

for idx, game in enumerate(df["Match"]):
    teams = game.split("vs")
    home, away = [x.strip() for x in teams]

    opponent = away if df.at[idx, "Team"] == home else home

    df.at[idx, "Opponent"] = opponent

teams = df["Team"].unique()
opponents = df["Opponent"].unique()
week = df["Gameweek"].max()

def processPassData(f: pd.DataFrame, cols):
    passes = f.loc[f["Action"].str.contains("pass")][cols].copy()
    passes = passes.dropna()

    passes["Action"] = passes["Action"].apply(lambda x: passOutput(x))
    passes["X1"] = passes["X1"].apply(lambda x: x * PITCH_X/100)
    passes["X2"] = passes["X2"].apply(lambda x: x * PITCH_X/100)
    passes["Y1"] = passes["Y1"].apply(lambda y: PITCH_Y - (y * PITCH_Y/100))
    passes["Y2"] = passes["Y2"].apply(lambda y: PITCH_Y - (y * PITCH_Y/100))

    passes = passes.loc[passes.apply(lambda row: isCorner(row["X1"], row["Y1"]) == False, axis=1)]
    passes = passes.reset_index(drop=True)

    passes["angle"] = np.arctan2(passes["Y2"] - passes["Y1"], passes["X2"] - passes["X1"]) * 180/np.pi
    passes["length"] = length(passes).apply(lambda d: math.sqrt(d))
    passes["prog"] = passes.apply(lambda row : prog(row["X1"], row["Y1"], row["X2"], row["Y2"]), axis = 1)
    passes["prog_distance"] = passes.apply(lambda row : distanceProgressed(row["X1"], row["Y1"], row["X2"], row["Y2"]), axis = 1)
    passes["prog_percent"] = passes.apply(lambda row : percentProgressed(row["X1"], row["Y1"], row["X2"], row["Y2"]), axis = 1)

    xT = pd.read_csv('/Users/qoidnaufal/Documents/LearnPython/xT_DS.csv',header=None)
    xT = np.array(xT)
    xT_rows, xT_cols = xT.shape

    x1_bin = pd.cut(passes['X1'], bins = xT_cols, labels = False)
    y1_bin = pd.cut(passes['Y1'], bins = xT_rows, labels = False)
    x2_bin = pd.cut(passes['X2'], bins = xT_cols, labels = False)
    y2_bin = pd.cut(passes['Y2'], bins = xT_rows, labels = False)

    v1 = xT[y1_bin, x1_bin]
    v2 = xT[y2_bin, x2_bin]
    passes['xT'] = np.subtract(v2, v1)

    return passes

def plotHist(data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
    fwd = data.loc[passes["prog_percent"] >= 0]["prog_percent"]
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

def elbowMethod(data: pd.DataFrame):
    filter = ["X1", "Y1", "xT"]
    median = np.median(data.loc[data["prog_percent"] >= 0]["prog_percent"])
    d = data.loc[data["prog_percent"] > median]
    d = d.loc[d["Action"] == PASS_SUCCESS].copy()

    K = np.linspace(1, 20, 20)
    X = d[filter].values
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

def cluster(data: np.ndarray, k: int):
    cluster = KMeans(n_clusters=k, random_state=69)
    labels = cluster.fit_predict(data)
    centroids = cluster.cluster_centers_
    return labels, centroids

def plotDistributed(passes: pd.DataFrame, k):
    data = passes.loc[(passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)].copy()
    param = ["X1", "Y1", "angle"]

    labels, centroids = cluster(data[param].to_numpy(), k)
    data["label"] = labels
    closest = findClosest(centroids, X, 4)

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(
                    ncols = n_col,
                    nrows = 1 if k <= 4 else int(k / 4),
                    grid_height = 0.85,
                    title_height = 0.06,
                    axis = False,
                    endnote_height = 0.04,
                    title_space = 0.04,
                    endnote_space = 0.01
                )

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=n_col, nrows=n_row, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    for i, (clust, ax) in enumerate(zip(np.linspace(0, k-1, k), axs['pitch'].flat[:k])):
        clustered = data.loc[data["label"] == clust]
        clust_xT = clustered["xT"]
        n = "{0:,.2f}".format(np.mean(clust_xT) * 100)

        ax.text(52.5, 74, f"xT per 100 passes: {n}",
                ha='center', va='center', fontsize=10)
    
        pitch.scatter(clustered.X1, clustered.Y1, alpha=0.1, s=10, c=colors[i % len(colors)], ax=ax)

        for nodes in closest[i]:
            x1 = nodes[0]
            y1 = nodes[1]
            angle = nodes[2]

            dst = clustered.loc[
                (clustered["X1"] == x1)
                    & (clustered["Y1"] == y1)
                    & (clustered["angle"] == angle)
            ]

            x2 = dst.X2
            y2 = dst.Y2

            pitch.arrows(x1, y1, x2, y2, width=1, alpha=0.7, ax=ax)

    axs['title'].text(
        0.5, 0.2,
        f'{k} Cluster Sumber Passing Progresif\nBRI Super League 2025/26 hingga pekan ke-{week}',
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotPerTeam(passes: pd.DataFrame, attackings: pd.Series, k):
    params = ["X1", "Y1", "angle"]
    data = passes.loc[(passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    for i, (team, ax) in enumerate(zip(attackings, axs['pitch'].flat[:18])):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Team"] == team].copy()
        labels, _ = cluster(team_data[params].to_numpy(), k)
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
            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.5,
            )

    axs['title'].text(
        0.5, 0.3,
        "2 Tipe Passing Progressive yang Paling Sering Dilakukan Masing-masing Tim",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotFacedThreat(passes: pd.DataFrame, defendings: pd.Series, k):
    params = ["X1", "Y1", "angle"]
    data = passes.loc[(passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)
    
    for i, (team, ax) in enumerate(zip(defendings, axs['pitch'].flat[:18])):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Opponent"] == team].copy()
        labels, _ = cluster(team_data[params].to_numpy(), k)
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
            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.5,
            )

    axs['title'].text(
        0.5, 0.3,
        "2 Passing Progressive yang Sering Dihadapi Masing-masing Tim",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotFinalThirdEntry(passes: pd.DataFrame, defendings: pd.Series, k: int):
    params = ["X1", "Y1", "angle"]
    data = passes.loc[
        (passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)
            & ((passes["X2"] < PENALTY_BOX_X)
                | (
                    (passes["Y2"] < PENALTY_BOX_Y_MIN)
                    | (passes["Y2"] > PENALTY_BOX_Y_MAX)
                ))
    ]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    for i, (team, ax) in enumerate(zip(defendings, axs["pitch"].flat[:18])):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Opponent"] == team].copy()
        labels, _ = cluster(team_data[params].to_numpy(), k)
        team_data["group"] = labels

        entry = team_data.loc[
            (team_data["X1"] < 2 * PITCH_X/3)
                & (team_data["X2"] >= 2 * PITCH_X/3)
        ]

        def max_2(f: pd.DataFrame):
            count = f["group"].value_counts()
            count = count.sort_values(ascending=False)
            return count.head(2)

        for j, clust in enumerate(max_2(entry).index):
            clustered = entry.loc[entry["group"] == clust]

            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.5,
            )

    axs['title'].text(
        0.5, 0.3,
        "2 Passing Progressive ke Sepertiga Akhir yang Sering Dihadapi Masing-masing Tim",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotPenaltyBoxEntry(passes: pd.DataFrame, defendings: pd.Series, k: int):
    params = ["X1", "Y1", "angle"]
    data = passes.loc[
        (passes["Action"] == PASS_SUCCESS)
            & (passes["X1"] < PITCH_X)
            & (passes["X2"] >= PENALTY_BOX_X)
            & (passes["Y2"] >= PENALTY_BOX_Y_MIN)
            & (passes["Y2"] <= PENALTY_BOX_Y_MAX)
    ]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    for i, (team, ax) in enumerate(zip(defendings, axs["pitch"].flat[:18])):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Opponent"] == team].copy()
        labels, _ = cluster(team_data[params].to_numpy(), k)
        team_data["group"] = labels

        entry = team_data.loc[
            (team_data["X1"] < PENALTY_BOX_X)
                | (
                    (team_data["Y1"] < PENALTY_BOX_Y_MIN)
                    | (team_data["Y1"] > PENALTY_BOX_Y_MAX)
                )
        ]

        def max_2(f: pd.DataFrame):
            count = f["group"].value_counts()
            count = count.sort_values(ascending=False)
            return count.head(2)

        for j, clust in enumerate(max_2(entry).index):
            clustered = entry.loc[entry["group"] == clust]

            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.5,
            )

    axs['title'].text(
        0.5, 0.3,
        "2 Passing ke Kotak Penalti yang Sering Dihadapi Masing-masing Tim",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotOnce(passes: pd.DataFrame, k):
    data = passes.loc[(passes["prog"] == True) & (passes["Action"] == PASS_SUCCESS)].copy()
    param = ["X1", "Y1", "angle"]

    labels, _ = cluster(data[params].to_numpy(), k)
    data["label"] = labels

    pitch = Pitch(line_color='black', pitch_type = "custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, ax = pitch.draw(figsize=(8, 9))
    pitch.scatter(data.X1, data.Y1, alpha=0.4, s=50, c=labels, cmap=gruvbox, ax=ax)

    clusters = np.linspace(0, k-1, k)

    for clust in clusters:
        cluster_data = data.loc[data["label"] == clust]

        x1 = np.mean(cluster_data.X1)
        y1 = np.mean(cluster_data.Y1)
        x2 = np.mean(cluster_data.X2)
        y2 = np.mean(cluster_data.Y2)

        avg_xT = "{0:,.2f}".format(np.mean(cluster_data.xT) * 100)

        pitch.arrows(x1, y1, x2, y2, width=2, ax=ax)

        def xy_loc(y1, y2):
            if y1 > y2:
                return (0, 5)
            elif y2 > y1:
                return (0, -5)
            else:
                return (-20, 0)

        ax.annotate(
            f"{avg_xT} xT",
            (x1, y1),
            xytext=xy_loc(y1, y2),
            ha='center',
            va='center',
            textcoords="offset points",
            size=8
        )

    title = plt.title(f"{k} Progressive Pass Clusters in BRI Super League 2025/26", fontdict=font(15))

    plt.show()

def mapTopPlayer(src: pd.DataFrame, players: pd.DataFrame, head, k, category):
    param = ["X1", "Y1", "angle"]
    data = src.loc[(src["prog"] == True) & (src["Action"] == PASS_SUCCESS)]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(
                    ncols = 5,
                    nrows = 1 if head <= 5 else int(head / 5),
                    grid_height = 0.85,
                    title_height = 0.06,
                    axis = False,
                    endnote_height = 0.04,
                    title_space = 0.04,
                    endnote_space = 0.01
                )

    player_data = players.head(head).copy()
    names = player_data.Player

    for i, (player, ax) in enumerate(zip(names, axs['pitch'].flat[:head])):
        ax.text(52.5, 74, f"{player}", ha='center', va='center', fontsize=10)

        pd = data.loc[data["Player"] == player].copy()
        X = pd[param].values
        cluster = KMeans(n_clusters=int(k), random_state=69)
        labels = cluster.fit_predict(X)
        pd["label"] = labels

        def max_2():
            count = pd['label'].value_counts()
            count = count.sort_values(ascending=False)
            return count.head(2)

        max_2 = max_2()

        for j, clust in enumerate(max_2.index):
            clustered = pd.loc[pd['label'] == clust]
            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.8,
            )

    map = {
        "TotalProgressivePasses": "Jumlah Percobaan Passing Progresif",
        "ProgressivePassSuccess": "Jumlah Passing Progresif Sukses",
        "clean_xT": "Total xT",
        "prog_xT": "xT dari Passing Progresif",
        "xT per 100": "xT Tiap 100 Passing",
    }

    cat = map[category]

    axs['title'].text(
        0.5, 0.15,
        f"2 Passing Progressive Andalan dari Top {head} Pemain\nBerdasarkan {cat}",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def mapTopPlayerPerTeam(src: pd.DataFrame, players, k, category):
    param = ["X1", "Y1", "angle"]
    data = src.loc[(src["prog"] == True) & (src["Action"] == PASS_SUCCESS)]

    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(
                    ncols = 6,
                    nrows = 3,
                    grid_height = 0.85,
                    title_height = 0.06,
                    axis = False,
                    endnote_height = 0.04,
                    title_space = 0.04,
                    endnote_space = 0.01
                )

    for i, (player, ax) in enumerate(zip(players, axs['pitch'].flat[:18])):
        pd = data.loc[data["Player"] == player].copy()

        p_team = pd.Team.iloc[0]
        ax.text(52.5, 79, f"[{p_team}]\n{player}", ha='center', va='center', fontsize=10)

        X = pd[param].values
        cluster = KMeans(n_clusters=int(k), random_state=69)
        labels = cluster.fit_predict(X)
        pd["label"] = labels

        def max_2():
            count = pd['label'].value_counts()
            count = count.sort_values(ascending=False)
            return count.head(2)

        max_2 = max_2()

        for j, clust in enumerate(max_2.index):
            clustered = pd.loc[pd['label'] == clust]
            pitch.arrows(
                clustered.X1, clustered.Y1,
                clustered.X2, clustered.Y2,
                color=colors[(i + j) % len(colors)],
                ax=ax,
                alpha=0.5,
                width=0.8,
            )

    map = {
        "TotalProgressivePasses": "Jumlah Percobaan Passing Progresif",
        "ProgressivePassSuccess": "Jumlah Passing Progresif Sukses",
        "clean_xT": "Total xT",
        "prog_xT": "xT dari Passing Progresif",
        "xT per 100": "xT Tiap 100 Passing",
        "TotalPasses": "Jumlah Passing",
    }

    cat = map[category]

    axs['title'].text(
        0.5, 0.15,
        f"2 Passing Progressive Andalan dari Pemain Tertinggi Masing-masing Tim\nBerdasarkan {cat}",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def playerData(passes: pd.DataFrame):
    players = passes["Player"].unique()
    player_passes = {
        "Player": [],
        "Team": [],
        "TotalPasses": [],
        "PassSuccess": [],
        "TotalProgressivePasses": [],
        "ProgressivePassSuccess": [],
        "gross_xT": [],
        "clean_xT": [],
        "prog_xT": [],
    }
    for player in players:
        pp = passes.loc[passes["Player"] == player]
        ps = pp.loc[pp["Action"] == PASS_SUCCESS]
        pr = pp.loc[pp["prog"] == True]
        cp = pp.loc[(pp["prog"] == True) & (pp["Action"] == PASS_SUCCESS)]

        gross_xT = np.sum(pp.xT)
        clean_xT = np.sum(ps.xT)
        prog_xT = np.sum(cp.xT)

        player_passes["Player"].append(player)
        player_passes["Team"].append(pp.Team.iloc[0])
        player_passes["TotalPasses"].append(len(pp))
        player_passes["PassSuccess"].append(len(ps))
        player_passes["TotalProgressivePasses"].append(len(pr))
        player_passes["ProgressivePassSuccess"].append(len(cp))
        player_passes["gross_xT"].append(gross_xT)
        player_passes["clean_xT"].append(clean_xT)
        player_passes["prog_xT"].append(prog_xT)

    player_passes = pd.DataFrame(player_passes)
    player_passes["xT per 100"] = (player_passes.clean_xT / player_passes.TotalPasses) * 100
    # player_passes["xT per 100 progression"] = (player_passes.prog_xT / player_passes.TotalProgressivePasses) * 100

    return player_passes

def plotPlayerMap(passes: pd.DataFrame, category):
    player_data = playerData(passes)
    sorted = player_data.sort_values(by=category, ascending=False)
    mapTopPlayer(passes, sorted, 10, 5, category)

def topPlayerPerTeamByCategory(passes: pd.DataFrame, category):
    player_data = playerData(passes)

    top_players = []

    for team in teams:
        team_data = player_data.loc[player_data["Team"] == team]
        max_val = np.max(team_data[category])
        top = team_data.loc[team_data[category] == max_val]

        top_players.append(top.Player.iloc[0])

    return top_players

def plotTopPlayerPerTeam(passes: pd.DataFrame, category):
    player_data = playerData(passes)
    top_players = topPlayerPerTeamByCategory(passes, category)
    mapTopPlayerPerTeam(passes, top_players, 5, category)

def mapEachCategory(passes: pd.DataFrame):
    data = pd.DataFrame({
        "Team": teams,
        "Total Passes": topPlayerPerTeamByCategory(passes, "TotalPasses"),
        "Total Progressive Passes": topPlayerPerTeamByCategory(passes, "TotalProgressivePasses"),
        "Progressive Pass Success": topPlayerPerTeamByCategory(passes, "ProgressivePassSuccess"),
        "gross_xT (risk taker)": topPlayerPerTeamByCategory(passes, "gross_xT"),
        "clean_xT (top creator)": topPlayerPerTeamByCategory(passes, "clean_xT"),
    })

    data.to_csv('./data2526/half_season/roles.csv', index=False)

# mapEachCategory(processPassData(df, ["Action", "Player", "Team", "X1", "Y1", "X2", "Y2"]))
# plotPlayerMap(processPassData(df, ["Action", "Player", "Team", "X1", "Y1", "X2", "Y2"]), "ProgressivePassSuccess")
# plotTopPlayerPerTeam(processPassData(df, ["Action", "Player", "Team", "X1", "Y1", "X2", "Y2"]), "clean_xT")
# plotHist(processPassData(df, ["Team", "Opponent", "Action", "X1", "Y1", "X2", "Y2"]))
# elbowMethod(processPassData(df, ["Team", "Opponent", "Action", "X1", "Y1", "X2", "Y2"]))
# plotDistributed(processPassData(df, ["Team", "Opponent", "Action", "X1", "Y1", "X2", "Y2"]), 11)
# plotOnce(processPassData(df, ["Action", "X1", "Y1", "X2", "Y2"]), 11)
# plotPerTeam(processPassData(df, ["Team", "Opponent", "Action", "X1", "Y1", "X2", "Y2"]), teams, 11)
# plotFacedThreat(processPassData(df, ["Opponent", "Action", "X1", "Y1", "X2", "Y2"]), opponents, 11)
# plotFinalThirdEntry(processPassData(df, ["Opponent", "Action", "X1", "Y1", "X2", "Y2"]), opponents, 11)
plotPenaltyBoxEntry(processPassData(df, ["Opponent", "Action", "X1", "Y1", "X2", "Y2"]), opponents, 7)
