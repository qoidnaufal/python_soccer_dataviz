import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

from mplsoccer import VerticalPitch
from matplotlib.colors import ListedColormap

PITCH_X = 105
PITCH_Y = 68

COLORS_5 = [
    "#98971a",
    "#d5c4a1",
    "#d79921",
    "#d65d0e",
    "#cc241d",
]

COLORS = [
    "#d5c4a1",
    "#d79921",
    "#d65d0e",
    "#cc241d",
    "#b16286",
    "#665c54",
    "#458588",
    "#689d6a",
    "#98971a",
]

GRUVBOX_5 = ListedColormap(COLORS_5)
GRUVBOX = ListedColormap(COLORS)

def setOpponent(frame: pd.DataFrame, separator: str):
    data = frame.copy().rename(columns={"Team": "Attacking"})
    data = data.fillna(0)

    for idx, game in enumerate(data["Match"]):
        teams = game.split(separator)
        home, away = [x.strip() for x in teams]

        data.at[idx, "Defending"] = away if data.at[idx, "Attacking"] == home else home

    return data

def getTotalCorners(frame: pd.DataFrame, state: str):
    return frame[["Corner", state]].groupby(state).sum()

def getGrossXG(frame: pd.DataFrame, state: str):
    return frame[[state, "xG"]].groupby(state).sum()

def getCleanXG(frame: pd.DataFrame, state: str):
    data = frame.loc[(frame["Event"] == "Goal")]
    return data[[state, "xG"]].groupby(state).sum()

def getShots(frame: pd.DataFrame, state: str):
    data = frame[state].value_counts()
    return pd.DataFrame(data)

def getGoals(frame: pd.DataFrame, state: str):
    data = frame.loc[(frame["Event"] == "Goal")]
    data =  data[state].value_counts()
    return pd.DataFrame(data)

def shotDistribution(frame: pd.DataFrame, state: str):
    data =  frame[[state, "Event"]].groupby(state).value_counts()
    return pd.DataFrame(data)

def getTeamData(df_xg: pd.DataFrame, df_shots: pd.DataFrame, state: str):
    total_ck = getTotalCorners(df_shots, state).rename(columns={"Corner": "CornersFaced" if state == "Defending" else "CornersAttempted"})

    grossXG = getGrossXG(df_xg, state).rename(columns={"xG": "gross_xG"})
    cleanXG = getCleanXG(df_xg, state).rename(columns={"xG": "clean_xG"})

    shot_param = "ShotsConceded" if state == "Defending" else "ShotsAttempted"
    goal_param = "GoalsConceded" if state == "Defending" else "GoalsScored"
    xg_per_shot_param = "xGpSC" if state == "Defending" else "xGpS"
    xg_per_goal_param = "xGpGC" if state == "Defending" else "xGpG"

    shots = getShots(df_xg, state).rename(columns={"count": shot_param})
    goals = getGoals(df_xg, state).rename(columns={"count": goal_param})

    team_data = pd.concat([total_ck, shots, goals, grossXG, cleanXG], axis=1)

    team_data[xg_per_shot_param] = team_data.gross_xG / team_data[shot_param]
    team_data[xg_per_goal_param] = team_data.clean_xG / team_data[goal_param]

    return team_data

