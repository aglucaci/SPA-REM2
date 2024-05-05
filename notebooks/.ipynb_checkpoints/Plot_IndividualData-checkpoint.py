#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 04:47:20 2023

@author: alex
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

print("# Reading data:", input_csv)

df = pd.read_csv(input_csv)
df = df[df.TaxaLabel_1 != "Unlabelled"]
df = df[df.TaxaLabel_2 != "Unlabelled"]
df = df[df.TaxaLabel_1 != ""]
df = df[df.TaxaLabel_2 != ""]
#Glires_
df = df[df.TaxaLabel_Pair != "Glires_"]

#print(set(df["TaxaLabel_Pair"].tolist()))
compressed_taxalabels = {}

print("# Compressing taxa labels")

# I want to loop over the taxalabels, and have the values be the adjusted names
for item in set(sorted(df["TaxaLabel_Pair"].tolist())):
    #print(item)
    #if item not in 
    #compressed_taxalabels
    # Check it both ways, then add it to the adjusted column
    #first  = item.split("_")[0]
    #second = item.split("_")[1]
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


def GeneratePlot(species, YAxis, YAxisTitle):
    species_df = df[(df.TaxaLabel_1 == species) | (df.TaxaLabel_2 == species)]
    source = species_df.copy()
    source = source.dropna() # df.dropna()
    TaxaLabelColumn = "AdjustedTaxaLabel_Pair"
    
    chart = alt.Chart(source, title=species).mark_circle(size=20, 
                                                          opacity=1.0, 
                                                          stroke='black', 
                                                          strokeWidth=0.5).encode(
        x=alt.X('TN93', title='TN93', scale = alt.Scale(type= 'linear')),
        y=alt.Y(YAxis, title=YAxisTitle, scale = alt.Scale(type= 'linear')),
        color = alt.Color(TaxaLabelColumn, 
                          legend=alt.Legend(title='Color legend',
                                            padding=80, 
                                            offset=0))
    ).properties(
        width=800,
        height=600
    )
    
    # Regression line
    regression = chart.transform_regression(
        'TN93',
        YAxis,
        method='linear',
        groupby=[TaxaLabelColumn],
        as_=['TN93', YAxis],
    ).mark_line(size=2).encode(
        x='TN93:Q',
        y=YAxis+':Q',
        color=alt.Color(TaxaLabelColumn, legend=None)
    )
    
    # Calculate regression statistics
    regression_stats = chart.transform_regression(
        'TN93',
        YAxis,
        method='poly',
        as_=['TN93', YAxis],
        groupby=[TaxaLabelColumn],
        params=True
    ).transform_calculate(
        r_squared='format(datum.rSquared, ".4f")',
        slope='format(datum.coef[1], ".4f")',
        intercept='format(datum.coef[0], ".4f")'
    ).mark_text(size=24,
        align='center',
        baseline='middle',
        dx=10
    ).encode(
        x='TN93',
        y=alt.value(50),
        text=alt.Text('r_squared:N', title="R-squared"),
        color=alt.Color(TaxaLabelColumn, legend=None)
    )
    
    """
    # Add annotation for R-squared
    r_squared_annotation = regression_stats.mark_text(
        align='left',
    ).encode(
        x=alt.value(20),
        y=alt.value(20),
        text=alt.Text('r_squared:N', title="R-squared"),
        color=alt.Color('TaxaLabel_Pair', legend=None)
    )
    """
    
    # Add the text box with the summary statistics
    text_box = regression_stats.mark_text(
        align='right',
        baseline='top',
        fontSize=12,
        color='black'
    ).encode(
        x='TN93:Q',
        y=YAxis,
        text=alt.Text("Slope: {'slope:N':.2f}, Intercept: {'intercept:N':.2f}, R²: {'r_squared:N':.2f}")  # Static text
    )
    
    # Combine charts
    outputFilename = 'INDV-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.png'
    
    chart = alt.layer(chart, regression, text_box).properties(
        width=600,
        height=400
    ).configure_legend(labelLimit=0).resolve_scale(color='independent')

    chart.save(outputFilename, scale_factor=2)
#end method

# MAIN ------------------------------------------------------------------------

#print ("# Saving charts, separated by clade")

for species in ["Carnivora", "Perissodactyla", "Glires", "Artiodactyla", "Eulipotyphla", "Primates"]:
    #GeneratePlot(species, "RMSD=", "RMSD")
    print(f"# Generating chart for {species}")
    GeneratePlot(species, "Normalized_Average_TM_Score", "TM-Score (Average)")
    #Normalized_Average_TM_Score', title='TM Score (Averaged)'
    
# =============================================================================
# End of file
# =============================================================================
