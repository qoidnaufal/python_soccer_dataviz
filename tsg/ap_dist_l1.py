import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
fig.subplots_adjust(wspace=0)
fig.text(
    0.5, 0.95, "Academy Product Contribution in BRI Super League 2025/26",
    size=20,
    ha="center", color="#000000"
)

# players on field * total games * 90 * total clubs
TOTAL_MINUTES_L1 = 11 * 34 * 90 * 18

# ###################################################
#
# FOREIGN
#
# ###################################################

mop = pd.read_csv("~/Documents/LearnPython/tsg/youth_data/2526/mop.csv")

foreign = mop.loc[(mop['Nationality'].str.contains('Indonesia') == False) & (mop['Competition'].str.contains('BRI') == True)]
foreign_minutes = foreign['MOP'].sum()
foreign_contribution = foreign_minutes / TOTAL_MINUTES_L1

# ###################################################
#
# ADJUSTED ACADEMY PRODUCT
#
# ###################################################

ap = pd.read_csv("~/Documents/LearnPython/tsg/youth_data/2526/academy_product.csv")

# ap_club = ap.sort_values(by=['Adj Minutes in Club'], ascending=False)
# ap_club = ap_club.set_index('Club Name')
adjusted_club_ap_minutes = ap['Adj Minutes in Club'].sum()
club_ap_contribution = adjusted_club_ap_minutes / TOTAL_MINUTES_L1

# ap_l1 = ap.sort_values(by=['Adj Minutes in Liga 1'], ascending=False)
# ap_l1 = ap_l1.set_index('Club Name')
adjusted_other_ap_minutes = ap['Adj Minutes in Other Liga 1'].sum()
other_ap_contribution = adjusted_other_ap_minutes / TOTAL_MINUTES_L1

total_adjusted_ap_minutes = adjusted_club_ap_minutes + adjusted_other_ap_minutes
adjusted_ap_contribution = club_ap_contribution + other_ap_contribution

# ###################################################
#
# NON ADJUSTED ACADEMY PRODUCT
#
# ###################################################

ap_l1 = ap.sort_values(by=['Minutes in Liga 1'], ascending=False)
ap_l1 = ap_l1.set_index('Club Name')

total_ap_minutes = ap_l1['Minutes in Liga 1'].sum()
max_ap_minutes = ap_l1['Minutes in Liga 1'].max()

# ###################################################
#
# LOCAL PLAYERS
#
# ###################################################

non_ap_players_minutes = TOTAL_MINUTES_L1 - foreign_minutes - total_adjusted_ap_minutes
non_ap_contribution = non_ap_players_minutes / TOTAL_MINUTES_L1

# ###################################################
#
# PLOTTING DATA
#
# ###################################################

dist = [adjusted_ap_contribution, foreign_contribution, non_ap_contribution]
labels = ["Academy Product", "Foreign", "Non Academy Product"]
explode = [0.1, 0, 0]

# prepare
angle = -180 * dist[0]
wedges, pie_labels, auto_txts = ax1.pie(dist, autopct='%1.1f%%', startangle=angle, labels=labels, explode=explode, labeldistance=0.75)

wedges[0].set(color='#5CB338', edgecolor='black', linewidth=2)
wedges[1].set(color='#578FCA')
wedges[2].set(color='#F79B72')

x0, y0 = auto_txts[0].get_position()
pie_labels[0].set_position((x0, y0 + 0.2))

x1, y1 = auto_txts[1].get_position()
pie_labels[1].set_position((x1, y1 + 0.2))

x2, y2 = auto_txts[2].get_position()
pie_labels[2].set_position((x2, y2 + 0.2))

bottom = 1
width = 0.2

# bar chart
# ap_params = adjusted_ap['Adjusted Total Minutes'].apply(lambda x: x / total_adjusted_ap_minutes).to_list()
ap_params = ap_l1['Minutes in Liga 1'].apply(lambda x: x / total_ap_minutes).to_list()
ap_labels = ap_l1.index.to_list()
# print(ap_labels)

colors = {
    "Persija Jakarta": "#DF2C20",
    "Persib Bandung": "blue",
    "Persebaya Surabaya": "green",
    "Bhayangkara Presisi Lampung FC": "yellow",
    "Persis Solo": "red",
    "Persita Tangerang": "purple",
    "PSM Makassar": "red",
    "Bali United": "red",
    "PSIM Yogyakarta": "blue",
    "Persijap Jepara": "red",
    "Borneo FC": "red",
    "Semen Padang": "red",
    "Arema FC": "blue",
    "Dewa United": "#FAC60D",
    "Madura United": "red",
    "Persik Kediri": "purple",
    "PSBS Biak": "cyan",
    "Malut United": "red"
}

# colors = {
#     "Persija Jakarta": "#DF2C20",
#     "Persib Bandung": "blue",
#     "Persebaya Surabaya": "green",
#     "Barito Putera": "yellow",
#     "Persis Solo": "red",
#     "Persita Tangerang": "purple",
#     "PSM Makassar": "red",
#     "Bali United": "red",
#     "PSIS Semarang": "blue",
#     "PSS Sleman": "green",
#     "Borneo FC": "red",
#     "Semen Padang": "red",
#     "Arema FC": "blue",
#     "Dewa United": "#FAC60D",
#     "Madura United": "red",
#     "Persik Kediri": "purple",
#     "PSBS Biak": "blue",
#     "Malut United": "red"
# }

# Adding from the top matches the legend.
for j, (height, label) in enumerate([*zip(ap_params, ap_labels)]):
    bottom -= height
    # alpha = max([height*total_ap_minutes/(max_ap_minutes), 0.5-(j/100)])
    # alpha = np.clip(alpha, 0, 1)
    bc = ax2.bar(0, height, width, bottom=bottom, color=colors.get(label), edgecolor='black', label=label, alpha=1.0)
    value = ap_l1.loc[label, 'Minutes in Liga 1']
    color = 'white'
    if label == "Bhayangkara Presisi Lampung FC" or label == "Dewa United":
        color = 'black'
    ax2.bar_label(bc, labels=[value], label_type='center', color=color)

# ax2.set_title('Minutes Contribution')
ax2.legend(title='Clubs', loc='center right')
ax2.axis('off')
ax2.set_xlim(-width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = sum(ap_params)

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(1)
con.set_linestyle("--")
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(1)
con.set_linestyle("--")
ax2.add_artist(con)

ax1.axis('off')

plt.show()
