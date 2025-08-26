import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

TOTAL_MINUTES = 11 * 34 * 90

df_youth = pd.read_csv("~/Documents/LearnPython/tsg2425/data/youth.csv")
df_youth = df_youth.sort_values(by=['Total Minutes'], ascending=False)

# ###################################################
#
#                     All Youth
#
# ###################################################

df_all = pd.read_csv("~/Documents/LearnPython/tsg2425/data/all_youth_minutes.csv")

# ###################################################
#
#                      >= 900
#
# ###################################################

df_900 = pd.read_csv("~/Documents/LearnPython/tsg2425/data/nine_hundred_players.csv")
df_900 = df_900.sort_values(by=['Minutes'], ascending=False)

# ###################################################
#
#                       Youth
#
# ###################################################

teams = df_youth['Team']
idx = np.arange(len(teams))
minutes = df_youth['Total Minutes']
total_players = df_youth['Players with Minutes']
ratio = minutes / total_players

max_minutes = minutes.max()
max_num = total_players.max()

# ###################################################
#
#                       Label
#
# ###################################################

p_label = total_players.to_list()
total_players = total_players.apply(lambda x: x * max_minutes / max_num / 2)

ratio = ratio.apply(lambda x: int(x))

# ###################################################
#
#                       Plot
#
# ###################################################

fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
width = 0.3

m_rect = ax.barh(idx-width/2, minutes, width, color="green")
ax.bar_label(m_rect, padding=3)

p_rect = ax.barh(idx+width/2, total_players, width, color="orange")
ax.bar_label(p_rect, labels=p_label, padding=3)

ax.plot(ratio, idx, color='blue', marker='o', linestyle='dashed')
# ax.label(r_line, labels=r_label, padding=3)

ax.set_yticks(idx, teams)
ax.invert_yaxis()
ax.set_xlim(0, max_minutes + max_minutes * 10 / 100)

ax.legend(["Average minutes per U22 player", "U22 players total minutes", "U22 players with minutes"])
title = ax.set_title("U22 Players Minutes Contribution\nBRI Liga 1 2024/25")
title.set(fontsize='xx-large', fontweight='bold')

plt.show()
