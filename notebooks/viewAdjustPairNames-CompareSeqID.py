#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 04:47:20 2023

@author: Alexander G Lucaci
"""

# =============================================================================
# Imports
# =============================================================================

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
alt.data_transformers.enable('default', 
                             max_rows=None)
from scipy import stats

# =============================================================================
# Declares
# =============================================================================

inputCSV = os.path.join("..", 
                         "tables", 
                         'SPA-REM2-Complete-Test-2-Adjusted.csv')

# =============================================================================
# Functions
# =============================================================================

def marginalPlot(species, YAxis, YAxisTitle, XAxis = "Seq_ID=n_identical/n_aligned="):
    global df
    species_df = df[(df.TaxaLabel_1 == species) | (df.TaxaLabel_2 == species)]
    source = species_df.copy()
    source = source.dropna() 
    
    # PLOT --- 
    base = alt.Chart(source)
    base_bar = base.mark_bar(opacity=0.7, binSpacing=0)
    cmap = 'AdjustedTaxaLabel_Pair'

    width, height = 600, 400
    
    points = base.mark_circle(size=20, opacity=1.0, stroke='black', strokeWidth=0.5).encode(
        alt.X(XAxis),
        alt.Y(YAxis, 
              title=YAxisTitle),
        color=alt.Color(cmap, legend=alt.Legend(title='Color legend'))
    ).properties(
        width=width,
        height=height,
        title=species
    )
    
    # Combine charts
    tag = "SeqID"
    outputFilenamePNG = tag + '-view-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.png'
    outputFilenameSVG = tag + '-view-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.svg'
    
    chart =  points
    
    chart = chart.configure_legend(labelLimit=150).resolve_scale(
        #x='shared',  # Ensure X-axes are aligned and shared between scatter and top histogram
        #y='shared',  # Ensure Y-axes are aligned and shared between scatter and right histogram
        color='independent'
    )
    
    chart.save(outputFilenamePNG, scale_factor=2)
    chart.save(outputFilenameSVG, scale_factor=2)

# end method

# =============================================================================
# Main
# =============================================================================

df = pd.read_csv(inputCSV)

for species in ["Carnivora", 
                "Perissodactyla", 
                "Glires", 
                "Artiodactyla", 
                "Eulipotyphla", 
                "Primates"]:
    
    print(f"# Generating chart for {species}")
    marginalPlot(species, 
                 "Normalized_Average_TM_Score", 
                 "TM Score (Averaged)")
    
    marginalPlot(species, "RMSD=", "RMSD")
# end for

    
# =============================================================================
# End of file
# =============================================================================
