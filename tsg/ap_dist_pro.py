import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
fig.subplots_adjust(wspace=0)
fig.text(
    0.5, 0.95, "Academy Product Contribution in Indonesian Professional Leagues (L1 + L2) 2025/26",
    size=20,
    ha="center", color="#000000"
)

# players on field * total games * 90 * total clubs
TOTAL_MINUTES_L1 = 11 * 34 * 90 * 18
TOTAL_MINUTES_L2_REGULAR = 11 * 27 * 90 * 10
TOTAL_MINUTES_L2_PLAYOFF = TOTAL_MINUTES_L2_REGULAR + (90 * 11)
TOTAL_MINUTES_L2_FINAL = TOTAL_MINUTES_L2_REGULAR + (120 * 11)

NON_REGULAR = [
    "PSS SLEMAN",
    "GARUDAYAKSA FC",
    "PERSIPURA JAYAPURA",
    "ADHYAKSA FC BANTEN",
    "PERSEKAT TEGAL",
    "PERSIBA BALIKPAPAN"
]

PLAYOFF_TEAMS = [
    "PERSIPURA JAYAPURA",
    "ADHYAKSA FC BANTEN",
    "PERSEKAT TEGAL",
    "PERSIBA BALIKPAPAN"
]

FINAL_TEAMS = [
    "PSS SLEMAN",
    "GARUDAYAKSA FC",
]

# ###################################################
#
# FOREIGN
#
# ###################################################

mop = pd.read_csv("~/Documents/LearnPython/tsg/youth_data/2526/mop.csv")

l2_foreign = mop.loc[(mop['Nationality'].str.contains('Indonesia') == False) & (mop['Competition'].str.contains('BRI') == False)]

l2_foreign_regular = l2_foreign.loc[~l2_foreign['Team'].isin(NON_REGULAR)]
l2_foreign_regular_minutes = l2_foreign_regular['MOP'].sum()
l2_foreign_regular_contribution = l2_foreign_regular_minutes / TOTAL_MINUTES_L2_REGULAR

l2_foreign_playoff = l2_foreign.loc[l2_foreign['Team'].isin(PLAYOFF_TEAMS)]
l2_foreign_playoff_minutes = l2_foreign_playoff['MOP'].sum()
l2_foreign_playoff_contribution = l2_foreign_playoff_minutes / TOTAL_MINUTES_L2_PLAYOFF

l2_foreign_final = l2_foreign.loc[l2_foreign['Team'].isin(FINAL_TEAMS)]
l2_foreign_final_minutes = l2_foreign_final['MOP'].sum()
l2_foreign_final_contribution = l2_foreign_final_minutes / TOTAL_MINUTES_L2_FINAL

# l2_foreign_minutes = l2_foreign_regular_minutes + l2_foreign_playoff_minutes + l2_foreign_final_minutes
l2_foreign_contribution = (l2_foreign_regular_contribution + l2_foreign_playoff_contribution + l2_foreign_final_contribution)/3

l1_foreign = mop.loc[(mop['Nationality'].str.contains('Indonesia') == False) & (mop['Competition'].str.contains('BRI') == True)]
l1_foreign_minutes = l1_foreign['MOP'].sum()
l1_foreign_contribution = l1_foreign_minutes / TOTAL_MINUTES_L1

# foreign_minutes = l1_foreign_minutes + l2_foreign_minutes
foreign_contribution = (l1_foreign_contribution + l2_foreign_contribution)/2

# ###################################################
#
# ADJUSTED ACADEMY PRODUCT
#
# ###################################################

ap = pd.read_csv("~/Documents/LearnPython/tsg/youth_data/2526/academy_product.csv")

# ###################################################
#
# Adjusted AP L1
#
# ###################################################

l1_total_adjusted_ap_minutes = ap['Adj Minutes in Liga 1'].sum()
l1_adjusted_ap_contribution = l1_total_adjusted_ap_minutes / TOTAL_MINUTES_L1

# ###################################################
#
# Adjusted AP L2
#
# ###################################################

l2_adjusted_regular_ap_minutes = ap['Adj Minutes in Liga 2 Regular Teams'].sum()
l2_regular_ap_contribution = l2_adjusted_regular_ap_minutes / TOTAL_MINUTES_L2_REGULAR

l2_adjusted_playoff_ap_minutes = ap['Adj Minutes in Liga 2 Playoff Teams'].sum()
l2_playoff_ap_contribution = l2_adjusted_playoff_ap_minutes / TOTAL_MINUTES_L2_PLAYOFF

l2_adjusted_final_ap_minutes = ap['Adj Minutes in Liga 2 Final Teams'].sum()
l2_final_ap_contribution = l2_adjusted_final_ap_minutes / TOTAL_MINUTES_L2_FINAL

l2_adjusted_ap_contribution = (l2_regular_ap_contribution + l2_playoff_ap_contribution + l2_final_ap_contribution)/3

# ###################################################
#
# Adjusted AP L1 + L2
#
# ###################################################

adjusted_ap_contribution = (l1_adjusted_ap_contribution + l2_adjusted_ap_contribution)/2

# ###################################################
#
# NON ADJUSTED ACADEMY PRODUCT
#
# ###################################################

ap_all = ap.sort_values(by=['Total Minutes'], ascending=False)
ap_all = ap_all.set_index('Club Name')

total_ap_minutes = ap_all['Total Minutes'].sum()
max_ap_minutes = ap_all['Total Minutes'].max()

# ###################################################
#
# LOCAL PLAYERS
#
# ###################################################

l2_non_ap_playoff_players_minutes = TOTAL_MINUTES_L2_PLAYOFF - l2_foreign_playoff_minutes - l2_adjusted_playoff_ap_minutes
l2_non_ap_playoff_contribution = l2_non_ap_playoff_players_minutes / TOTAL_MINUTES_L2_PLAYOFF

l2_non_ap_regular_players_minutes = TOTAL_MINUTES_L2_REGULAR - l2_foreign_regular_minutes - l2_adjusted_regular_ap_minutes
l2_non_ap_regular_contribution = l2_non_ap_regular_players_minutes / TOTAL_MINUTES_L2_REGULAR

l2_non_ap_final_players_minutes = TOTAL_MINUTES_L2_FINAL - l2_foreign_final_minutes - l2_adjusted_final_ap_minutes
l2_non_ap_final_contribution = l2_non_ap_final_players_minutes / TOTAL_MINUTES_L2_FINAL

l2_non_ap_contribution = (l2_non_ap_playoff_contribution + l2_non_ap_regular_contribution + l2_non_ap_final_contribution)/3

l1_non_ap_players_minutes = TOTAL_MINUTES_L1 - l1_foreign_minutes - l1_total_adjusted_ap_minutes
l1_non_ap_contribution = l1_non_ap_players_minutes / TOTAL_MINUTES_L1

non_ap_contribution = (l1_non_ap_contribution + l2_non_ap_contribution)/2

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
pie_labels[0].set_position((x0 - 0.2, y0 + 0.1))

x1, y1 = auto_txts[1].get_position()
pie_labels[1].set_position((x1 - 0.1, y1 + 0.1))

x2, y2 = auto_txts[2].get_position()
pie_labels[2].set_position((x2 + 0.35, y2 + 0.1))

bottom = 1
width = 0.2

# bar chart
# ap_params = adjusted_ap['Adjusted Total Minutes'].apply(lambda x: x / total_adjusted_ap_minutes).to_list()
ap_params = ap_all['Total Minutes'].apply(lambda x: x / total_ap_minutes).to_list()
ap_labels = ap_all.index.to_list()
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
    value = ap_all.loc[label, 'Total Minutes']
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
