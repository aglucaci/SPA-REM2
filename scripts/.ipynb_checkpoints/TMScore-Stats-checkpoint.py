# Imports
import re
import os
import sys
import pandas as pd
from tqdm import tqdm
import glob

inputCSV = os.path.join ("..",
                         "tables",
                         "TM_Align_Results.csv")

df = pd.read_csv(inputCSV)

#print(df.describe())

for col in df.columns:
    print(df[col].describe(), "\n")



df2 = df[df["Normalized_Average_TM_Score"] > 0.5]

print(df.shape)
print(df2.shape)

print(df2.shape[0]/df.shape[0])