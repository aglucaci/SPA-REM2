#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 04:47:20 2023

@author: Alexander G Lucaci
"""

import os
import sys
import pandas as pd

#from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#import os
from tqdm import tqdm
import numpy as np
import altair as alt
#from vega_datasets import data
alt.data_transformers.enable('default', max_rows=None)
from scipy import stats

input_csv = os.path.join("..", 
                         "tables", 
                         'SPA-REM2-Complete-Test-2.csv')

output_csv = os.path.join("..", 
                         "tables", 
                         'SPA-REM2-Complete-Test-2-Adjusted.csv')

print("# Reading data:", input_csv)

df = pd.read_csv(input_csv)
df = df[df.TaxaLabel_1 != "Unlabelled"]
df = df[df.TaxaLabel_2 != "Unlabelled"]
df = df[df.TaxaLabel_1 != ""]
df = df[df.TaxaLabel_2 != ""]
df = df[df.TaxaLabel_Pair != "Glires_"]

# =============================================================================
# Compress categories
# =============================================================================

compressed_taxalabels = {}

print("# Compressing taxa labels")

# I want to loop over the taxalabels, and have the values be the adjusted names
for item in set(sorted(df["TaxaLabel_Pair"].tolist())): 
    if len(compressed_taxalabels.keys()) == 0:
        compressed_taxalabels[item] = []
    else:
        first  = item.split("_")[0]
        second = item.split("_")[1]
        
        if "_".join([first, second]) in compressed_taxalabels.keys():
            continue
        elif "_".join([second, first]) in compressed_taxalabels.keys():
            compressed_taxalabels["_".join([second, first])].append("_".join([first, second]))
        else:
            compressed_taxalabels[item] = []
        #end if
    #end if
#end for

#I want to loop over the keys in compressed_taxalabels
df["AdjustedTaxaLabel_Pair"] = ""
print("# Creating adjusted taxa labels")

for index, row in df.iterrows():
    if row["TaxaLabel_Pair"] in compressed_taxalabels.keys():
        df.loc[index, "AdjustedTaxaLabel_Pair"] = row["TaxaLabel_Pair"]
    else:
        # not in the main keys it has to be in the subset
        # lookup
        for item in compressed_taxalabels.keys():
            if row["TaxaLabel_Pair"] in compressed_taxalabels[item]:
                df.loc[index, "AdjustedTaxaLabel_Pair"] = item
            #end if
        #end for
    #end if
#end for

# =============================================================================
# Visualize
# =============================================================================

df.to_csv(output_csv, index=False)
    
# =============================================================================
# End of file
# =============================================================================
