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

#input_csv = os.path.join("..", 
#                         "tables", 
#                         'TM_Align_Results_with_GeneticDistance-Complete.csv')

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

# =============================================================================
# Compress categories
# =============================================================================

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
    #if row["TaxaLabel_Pair"].split("_")[0] == row["TaxaLabel_Pair"].split("_")[1]:
    #    continue
    #end if                          
    #if row["TaxaLabel_Pair"] = ""
    
    #if row["TaxaLabel_Pair"] in []:
    #    df.loc[index, "AdjustedTaxaLabel_Pair"] = ""
    #else:
    #    pass
    #end if
    
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
"""
source = df

chart1 = alt.Chart(source).mark_point(size=1).encode(
    x=alt.X('TN93', title='TN93', scale = alt.Scale(type= 'linear')),
    y=alt.Y('RMSD=', title='RMSD', scale = alt.Scale(type= 'linear')),
    #color = "Carnivora_Unlabelled"
    color = "AdjustedTaxaLabel_Pair"
)

Reg_Line = chart1.transform_regression('TN93', 'RMSD=',
                                      method="exp",
                                      groupby=["AdjustedTaxaLabel_Pair"]
)                    .mark_line().encode(color=alt.Color('AdjustedTaxaLabel_Pair', legend=None))


"""
"""
bar_args = {'opacity': .3, 'binSpacing': 0}

top_hist = base.mark_bar(**bar_args).encode(
    alt.X('sepalLength:Q')
          # when using bins, the axis scale is set through
          # the bin extent, so we do not specify the scale here
          # (which would be ignored anyway)
          .bin(maxbins=20, extent=xscale.domain)
          .stack(None)
          .title(''),
    alt.Y('count()').stack(None).title(''),
    alt.Color('species:N'),
).properties(height=60)

right_hist = base.mark_bar(**bar_args).encode(
    alt.Y('sepalWidth:Q')
          .bin(maxbins=20, extent=yscale.domain)
          .stack(None)
          .title(''),
    alt.X('count()').stack(None).title(''),
    alt.Color('species:N'),
).properties(width=60)

alt.Chart(iris).mark_point().encode(
    x='petalLength:Q',
    y='petalWidth:Q',
    color='species:N'
).properties(
    width=180,
    height=180
).facet(
    facet='species:N',
    columns=2
)


chart2 = alt.Chart(source).mark_point(size=2, color="black").encode(
    x=alt.X('TN93', title='TN93'),
    y=alt.Y('Normalized_Average_TM_Score', title='TM Score (Averaged)')
).facet(
    facet='AdjustedTaxaLabel_Pair',
    columns=6
)

"""

#print ("# Saving charts")
#chart1.save('AMES-REM2-TN93-RMSD.svg')

#(chart1 + Reg_Line).resolve_scale(color='independent').save('SPA-REM2-TN93-RMSD.svg')

#chart2.save('SPA-REM2-TN93-TMScore.svg')


# =============================================================================
# Primates
# =============================================================================

# titanic[(titanic["Pclass"] == 2) | (titanic["Pclass"] == 3)]

"""
primates = df[(df.TaxaLabel_1 == "Primates") | (df.TaxaLabel_2 == "Primates")]

source = primates

chart1 = alt.Chart(source).mark_point(size=1, opacity=0.8).encode(
    x=alt.X('TN93', title='TN93', scale = alt.Scale(type= 'linear')),
    y=alt.Y('RMSD=', title='RMSD', scale = alt.Scale(type= 'linear')),
    #color = "Carnivora_Unlabelled"
    color = alt.Color("AdjustedTaxaLabel_Pair", title='Color legend')
).properties(
    width=300,
    height=200
)

Reg_Line = chart1.transform_regression('TN93', 'RMSD=',
                                      method="exp",
                                      groupby=["AdjustedTaxaLabel_Pair"]
)                    .mark_line().encode(color=alt.Color('AdjustedTaxaLabel_Pair', legend=None))

print ("# Saving charts, separated by clade - Primates")
#chart1.save('AMES-REM2-TN93-RMSD.svg')

(chart1 + Reg_Line).configure_legend(labelLimit=0).resolve_scale(color='independent').save('AMES-REM2-TN93-RMSD-Primates.svg')
"""

