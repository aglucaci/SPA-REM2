#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 05:46:32 2023

@author: alex
"""

import re
import os
import sys
from ete3 import Tree
import pandas as pd
from tqdm import tqdm

results = {}
count = 0

def parseName(name):
    parsed_name = name
    parsed_name = parsed_name.split("_")
    if "Node" in parsed_name[0]:
        parsed_name = parsed_name[0]
    else:
        parsed_name = "_".join(parsed_name[0:3])
    #end if
    return parsed_name
# end method

def fillDataFrame(df, name, label):
    # Find it in index
    # Short_Name of Chain_1:	Short_Name of Chain_2:
    #TaxaLabel_1_index = df['Short_Name of Chain_1:'].loc[lambda x: x==name].index
    #TaxaLabel_2_index = df['Short_Name of Chain_2:'].loc[lambda x: x==name].index
    #df["TaxaLabel_1"][TaxaLabel_1_index] = label.groups()[0]
    #df["TaxaLabel_2"][TaxaLabel_2_index] = label.groups()[0]
    for index, row in df.iterrows():
        if row["Short_Name of Chain_1:"] == name:
            try: 
                #df["TaxaLabel_1"][index] = label.groups()[0]
                df.loc[index, "TaxaLabel_1"] = label.groups()[0]
            except:
                #df["TaxaLabel_1"][index] = "Unlabelled"
                df.loc[index, "TaxaLabel_1"] = "Unlabelled"
            #end try
            
        elif row["Short_Name of Chain_2:"] == name:
            try: 
                #df["TaxaLabel_2"][index] = label.groups()[0]
                # Try using .loc[row_indexer,col_indexer] = value instead
                df.loc[index, "TaxaLabel_2"] = label.groups()[0]
            except:
                #df["TaxaLabel_2"][index] = "Unlabelled"
                df.loc[index, "TaxaLabel_2"] = "Unlabelled"
            #end try
        else:
            pass
        #end if
    #end for
    return df
# end method

# =============================================================================
# Main subroutine
# =============================================================================

input_csv = os.path.join("..", 
                         "tables", 
                         "TM_Align_Results_with_GeneticDistance-Complete.csv")

df = pd.read_csv(input_csv)

df["TaxaLabel_1"]    = ""
df["TaxaLabel_2"]    = ""
df["TaxaLabel_Pair"] = ""

print("# Grabbing labels and adding to dataframe")

t = Tree(os.path.join("..", 
                      "data",  
                      "mammalian_REM2_codons.SA.FilterOutliers.fasta.treefile.labelled"), format=1)

for node in tqdm(t.traverse("postorder")):
  # Do some analysis on node
  #print(node.name)
  # \{(.*?)\}
  label = ""
  label = re.search("{(.*?)}", node.name)
  name = parseName(node.name).split("{")[0]
  try: 
      #print(name, label.groups()[0])
      results[count] = {name: label.groups()[0]}
  except:
      #print(name, "Unlabelled")
      results[count] = {name:  "Unlabelled"}
  #end try
  count += 1
  df = fillDataFrame(df, name, label)
#end for


# SAVE OUTPUT -----------------------------------------------------------------
df["TaxaLabel_Pair"] = df["TaxaLabel_1"] + "_" + df["TaxaLabel_2"]

output_csv = os.path.join("..", 
                         "tables", 
                         'SPA-REM2-Complete-Test-2.csv')

print("# Saving data to:", output_csv)

df.to_csv(output_csv)

# =============================================================================
# Match them
# =============================================================================

print(results)