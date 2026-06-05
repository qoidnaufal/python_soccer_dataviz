import pandas as pd
import numpy as np

df = pd.read_csv("./youth_data/2526/mop.csv")

# mop = df[["Name", "MoP"]].groupby(["Name"]).sum()
# mop.reset_index(inplace=True)
# mop["Name"] = mop["Name"].apply(lambda x: x.strip())

print(df)
