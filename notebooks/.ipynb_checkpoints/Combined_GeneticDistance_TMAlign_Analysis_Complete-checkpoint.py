#!/usr/bin/env python
# coding: utf-8

# IMPORTS ---------------------------------------------------------------------

import os
import sys
import pandas as pd
#from sklearn.decomposition import PCA
#import matplotlib.pyplot as plt
#import os
from tqdm import tqdm
import numpy as np
#import altair as alt
#from vega_datasets import data
import warnings
warnings.filterwarnings('ignore')

#alt.data_transformers.enable('default', max_rows=None)

# DECLARES --------------------------------------------------------------------

df_tmalign = pd.read_csv(os.path.join("..", 
                                      "tables", 
                                      'TM_Align_Results.csv'), index_col=0)

df_tn93 = pd.read_csv(os.path.join("..", 
                                   "results", 
                                   "mammalian_REM2_codons.SA.FilterOutliers.fasta.SLAC.json.msa.fasta.dst"))

# HELPER FUNCTIONS ------------------------------------------------------------
def parseName(name):
    parsed_name = name
    parsed_name = parsed_name.split("_")
    
    if "Node" in parsed_name[0]:
        parsed_name = parsed_name[0].replace(".pdb", "")
    else:
        parsed_name = "_".join(parsed_name[0:3])
    #end if
    return parsed_name
#end method

# MAIN ------------------------------------------------------------------------

df_tmalign["Short_Name of Chain_1:"] = ""
df_tmalign["Short_Name of Chain_2:"] = ""

for index, row in tqdm(df_tmalign.iterrows()):
    id1 = row["Name of Chain_1:"]
    id2 = row["Name of Chain_2:"]
    
    # Parse names
    id1_parsed = parseName(id1)
    id2_parsed = parseName(id2)
    
    # dfmi.loc[:, ('one', 'second')]
    #df_tmalign.loc[:, ("Short_Name of Chain_1:", index)] = id1_parsed
    #df_tmalign.loc[:, ("Short_Name of Chain_2:", index)] = id2_parsed
    
    df_tmalign["Short_Name of Chain_1:"][index] = id1_parsed
    df_tmalign["Short_Name of Chain_2:"][index] = id2_parsed
#end for

df_tmalign["TN93"] = ""

for index, row in tqdm(df_tn93.iterrows()):
    id1_parsed = parseName(row["ID1"])
    id2_parsed = parseName(row["ID2"])
    distance =   row["Distance"]
    
    df = df_tmalign[df_tmalign["Short_Name of Chain_2:"] == id1_parsed]
    df2 = df[df["Short_Name of Chain_1:"] == id2_parsed]
    df_tmalign["TN93"][df2.index] = distance
    
    df = df_tmalign[df_tmalign["Short_Name of Chain_1:"] == id1_parsed]
    df2 = df[df["Short_Name of Chain_2:"] == id2_parsed]
    df_tmalign["TN93"][df2.index] = distance
        
    #break
    #print(df2.index[0])
    #break
# end for

# SAVE OUTPUT -----------------------------------------------------------------

output_csv = os.path.join("..", 
                         "tables", 
                         'TM_Align_Results_with_GeneticDistance-Complete.csv')

print("# Saving data to:", output_csv)

df_tmalign.to_csv(output_csv)

sys.exit(0)

# END OF FILE -----------------------------------------------------------------
