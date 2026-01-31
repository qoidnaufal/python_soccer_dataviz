import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans
from mplsoccer import Pitch
from matplotlib.colors import ListedColormap

COLORS = ["#cc241d","#b8bb26","#d79921","#83a598","#b16286","#689d6a","#d5c4a1","#d65d0e","#7c6f64","#98971a","#458588"]
GRUVBOX = ListedColormap(COLORS)

COLORS_V = ["#cc241d","#fe9018","#b8bb26","#458588","#fabd2f"]
GRUVBOX_V = ListedColormap(COLORS_V)

COLORS_H = ["#b8bb26","#458588","#fe9018","#458588","#b8bb26"]
GRUVBOX_H = ListedColormap(COLORS_H)

PITCH_X = 105
PITCH_Y = 68

# ['Gameweek', 'Match', 'Act Name', 'Team', 'Min', 'Action', 'X1', 'Y1', 'X2', 'Y2', 'xG', 'MatchId']
# ['pass failed' 'duel won' 'passing' 'tackle' 'duel lost' 'intercept' 'recovery ball' 'block' 'shoot blocked' 'shoot off target' 'tackle failed' 'shoot on target' 'block cross']

ATT_ACTIONS = ['pass failed', 'passing', 'shoot blocked', 'shoot off target', 'shoot on target']
DEF_ACTIONS = ['duel lost', 'duel won', 'intercept', 'recovery ball', 'block', 'tackle', 'tackle failed', 'block cross']
PASSES = ['pass failed', 'passing']

def font(size: int):
    return {'family': 'serif', 'weight': 'normal', 'size': size }

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

def setMatchId(df: pd.DataFrame):
    games = df["Match"].unique()
    match_ids = {}
    for id, game in enumerate(games):
        match_ids[game] = id

    df["MatchId"] = df["Match"].map(match_ids)
    return df

df = pd.read_excel("../../data2526/half_season/20260105_updated.xlsx")
df = df.rename(columns={"Act Name": "Player"})

for idx, game in enumerate(df["Match"]):
    teams = game.split("vs")
    home, away = [x.strip() for x in teams]

    df.at[idx, "Opponent"] = away if df.at[idx, "Team"] == home else home

WEEK = df["Gameweek"].max()
TEAMS = df["Team"].unique()
OPPONENTS = df["Opponent"].unique()

def processData(frame: pd.DataFrame, is_def):
    data = frame.loc[frame["Action"].isin(DEF_ACTIONS if is_def else PASSES)].copy()
    # data["Min"] = frame["Min"].apply(lambda x: parseTime(x))
    data["X1"] = frame["X1"].apply(lambda x: x * PITCH_X/100)
    data["X2"] = frame["X2"].apply(lambda x: x * PITCH_X/100)
    data["Y1"] = frame["Y1"].apply(lambda y: PITCH_Y - (y * PITCH_Y/100))
    data["Y2"] = frame["Y2"].apply(lambda y: PITCH_Y - (y * PITCH_Y/100))

    condition_true = data["X1"].notna() & data["Y1"].notna()
    condition_false = data["X2"].notna() & data["Y2"].notna()
    data = data.loc[condition_true] if is_def else data.loc[condition_false]

    return data

def createCluster(data: np.ndarray, k: int):
    cluster = KMeans(n_clusters=k, random_state=69)
    labels = cluster.fit_predict(data)
    centroids = cluster.cluster_centers_
    return labels, centroids

