import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

df = pd.read_csv("~/Documents/LearnPython/tsg2425/data/ap.csv")
df = df[['Klub', 'AP minutes', '%']]
df = df.set_index('Klub')

print(df)

teams = df.index
idx = np.arange(len(teams))

minutes = df['AP minutes']
max_minutes = df['AP minutes'].max()
percentage = df['%']
adjusted_p = df['%'].apply(lambda x: max_minutes * x / 100)

# zscore = df.apply(stats.zscore)
# percentile = zscore.apply(lambda x: 100 - (stats.norm.sf(x) * 100))

fig, ax = plt.subplots(figsize=(8, 9), layout='constrained')
width = 0.4

m_rect = ax.barh(idx-width/2, minutes, width, color="green")
ax.bar_label(m_rect, padding=3)

p_rect = ax.barh(idx+width/2, adjusted_p, width, color="orange")
ax.bar_label(p_rect, labels=percentage.to_list(), padding=3)

ax.set_yticks(idx, teams)
ax.invert_yaxis()
ax.set_xlim(0, max_minutes + max_minutes * 10 / 100)

ax.legend(["Playing minutes", "% minutes contribution"])
title = ax.set_title("Academy Product in BRI Liga 1 2024/25")
title.set(fontsize='xx-large', fontweight='bold')

plt.show()
