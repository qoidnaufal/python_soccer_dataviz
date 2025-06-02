import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
fig.subplots_adjust(wspace=0)
fig.text(
    0.5, 0.95, "Academy Product Contribution in BRI Liga 1 2024/25",
    size=20,
    ha="center", color="#000000"
)


total_minutes = 11 * 34 * 90 * 18

# ###################################################
#
#                      FOREIGN
#
# ###################################################

foreign = pd.read_csv("~/Documents/LearnPython/tsg2425/data/mop.csv")
foreign = foreign.loc[
    foreign['Nationality'].str.contains('Indonesia') == False
]
foreign_minutes = foreign['MoP'].sum()
foreign_contribution = foreign_minutes / total_minutes

# ###################################################
#
#                  ACADEMY PRODUCT
#
# ###################################################

ap = pd.read_csv("~/Documents/LearnPython/tsg2425/data/ap.csv")
ap = ap[['Klub', 'AP minutes', '%']]
ap = ap.set_index('Klub')

ap_minutes = ap['AP minutes'].sum()
max_ap_minutes = ap['AP minutes'].max()
ap_contribution = ap_minutes / total_minutes

# ###################################################
#
#                  LOCAL PLAYERS
#
# ###################################################

non_ap_players_minutes = total_minutes - foreign_minutes - ap_minutes
non_ap_contribution = non_ap_players_minutes / total_minutes

dist = [ap_contribution, foreign_contribution, non_ap_contribution]
labels = ["Academy Product", "Foreign", "Non Academy Product"]
explode = [0.1, 0, 0]

# prepare
angle = -180 * dist[0]
wedges, *_ = ax1.pie(dist, autopct='%1.1f%%', startangle=angle, labels=labels, explode=explode)
bottom = 1
width = 0.2

# bar chart
ap_params = ap['AP minutes'].apply(lambda x: x / ap_minutes).to_list()
ap_labels = ap.index.to_list()
print(ap_labels)

colors = {
    "Persija Jakarta": "orange",
    "Persib Bandung": "blue",
    "Persebaya Surabaya": "green",
    "Barito Putera": "yellow",
    "Persis Solo": "red",
    "Persita Tangerang": "purple",
    "PSM Makassar": "red",
    "Bali United": "red",
    "PSIS Semarang": "blue",
    "PSS Sleman": "green",
    "Borneo FC": "red",
    "Semen Padang": "red",
    "Arema FC": "blue",
    "Dewa United": "gold",
    "Madura United": "red",
    "Persik Kediri": "purple",
    "PSBS Biak": "blue",
    "Malut United": "red"
}

# Adding from the top matches the legend.
for j, (height, label) in enumerate([*zip(ap_params, ap_labels)]):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color=colors.get(label), label=label,
                 alpha=max([height*ap_minutes/(max_ap_minutes), 0.3]))
    value = ap.loc[label, 'AP minutes']
    ax2.bar_label(bc, labels=[value], label_type='center')

ax2.set_title('Minutes Contribution')
ax2.legend(loc='center right')
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = sum(ap_params)

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(2)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(2)

plt.show()
