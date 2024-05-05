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


inputCSV = os.path.join("..", 
                         "tables", 
                         'SPA-REM2-Complete-Test-2-Adjusted.csv')

def GeneratePlot(species, YAxis, YAxisTitle):
    global df
    species_df = df[(df.TaxaLabel_1 == species) | (df.TaxaLabel_2 == species)]

    source = species_df.copy()

    source = source.dropna() # df.dropna()

    chart = alt.Chart(source, title=species).mark_circle(size=20, 
                                                          opacity=1.0, 
                                                          stroke='black', 
                                                          strokeWidth=0.5).encode(
        x=alt.X('TN93', title='TN93', scale = alt.Scale(type= 'linear')),
        y=alt.Y(YAxis, title=YAxisTitle, scale = alt.Scale(type= 'linear')),
        color = alt.Color("AdjustedTaxaLabel_Pair", 
                          legend=alt.Legend(title='Color legend'), 
                          )
    ).properties(
        width=1200,
        height=800
    )

    # Regression line
    regression = chart.transform_regression(
        'TN93',
        YAxis,
        method='linear',
        groupby=["AdjustedTaxaLabel_Pair"],
        as_=['TN93', YAxis],
    ).mark_line().encode(
        x='TN93:Q',
        y=YAxis+':Q',
        color=alt.Color('AdjustedTaxaLabel_Pair', legend=None)
    )
    
    # Calculate regression statistics
    regression_stats = chart.transform_regression(
        'TN93',
        YAxis,
        method='linear',
        as_=['TN93', YAxis],
        groupby=["AdjustedTaxaLabel_Pair"],
        params=True
    ).transform_calculate(
        r_squared='format(datum.rSquared, ".4f")',
        slope='format(datum.coef[1], ".4f")',
        intercept='format(datum.coef[0], ".4f")',
    )
    cmap = 'AdjustedTaxaLabel_Pair'
    
    # Add annotation for R-squared
    r_squared_annotation = regression_stats.mark_text(
        align='right',
    ).encode(
        x=alt.value(500),
        y=alt.value(20),
        text=alt.Text('slope:N'),
        color=alt.Color(cmap, legend=None)
    )
    
    # Combine charts
    outputFilenamePNG = 'view-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.png'
    outputFilenameSVG = 'view-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.svg'
    
    chart = alt.layer(chart, regression, r_squared_annotation).properties(
        width=600,
        height=400
    ).configure_legend(labelLimit=150).resolve_scale(color='independent')
    
    chart.save(outputFilenamePNG, scale_factor=2)
    chart.save(outputFilenameSVG, scale_factor=2)
#end method


def marginalPlot(species, YAxis, YAxisTitle):
    global df
    species_df = df[(df.TaxaLabel_1 == species) | (df.TaxaLabel_2 == species)]
    source = species_df.copy()
    source = source.dropna() # df.dropna()
    
    base = alt.Chart(source)
    base_bar = base.mark_bar(opacity=0.7, binSpacing=0)
    cmap = 'AdjustedTaxaLabel_Pair'

    width, height = 600, 400
    
    points = base.mark_circle(size=20, opacity=1.0, stroke='black', strokeWidth=0.5).encode(
        alt.X("TN93"),
        alt.Y(YAxis, title=YAxisTitle),
        color=alt.Color(cmap, legend=alt.Legend(title='Color legend'))
    ).properties(
        width=width,
        height=height,
        title=species
    )
    
    top_hist = (
        base_bar
        .encode(
            alt.X("TN93")
                # when using bins, the axis scale is set through
                # the bin extent, so we do not specify the scale here
                # (which would be ignored anyway)
                .bin(maxbins=20).stack(None).title(""),
            alt.Y("count()").stack(None).title(""),
            alt.Color(cmap, legend=None),
        )
        .properties(height=60, 
                    width=width)
    )
    
    right_hist = (
        base_bar
        .encode(
            alt.Y(YAxis)
                .bin(maxbins=20)
                .stack(None)
                .title(""),
            alt.X("count()").stack(None).title(""),
            alt.Color(cmap, legend=None),
        )
        .properties(width=60, 
                    height=height)
    )
    
    # Combine charts
    outputFilenamePNG = 'view-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.png'
    outputFilenameSVG = 'view-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.svg'
    
    chart = top_hist & (points | right_hist)

    #chart = chart.configure_legend(labelLimit=150).resolve_scale(color='independent')

    chart = chart.configure_legend(labelLimit=150).resolve_scale(
        #x='shared',  # Ensure X-axes are aligned and shared between scatter and top histogram
        #y='shared',  # Ensure Y-axes are aligned and shared between scatter and right histogram
        color='independent'
)
    
    chart.save(outputFilenamePNG, scale_factor=2)
    chart.save(outputFilenameSVG, scale_factor=2)

df = pd.read_csv(inputCSV)

for species in ["Carnivora", "Perissodactyla", "Glires", "Artiodactyla", "Eulipotyphla", "Primates"]:
    print(f"# Generating chart for {species}")
    marginalPlot(species, "Normalized_Average_TM_Score", "TM Score (Averaged)")

    
# =============================================================================
# End of file
# =============================================================================
