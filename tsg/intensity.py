import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# ['Gameweek', 'Match', 'Team', 'Total Pass', 'Completed Pass']
dfPrev = pd.read_excel("~/Documents/LearnPython/tsg2425/data/pass_completed_23_24.xlsx")
dfPrev = dfPrev.loc[dfPrev["Gameweek"] <= 34]
dfCurr = pd.read_excel("~/Documents/LearnPython/tsg2425/data/pass_completed_24_25.xlsx")

dfPrev = dfPrev[["Gameweek", "Completed Pass"]]
dfCurr = dfCurr[["Gameweek", "Completed Pass"]]

dfPrev = dfPrev.groupby(["Gameweek"]).sum()
dfCurr = dfCurr.groupby(["Gameweek"]).sum()

dfPrev = dfPrev.groupby(["Gameweek"]).sum()
dfCurr = dfCurr.groupby(["Gameweek"]).sum()

dfPrev["Completed Pass"] = dfPrev["Completed Pass"].apply(lambda x: x / 9)
dfCurr["Completed Pass"] = dfCurr["Completed Pass"].apply(lambda x: x / 9)

dfPrev["Rolling Average Intensity"] = dfPrev["Completed Pass"].rolling(4).mean()
dfCurr["Rolling Average Intensity"] = dfCurr["Completed Pass"].rolling(4).mean()

prev10 = dfPrev["Completed Pass"].head(10)
curr10 = dfCurr["Completed Pass"].head(10)

print(prev10)
print(prev10.mean())
print(curr10)
print(curr10.mean())

x = np.array(dfCurr.index)
yPrev = np.array(dfPrev["Rolling Average Intensity"])
yCurr = np.array(dfCurr["Rolling Average Intensity"])

fig, ax = plt.subplots(figsize = (16,9), layout='constrained')
ax.tick_params(axis='x')
ax.tick_params(axis='y')
ax.set_ylabel('Rata-rata Passing Sukses', size='14', labelpad=12)
ax.set_xlabel('Pekan', size='14')

title = "Perbandingan Intensitas Liga 1\nMusim 2023/24 dan Musim 2024/25"

plt.plot(x, yPrev, color = 'red', linestyle='dashed', linewidth=3)
plt.plot(x, yCurr, color = 'blue', linewidth=3)
ax.fill_between(x, yPrev, yCurr, where=yPrev>=yCurr, facecolor='red', alpha=0.6, interpolate=True)
ax.fill_between(x, yPrev, yCurr, where=yPrev<yCurr, facecolor='blue', alpha=0.6, interpolate=True)

plt.legend(["Musim 2023-24", "Musim 2024-25"], loc ="lower right")
title = ax.set_title(title)
title.set(fontsize='xx-large', fontweight='bold')
plt.show()