def GeneratePlot(species, YAxis, YAxisTitle):
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
                          legend=alt.Legend(title='Color legend',
                                            padding=80, 
                                            offset=0))
    ).properties(
        width=800,
        height=600
    )

    #Reg_Line = chart1.transform_regression('TN93', YAxis,
    #                                        method="linear",
    #                                        groupby=["AdjustedTaxaLabel_Pair"]
    #)                                       .mark_line().encode(color=alt.Color('AdjustedTaxaLabel_Pair', 
    #                                                                            legend=None))


    # Regression line
    regression = chart.transform_regression(
        'TN93',
        YAxis,
        method='poly',
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
        r_squared='format(datum.rSquared, ".2f")',
        slope='format(datum.coef[1], ".2f")',
        intercept='format(datum.coef[0], ".2f")'
    )
    
    # Add annotation for R-squared
    r_squared_annotation = regression_stats.mark_text(
        align='left',
    ).encode(
        x=alt.value(20),
        y=alt.value(20),
        text=alt.Text('r_squared:N', title="R-squared"),
        color=alt.Color('AdjustedTaxaLabel_Pair', legend=None)
    )

    """
    (chart1 + Reg_Line +   r_squared_annotation).configure_legend(labelLimit=0).resolve_scale(color='independent').save('SPA-REM2-' + 
                                                                                               YAxis.replace(" ", "") +
                                                                                               '-TN93-' + 
                                                                                               species + 
                                                                                               '.png', 
                                                                                               scale_factor=2)
    """
    # Combine charts

    outputFilename = 'Density-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.png'

    density_x = chart.transform_density(
    density='TN93',
    groupby=['AdjustedTaxaLabel_Pair'],
    steps=200,
    extent=[0, 50],
    as_=['TN93', 'density']
    ).mark_area(orient='vertical', opacity=0.5).encode(
        y='density:Q',
    )
    
    density_y = chart.transform_density(
        density=YAxis,
        groupby=['AdjustedTaxaLabel_Pair'],
        steps=200,
        extent=[0, 26],
        as_=[YAxis, 'density']
    ).mark_area(orient='horizontal', opacity=0.5).encode(
        x='density:Q',
    )


    chart2 = alt.layer(alt.vconcat(density_x, alt.hconcat(chart, density_y)))
    
    chart2.properties(
        width=600,
        height=400
    ).configure_legend(labelLimit=0).resolve_scale(color='independent')
    
    #chart = alt.layer(chart, regression, r_squared_annotation).properties(
    #    width=600,
    #    height=400
    #).configure_legend(labelLimit=0).resolve_scale(color='independent')

    chart2.save(outputFilename, scale_factor=2)
#end method

print ("# Saving charts, separated by clade")

for species in ["Carnivora", "Perissodactyla", "Glires", "Artiodactyla", "Eulipotyphla", "Primates"]:
    #GeneratePlot(species, "RMSD=", "RMSD")
    print(f"# Generating chart for {species}")
    
    GeneratePlot(species, "Normalized_Average_TM_Score", "TM Score (Averaged)")
    #Normalized_Average_TM_Score', title='TM Score (Averaged)'
    
# =============================================================================
# End of file
# =============================================================================


"""
import altair as alt
from vega_datasets import data

source = data.cars.url

base = alt.Chart(source).encode(
    x='Miles_per_Gallon:Q',
    y='Acceleration:Q',
    color='Origin:N'
)

points = base.mark_point()

density_x = base.transform_density(
    density='Miles_per_Gallon',
    groupby=['Origin'],
    steps=200,
    extent=[0, 50],
    as_=['Miles_per_Gallon', 'density']
).mark_area(orient='vertical', opacity=0.5).encode(
    y='density:Q',
).properties(
    height=100
)

density_y = base.transform_density(
    density='Acceleration',
    groupby=['Origin'],
    steps=200,
    extent=[0, 26],
    as_=['Acceleration', 'density']
).mark_area(orient='horizontal', opacity=0.5).encode(
    x='density:Q',
).properties(
    width=100
)

density_x & (points | density_y)
"""
