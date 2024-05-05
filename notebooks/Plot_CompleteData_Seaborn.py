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
import altair as alt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

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
        r_squared='format(datum.rSquared, ".2f")',
        slope='format(datum.coef[1], ".2f")',
        intercept='format(datum.coef[0], ".2f")'
    )
    
    # Add annotation for R-squared
    r_squared_annotation = regression_stats.mark_text(color='black',
        align='left',
    ).encode(
        x=alt.value(20),
        y=alt.value(20),
        text=alt.Text('r_squared:N', title="R-squared"),
        #color=alt.Color('black', legend=None)
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

    outputFilenamePNG = 'SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.png'
    outputFilenameSVG = 'SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + '.svg'
    
    chart = alt.layer(chart, regression, r_squared_annotation).properties(
        width=600,
        height=400
    ).configure_legend(labelLimit=0).resolve_scale(color='independent')

    chart.save(outputFilenamePNG, scale_factor=2)
    chart.save(outputFilenameSVG, scale_factor=2)
#end method

def GeneratePlotPlt(species, YAxis, YAxisTitle, source, pair):
    # Fit a linear regression model
    model = LinearRegression()
    model.fit(source[['TN93']], source[YAxis])
    
    # Calculate the regression statistics
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(source[['TN93']], source[YAxis])
    
    # Create the scatter plot
    scatter_plot = alt.Chart(source).mark_point(color='blue').encode(
        x='TN93',
        y=YAxis
    )
    
    # Add the regression line
    regression_line = scatter_plot.transform_regression(
        'TN93', YAxis, method='linear'
    ).mark_line(color='red')
    
    # Prepare text for the summary statistics
    stats_text = f'Slope: {slope:.2f}, Intercept: {intercept:.2f}, R²: {r_squared:.2f}'
    
    # Add the text box with the summary statistics
    text_box = alt.Chart(source).mark_text(
        align='right',
        baseline='top',
        fontSize=12,
        color='black'
    ).encode(
        x='TN93:Q',
        y=YAxis,
        text=alt.value(stats_text)  # Static text
    )
    
    # Combine all the elements
    final_chart = (scatter_plot + regression_line + text_box).properties(
        width=600,
        height=400,
        title='Scatter Plot with Regression Line and Statistics'
    )
    
    outputFilenamePNG = 'NewPlt-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + "_" + pair + '.png'
    outputFilenameSVG = 'NewPlt-SPA-REM2-' + YAxis.replace(" ", "") + '-TN93-' + species + "_" + pair + '.svg'
    
    final_chart.save(outputFilenamePNG, scale_factor=2)
    final_chart.save(outputFilenameSVG, scale_factor=2)

# -----
def PlotSeaborn(YAxis, group):
    # Initialize the model
    model = LinearRegression()
    # Function to calculate regression statistics
    def regression_stats(group):
        model.fit(group[['TN93']], group[YAxis])
        y_pred = model.predict(group[['TN93']])
        return pd.Series({
            'slope': model.coef_[0],
            'intercept': model.intercept_,
            'r_squared': r2_score(group['y'], y_pred)
        })
    
    # Apply the function to each group
    stats = data.groupby('group').apply(regression_stats).reset_index()
    
    # Create the plot
    g = sns.lmplot(x='x', y='y', col='group', hue='group', data=data,
                   ci=None, palette='muted', height=4,
                   scatter_kws={"s": 50, "alpha": 1})
    
    # Add annotations with the regression stats
    for ax, group in zip(g.axes.flatten(), stats['group']):
        stat = stats[stats['group'] == group].iloc[0]
        annotation = f"Slope: {stat['slope']:.2f}\nIntercept: {stat['intercept']:.2f}\nR²: {stat['r_squared']:.2f}"
        ax.text(0.05, 0.95, annotation, transform=ax.transAxes, verticalalignment='top')
    plt.show()

# -----

def process(species, YAxis, YAxisTitle, col="AdjustedTaxaLabel_Pair"):
    species_df = df[(df.TaxaLabel_1 == species) | (df.TaxaLabel_2 == species)]
    source = species_df.copy()
    source = source.dropna() # df.dropna()
    
    for item in set(source[col].tolist()):
        holder = source[source[col] == item]
        #print(holder)
        GeneratePlotPlt(species, "Normalized_Average_TM_Score", "TM Score (Averaged)", holder, item)


print ("# Saving charts, separated by clade")

for species in ["Carnivora", "Perissodactyla", "Glires", "Artiodactyla", "Eulipotyphla", "Primates"]:
    print(f"# Generating chart for {species}")
    process(species, "Normalized_Average_TM_Score", "TM Score (Averaged)")


    
# =============================================================================
# End of file
# =============================================================================
