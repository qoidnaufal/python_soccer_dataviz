import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

TOTAL_MINUTES = 6 * 34 * 90

# TODO: Average starters per game

# ###################################################
#
#                      FOREIGN
#
# ###################################################

foreign = pd.read_csv("~/Documents/LearnPython/tsg2425/data/mop.csv")
foreign = foreign.loc[
    foreign['Nationality'].str.contains('Indonesia') == False
]
# foreign_minutes = foreign['MoP'].sum()
# foreign_contribution = foreign_minutes / TOTAL_MINUTES
# print(foreign_contribution)

foreign_per_club = foreign[['Team', 'MoP']]
foreign_per_club = foreign_per_club.groupby(['Team']).sum()
foreign_per_club['Contribution %'] = foreign_per_club['MoP'] / TOTAL_MINUTES * 100
foreign_per_club = foreign_per_club.sort_values(by=['MoP'], ascending=False)

# print(foreign_per_club)
# print(f"max possible minutes: {TOTAL_MINUTES}")

# ###################################################
#
#                     INGREDIENTS
#
# ###################################################

teams = foreign_per_club.index
idx = np.arange(len(teams))

minutes = foreign_per_club['MoP']
percentage = foreign_per_club['Contribution %'].apply(lambda x: np.round(x))
p_label = percentage.to_list()

# ###################################################
#
#                        PLOT
#
# ###################################################

fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
width = 0.4

rect = ax.barh(idx-width/2, minutes, width, color="green")
ax.bar_label(rect, padding=3)

p_rect = ax.barh(idx+width/2, minutes/2, width, color="orange")
ax.bar_label(p_rect, labels=p_label, padding=3)

ax.set_yticks(idx, teams)
ax.invert_yaxis()
ax.set_xlim(0, TOTAL_MINUTES + TOTAL_MINUTES * 10 / 100)

ax.legend(["Playing minutes", "% minutes contribution"])
title = ax.set_title("Foreign Players Minutes Contribution\nin BRI Liga 1 2024/25")
title.set(fontsize='xx-large', fontweight='bold')

plt.show()
