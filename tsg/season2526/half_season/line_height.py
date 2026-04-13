import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

LINE_HEIGHTS = {
    "Team": [
        "PERSIJA",
        "PERSIK Kediri",
        "PSM Makassar",
        "Malut United FC",
        "Bali United FC",
        "Dewa United Banten FC",
        "PERSIB",
        "PSIM Yogyakarta",
        "Bhayangkara Presisi Lampung FC",
        "Semen Padang FC",
        "Arema FC",
        "PERSEBAYA Surabaya",
        "PERSITA",
        "Borneo FC Samarinda",
        "PERSIS",
        "PERSIJAP",
        "PSBS Biak",
        "Madura United FC",
    ],
    "LineHeight": [
        42.0,
        38.5,
        37.8,
        37.5,
        37.2,
        37.1,
        37.1,
        37.0,
        36.5,
        36.2,
        36.1,
        35.5,
        34.9,
        34.7,
        34.5,
        33.3,
        33.2,
        33.2,
    ]
}

def plotWithTrendLine(df: pd.DataFrame):
    x = df.PPDA
    y = df.LineHeight
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    for name, limit, h in zip(df.index, p(x), y):
        if h >= limit:
            df.loc[df.index == name, "Color"] = "#cc241d"
        else:
            df.loc[df.index == name, "Color"] = "#fb4934"

    _, ax = plt.subplots(figsize=(9, 9), layout='constrained')
    ax.scatter(x, y, c=df.Color, s=150)
    ax.plot(x, p(x), color="#282828", linestyle="--", linewidth=1)

    ax.set_xlabel("PPDA\n", size=10, labelpad=12)
    ax.set_ylabel("\nRata-rata Ketinggian Aksi Bertahan", size=10, labelpad=12)

    ax.xaxis.set_inverted(True)

    left = ["PERSIJA", "PERSIK Kediri", "PSIM Yogyakarta", "Malut United FC", "PERSIS", "PERSITA", "Bhayangkara Presisi Lampung FC"]
    top = ["Bali United FC", "Dewa United Banten FC"]
    bot = ["PERSIB", "PSBS Biak"]

    for i, txt in enumerate(df.index):
        ax.annotate(
            txt,
            (x.iloc[i], y.iloc[i]),
            xytext=(-10, 0) if txt in left else (0, -12) if txt in bot else (0, 12) if txt in top else (10, 0),
            textcoords="offset points",
            color = 'black',
            ha='right' if txt in left else 'center' if txt in bot else 'center' if txt in top else 'left',
            va='center'
        )

    ax.annotate(
        f"{p}",
        (np.min(x), p(np.min(x))),
        color = 'black',
        ha = 'right',
        va = 'top',
        size = 6,
        rotation=35,
    )

    ax.set_title(
        "Perbandingan PPDA vs Rata-rata Ketinggian Aksi Bertahan",
        fontdict={
            "fontsize": 15,
        },
        pad=10.0
    )

    plt.show()

ppda = pd.read_excel("../../data2526/half_season/20260123_PPDA.xlsx")
ppda = ppda.set_index("Team")
lh = pd.DataFrame(LINE_HEIGHTS)
lh = lh.set_index("Team")

df = pd.concat([ppda, lh],axis=1)

plotWithTrendLine(df)