def plotShotMapPerTeam(frame: pd.DataFrame, state: str):
    data = frame.copy()
    data["X"] = data["X"].apply(lambda x: PITCH_X - x)

    teams = data[state].unique()

    pitch = VerticalPitch(half=True, line_color='black', pitch_type="custom", pitch_length=PITCH_X, pitch_width=PITCH_Y)
    fig, axs = pitch.grid(ncols=6, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    event_color = {
        "Goal": '#cc241d',
        "Shot On": '#d65d0e',
        "Shot Off": '#fabd2f',
        "Shot Blocked": '#b8bb26',
    }

    for team, ax in zip(teams, axs['pitch'].flat[:18]):
        ax.text(
            PITCH_Y/2,
            PITCH_X + 6,
            f"{team}",
            ha='center',
            va='center',
            fontsize=10
        )

        team_data = data.loc[data[state] == team]

        goals = team_data.loc[team_data.Event == "Goal"]
        on_target = team_data.loc[team_data.Event == "Shot On"]
        off_target = team_data.loc[team_data.Event == "Shot Off"]
        blocked = team_data.loc[team_data.Event == "Shot Blocked"]

        pitch.scatter(
            goals.X,
            goals.Y,
            marker="*",
            zorder=3,
            alpha=0.8,
            s=goals.xG * 500 + 10,
            c=event_color["Goal"],
            linewidths=0.7,
            edgecolors="black",
            ax=ax
        )

        pitch.scatter(
            on_target.X,
            on_target.Y,
            zorder=2,
            alpha=0.8,
            s=on_target.xG * 500 + 10,
            c=event_color["Shot On"],
            linewidths=0.7,
            edgecolors="black",
            ax=ax
        )

        pitch.scatter(
            off_target.X,
            off_target.Y,
            zorder=1,
            alpha=0.8,
            s=off_target.xG * 500 + 10,
            c=event_color["Shot Off"],
            linewidths=0.7,
            edgecolors="black",
            ax=ax
        )

        pitch.scatter(
            blocked.X,
            blocked.Y,
            zorder=0,
            alpha=0.8,
            s=blocked.xG * 500 + 10,
            c=event_color["Shot Blocked"],
            linewidths=0.7,
            edgecolors="black",
            ax=ax
        )

        goals_count = len(goals)
        shots = len(team_data)
        xG_val = round(team_data.xG.sum(), 2)
        b_txt = ["scored", "xG"] if state == "Attacking" else ["conceded", "xGC"]

        ax.text(
            PITCH_Y/2, PITCH_X/2,
            f"goals {b_txt[0]}: {goals_count}\n{b_txt[1]}: {xG_val}\nshots: {shots}",
            color = 'black',
            ha = 'center',
            va = 'center',
            fontsize = 8,
            bbox={'facecolor': '#ebdbb2', 'pad': 4}
        )

    t_txt = "Diterima" if state == "Defending" else "Dihasilkan"

    axs['title'].text(
        0.5, 0.2,
        f'Peta Tembakan yang {t_txt} dari Situasi {state} Corner Kick\nBRI Super League 2025/26',
        ha='center',
        va='center',
        fontsize=20
    )

    plt.show()

def plotCKProficiency(df_xg: pd.DataFrame, df_shot: pd.DataFrame, state: str):
    data = getTeamData(df_xg, df_shot, state)
    data = data.fillna(0)
    x = ((data.ShotsConceded / data.CornersFaced) if state == "Defending" else (data.ShotsAttempted / data.CornersAttempted)) * 10
    y = (data.xGpSC if state == "Defending" else data.xGpS) * 10

    _, ax = plt.subplots(figsize=(9, 9), layout='constrained')

    c_param = data.GoalsConceded if state == "Defending" else data.GoalsScored
    cm = "Reds" if state == "Defending" else "YlGn"
    sc = ax.scatter(x, y, s=150, c=c_param, cmap=cm, linewidths=1, edgecolors="black")

    ax.plot([np.median(x),np.median(x)],[y.max(),y.min()], color="#282828", linestyle = ":", lw=1)
    ax.plot([x.min(),x.max()],[np.median(y),np.median(y)], color="#282828", linestyle = ":", lw=1)

    cbar = ax.figure.colorbar(sc, shrink=0.5)

    bar_label = "Kebobolan" if state == "Defending" else "Gol Dicetak"
    ax_label = "Diterima" if state == "Defending" else "Dihasilkan"

    cbar.ax.set_ylabel(f"\nJumlah {bar_label} dari Tendangan Sudut", rotation=-90, va="bottom", size=10)
    ax.set_xlabel(f"Tembakan yang {ax_label} tiap 10 Tendangan Sudut\n", size=10, labelpad=12)
    ax.set_ylabel(f"\nxG per 10 Tembakan yang {ax_label}", size=10, labelpad=12)

    ax.tick_params(top=False, right=False)

    att_offset = ["PERSIB", "PERSEBAYA Surabaya"]
    def_offset = ["Madura United FC"]
    offset = def_offset if state == "Defending" else att_offset

    for i, txt in enumerate(data.index):
        ax.annotate(
            txt,
            (x.iloc[i], y.iloc[i]),
            xytext=(-10, 0) if txt in offset else (10, 0),
            textcoords="offset points",
            color = 'black',
            ha= "right" if txt in offset else 'left',
            va='center'
        )

    ax.set_title(
        f"Performa Masing-masing Tim dalam Situasi {state} Corner Kick",
        fontdict={
            "fontsize": 15,
        },
        pad=10.0
    )

    plt.show()

def plotAttackVSDefend(df_xg: pd.DataFrame, df_shot: pd.DataFrame):
    attack = getTeamData(df_xg, df_shot, "Attacking").rename(
        columns={
            "Attacking": "Team",
            "gross_xG": "att_xG",
        }
    )
    attack = attack.fillna(0)

    defend = getTeamData(df_xg, df_shot, "Defending").rename(
        columns={
            "Defending": "Team",
            "gross_xG": "def_xG",
        }
    )
    defend = defend.fillna(0)

    data = pd.concat([attack, defend], axis=1)
    att_v_def = data.GoalsScored - data.GoalsConceded

    x = (data.att_xG / data.CornersAttempted) * 10
    y = (data.def_xG / data.CornersFaced) * 10

    gr = mpl.colormaps['Greens'].resampled(128)
    rd = mpl.colormaps['Reds_r'].resampled(128)

    newcolors = np.vstack((rd(np.linspace(0.2, 1, 128)), gr(np.linspace(0, 0.8, 128))))
    rdgr = ListedColormap(newcolors)

    _, ax = plt.subplots(figsize=(9, 9), layout='constrained')
    sc = ax.scatter(x, y, s=150, linewidths=1, c=att_v_def, cmap=rdgr, edgecolors="black")
    ax.yaxis.set_inverted(True)

    ax.plot([np.median(x),np.median(x)],[y.max(),y.min()], color="#282828", linestyle = ":", lw=1)
    ax.plot([x.min(),x.max()],[np.median(y),np.median(y)], color="#282828", linestyle = ":", lw=1)

    ax.set_xlabel("xG dihasilkan tiap 10 tendangan sudut\n", size=10, labelpad=12)
    ax.set_ylabel("\nxG diderita tiap 10 tendangan sudut", size=10, labelpad=12)

    cbar = ax.figure.colorbar(sc, shrink=0.5)
    cbar.ax.set_ylabel(f"\nselisih gol vs kebobolan", rotation=-90, va="bottom", size=10)

    offset = ["PERSIB", "PERSIJAP", "PERSITA", "Malut United FC", "Madura United FC", "Bhayangkara Presisi Lampung FC"]

    for i, txt in enumerate(data.index):
        ax.annotate(
            txt,
            (x.iloc[i], y.iloc[i]),
            xytext=(-10, 0) if txt in offset else (10, 0),
            textcoords="offset points",
            color = 'black',
            ha= "right" if txt in offset else 'left',
            va='center'
        )

    ax.annotate(
        "jago attack, jago defend",
        (x.max() + (x.max()/70), y.min() - (y.min()/20)),
        color = 'black',
        ha = 'right',
        va = 'center',
        size = 8,
        bbox={'facecolor': '#ebdbb2', 'pad': 4}
    )
    ax.annotate(
        "jago defend, payah attack",
        (x.min() - (x.min()/20), y.min() - (y.min()/20)),
        color = 'black',
        ha = 'left',
        va = 'center',
        size = 8,
        bbox={'facecolor': '#ebdbb2', 'pad': 4}
    )
    ax.annotate(
        "payah attack, payah defend",
        (x.min() - (x.min()/20), y.max() + (y.max()/70)),
        color = 'black',
        ha = 'left',
        va = 'center',
        size = 8,
        bbox={'facecolor': '#ebdbb2', 'pad': 4}
    )
    ax.annotate(
        "jago attack, payah defend",
        (x.max() + (x.max()/70), y.max() + (y.max()/70)),
        color = 'black',
        ha = 'right',
        va = 'center',
        size = 8,
        bbox={'facecolor': '#ebdbb2', 'pad': 4}
    )

    ax.set_title(
        "Kemampuan Attack vs Defend Corner Kick Masing-masing Tim\nBRI Super League 2026 (hingga tengah musim)",
        fontdict={
            "fontsize": 15,
        },
        pad=10.0
    )

    plt.show()

# df_shots = setOpponent(pd.read_excel("../../data2526/half_season/corner-kick.xlsx"), "-")
# df_xg = setOpponent(pd.read_excel("../../data2526/half_season/xG-from-corner.xlsx"), "vs")

# plotCKProficiency(
#     setOpponent(pd.read_excel("../../data2526/half_season/xG-from-corner.xlsx"), "vs"),
#     setOpponent(pd.read_excel("../../data2526/half_season/corner-kick.xlsx"), "-"),
#     "Attacking",
# )

# plotShotMapPerTeam(
#     setOpponent(pd.read_excel("../../data2526/half_season/xG-from-corner.xlsx"), "vs"),
#     "Defending"
# )

# plotAttackVSDefend(
#     setOpponent(pd.read_excel("../../data2526/half_season/xG-from-corner.xlsx"), "vs"),
#     df_shots
# )
