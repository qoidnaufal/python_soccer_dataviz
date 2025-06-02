import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("~/Documents/LearnRust/tsg2425/dataset/touchfinal3rd.csv")
df_ppda = pd.read_csv("~/Documents/LearnRust/tsg2425/dataset/ppda.csv")

df_ppda = df_ppda.fillna(0)
df_ppda = df_ppda.replace(to_replace="-", value=0)
df_ppda[["Winning", "Drawing", "Losing"]] = df[["Winning", "Drawing", "Losing"]].apply(pd.to_numeric)
df_ppda = df_ppda[["Team", "Winning", "Drawing", "Losing"]]
df_ppda = df_ppda.groupby(["Team"]).mean()

df = df.rename(columns={
              "Winning": "W",
              "Drawing": "D",
              "Losing": "L"
          })
idx = 0
for game in df["Match"]:
    teams = game.split("vs")
    teams = [x.strip() for x in teams]

    opponent = ""

    if df.at[idx, "Team"] == teams[0]:
        opponent = teams[1]
    else:
        opponent = teams[0]

    df.at[idx, "Opponent"] = opponent

    df.at[idx, "OppW"] = df.loc[(df["Match"] == game) & (df["Team"] == opponent)]["W"].iloc[0]
    df.at[idx, "OppD"] = df.loc[(df["Match"] == game) & (df["Team"] == opponent)]["D"].iloc[0]
    df.at[idx, "OppL"] = df.loc[(df["Match"] == game) & (df["Team"] == opponent)]["L"].iloc[0]

    idx += 1

df["Winning"] = df["W"] / (df["W"] + df["OppL"])
df["Drawing"] = df["D"] / (df["D"] + df["OppD"])
df["Losing"] = df["L"] / (df["L"] + df["OppW"])

df = df.fillna(0)

df = df[["Team", "Winning", "Drawing", "Losing"]]
df = df.groupby(["Team"]).mean()
df["Total"] = (df["Winning"] + df["Drawing"] + df["Losing"]) / 3

teams = df.index
idx = np.arange(len(teams))
w = df["Winning"]
d = df["Drawing"]
l = df["Losing"]
total = df["Total"]
width = 0.25

fig = plt.figure(figsize=(16, 9))
grid = fig.add_gridspec(1, 2, width_ratios=(1, 1), left=0.15, right=0.93, wspace=0.45)

ax = fig.add_subplot(grid[0, 0])

ax.barh(idx-width, w, width, color="green")
ax.barh(idx, d, width, color="orange")
ax.barh(idx+width, l, width, color="red")
ax.legend(["Winning", "Drawing", "Losing"])

ax.set_yticks(idx, teams)
ax.invert_yaxis()

# ax.set_xlabel("Average Field Tilt")
# ax.set_ylabel("Teams")
ax.plot([0.5, 0.5], [idx.min() - 1, idx.max() + 1], 'k-', linestyle = ":", lw=1)
ax.set_title("Average Field Tilt per Gamestate")

ax_ppda = fig.add_subplot(grid[0, 1], sharey=ax)
# ax_ppda.tick_params(axis="y", labelleft=False)
ax_ppda.tick_params(axis="x", labelbottom=False)

ppda_width = 0.4
ax_ppda.barh(idx-(ppda_width/2), df_ppda["Winning"], ppda_width, color="green")
ax_ppda.barh(idx+(ppda_width/2), df_ppda["Drawing"], ppda_width, color="orange")
ax_ppda.barh(idx, df_ppda["Losing"].apply(lambda x: x*-1), ppda_width, color="red")
ax_ppda.set_yticks(idx, teams)
ax_ppda.legend(["Winning", "Drawing", "Losing"])
ax_ppda.set_title("Average PPDA Comparison between Gamestate")

plt.show()