def plotZoneDensity(data: df.DataFrame, k: int):
    total_len = len(data)

    params = ["X1", "X1"]
    labels, _ = cluster(data[params].to_numpy(), k)
    data["group"] = labels

    pitch = Pitch(line_color='black', pitch_type = "custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, ax = pitch.draw(figsize=(8, 9))
    pitch.scatter(data.X1, data.Y1, alpha=0.4, s=50, c=data.group, cmap=GRUVBOX, ax=ax)

    for cluster in np.linspace(0, k-1, k):
        clustered = data.loc[data["group"] == cluster]
        pct_val = round((len(clustered) / total_len) * 100)
        x_mean = clustered.X1.mean()
        ax.text(x_mean, PITCH_Y/2, f"{pct_val}%",
                ha='center', va='center', fontsize=30)

    title = plt.title(f"{k} Klaster Aksi Bertahan\nBRI Super League 2025/26", fontdict=font(20))

    plt.show()

def plotClusteredZoneDensityPerTeam(data: df.DataFrame, teams: pd.Series, k: int):
    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    params = ["X1", "Y1"]

    for team, ax in zip(teams, axs['pitch'].flat[:18]):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Team"] == team].copy()
        labels, _ = createCluster(team_data[params].to_numpy(), k)
        team_data["group"] = labels
        total_len = len(team_data)


        for i, cluster in enumerate(np.linspace(0, k-1, k)):
            clustered = team_data.loc[team_data["group"] == cluster]
            pct_val = round((len(clustered) / total_len) * 100)
            x_mean = clustered.X1.mean()
            y_mean = clustered.Y1.mean()

            color = COLORS[i % len(COLORS)]
            hull = pitch.convexhull(clustered.X1, clustered.Y1)
            poly = pitch.polygon(hull, ax=ax, edgecolor=color, facecolor=color, alpha=0.3)
            pitch.scatter(
                clustered.X1,
                clustered.Y1,
                alpha=0.4,
                s=10,
                c=color,
                ax=ax
            )

            ax.text(x_mean, y_mean, f"{pct_val}%",
                    ha='center', va='center', fontsize=9)

    axs['title'].text(
        0.5, 0.2,
        f"{k} Zona Aksi Bertahan Masing-masing Tim\nBRI Super League 2025/26",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotMostTargetedZonePerTeam(data: df.DataFrame, teams: pd.Series, k: int):
    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    params = ["X2", "Y2"]

    for team, ax in zip(teams, axs['pitch'].flat[:18]):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Opponent"] == team].copy()
        labels, _ = createCluster(team_data[params].to_numpy(), k)
        team_data["group"] = labels
        total_len = len(team_data)


        for i, cluster in enumerate(np.linspace(0, k-1, k)):
            clustered = team_data.loc[team_data["group"] == cluster]
            pct_val = round((len(clustered) / total_len) * 100)
            x_mean = clustered.X2.mean()
            y_mean = clustered.Y2.mean()

            color = COLORS[i % len(COLORS)]
            hull = pitch.convexhull(clustered.X2, clustered.Y2)
            poly = pitch.polygon(hull, ax=ax, edgecolor=color, facecolor=color, alpha=0.3)
            pitch.scatter(
                clustered.X2,
                clustered.Y2,
                alpha=0.4,
                s=10,
                c=color,
                ax=ax
            )

            ax.text(x_mean, y_mean, f"{pct_val}%",
                    ha='center', va='center', fontsize=9)

    axs['title'].text(
        0.5, 0.2,
        f"{k} Zona Paling Sering Dimanfaatkan Lawan dari Masing-masing Tim\nBRI Super League 2025/26",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def zones(x, cat):
    fifth = cat / 5
    if x <= fifth:
        return 0
    elif (x > fifth) and (x <= 2 * fifth):
        return 1
    elif (x > 2 * fifth) & (x <= 3 * fifth):
        return 2
    elif (x > 3 * fifth) & (x <= 4 * fifth):
        return 3
    elif (x > 4 * fifth) & (x <= cat):
        return 4

def plotDefensiveZonePerTeam(data: df.DataFrame, teams: pd.Series, div):
    pitch = Pitch(line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    params = ["X1", "X1"]

    for i, (team, ax) in enumerate(zip(teams, axs['pitch'].flat[:18])):
        ax.text(52.5, 74, f"{team}", ha='center', va='center', fontsize=10)

        team_data = data.loc[data["Team"] == team].copy()
        team_data["Zone"] = team_data[div].apply(lambda x: zones(x, PITCH_X if div == "X1" else PITCH_Y))
        total_len = len(team_data)

        pitch.scatter(
            team_data.X1,
            team_data.Y1,
            alpha=0.4,
            s=10,
            c=team_data.Zone,
            cmap=GRUVBOX_V if div == "X1" else GRUVBOX_H,
            ax=ax
        )

        for zone in range(5):
            clustered = team_data.loc[team_data["Zone"] == zone]

            if div == "X1":
                pct_val = round((len(clustered) / total_len) * 100)
                x_mean = clustered.X1.mean()
                ax.text(x_mean, -6, f"{pct_val}%", ha='center', va='center', fontsize=9)
            else:
                own_count = len(team_data.loc[team_data["X1"] < PITCH_X / 2].Y1)
                own_half = clustered.loc[clustered["X1"] < PITCH_X / 2].Y1
                pct_val = round((len(own_half) / own_count) * 100)
                ax.text(PITCH_X/3.5, own_half.mean(), f"{pct_val}%", ha="center", va="center", fontsize=9)

                opp_count = len(team_data.loc[team_data["X1"] >= PITCH_X / 2].Y1)
                opp_half = clustered.loc[clustered["X1"] >= PITCH_X / 2].Y1
                pct_val = round((len(opp_half) / opp_count) * 100)
                ax.text(PITCH_X - PITCH_X/3.5, opp_half.mean(), f"{pct_val}%", ha="center", va="center", fontsize=9)

        if div == "Y1":
            ax.text(0, -6, "Own Half", ha="left", va="center", fontsize=7)
            ax.text(PITCH_X, -6, "Opponent's Half", ha="right", va="center", fontsize=7)

    cat = {
        "X1": "Zona Vertikal",
        "Y1": "Koridor Horizontal"
    }

    t = cat[div]

    axs['title'].text(
        0.5, 0.2,
        f"Aktivitas Aksi Bertahan Masing-masing Tim Berdasarkan {t}\nBRI Super League 2025/26",
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

# plotZoneDensity(processData(df, True), 4)
plotClusteredZoneDensityPerTeam(processData(df, True), TEAMS, 11)
# plotMostTargetedZonePerTeam(processData(df, False), OPPONENTS, 11)
# plotDefensiveZonePerTeam(processData(df, True), TEAMS, "X1")
