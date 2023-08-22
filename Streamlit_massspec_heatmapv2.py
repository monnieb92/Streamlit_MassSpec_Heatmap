#!/bin/python3
# use subprocess if seaborn isn't installing via requirements.txt
#import subprocess 
#subprocess.call(['pip', 'install', 'seaborn'])

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LogNorm


uploaded_file = st.sidebar.file_uploader("Upload your input csv file", type=["csv"])
st.write('This is the path to the csv file from Spectral Counts', uploaded_file)

fontsize = st.number_input('Font size of spectral counts',value = 8)
st.write('Font size for the annotations aka spectral counts, default 8', fontsize)

fontsize_tick = st.number_input('Font size for y-axis',value = 8)
st.write('Font size for the y-axis, default 8', fontsize_tick)

rows = st.number_input('Nunber of rows',value = 93)
st.write('Number of rows aka proteins to include minus 1 (python index starts at 0 instead of 1), default 93)', rows)
## argument of size of the figure; You may have to troubleshoot the more proteins/rows you add


color = st.text_input('Pick A ColorMap: https://seaborn.pydata.org/tutorial/color_palettes.html', 'vlag')
st.write('Color map, default is vlag', color)

default_width = 6
default_height = 16
width= st.number_input('Plot size width, default is 6 ',value=default_width)
st.write(width)
height= st.number_input('Plot size height, default 16' ,value=default_height)
st.write(height)
                        
location=st.number.input('Location of spectral count columns for the heatmap, default 9:15 (This assumes ParentalA, ParentalB, ParentalC, SampleA, SampleB, SampleC)',value='9:15')
st.write(location)


# Read CSV file
df = pd.read_csv(uploaded_file)
print("Top 10 rows of the csv file")
print(df.head(10))

# Extract GeneName
df['GeneName'] = df.iloc[:,3].str.extract(r'GN=(\w+)')

# Prepare heatmap data
dfheatmapv1 = df['GeneName'].to_frame(name='GeneName')
loc_start, loc_end = map(int, location.split(':'))
dfheatmap = df.iloc[:, loc_start:loc_end]  # Select columns 9 to 14
dfheatmap = pd.concat([dfheatmapv1,dfheatmap], axis = 1)
print("Top 5 rows of the new concatenated data frame for the heatmap")
print(dfheatmap.head(5))
dfheatmap = dfheatmap.iloc[0:rows]
## Set the GeneName column as the row names for each spectral count 
dfheatmap.set_index('GeneName', inplace=True)
print("Top 5 rows of the new df for heatmap with the rows labeled as GeneNames")
print(dfheatmap.head(5))
## Making any NAs into 0s 
dfheatmap_filled = dfheatmap.fillna(0)

# Plot heatmap
offset = 1e-1
## Offsetting the heatmap by 0.01 to help adjust the coloring in the heatmap because the logNorm of 0 is -inf
dfheatmap_offset = dfheatmap_filled + offset
## figure heatmap size 
fig, ax = plt.subplots(figsize=[width,height])
## plotting heatmap with the offset df as the coloring because the logNorm of 0 is -inf, the annotated spectral counts as dfheatmap_filled (the actual # of spectral counts) and no decimal point fmt='.0f'; cmap is the coloring map/palette you chose or the default; linecolor is always white with a width of 0.5 between each heatmap square; performing the log normalization of the spectral counts for proper coloring  
p1 = sns.heatmap(dfheatmap_offset, fmt='.0f', annot=dfheatmap_filled, annot_kws={"size": fontsize, "weight": "bold"}, cmap=color, linecolor='white', linewidth='0.5', norm=LogNorm())
## adjust the size and boldness of the y-axis labeling aka the protein/Gene names 
ax.set_yticklabels(ax.get_yticklabels(), size=fontsize_tick, weight='bold') ## version 2 addition 
## Saving the final heatmap 
plt.savefig('heatmap.png')

st.pyplot()

save=st.download_button('PNG file name to save', data=open('heatmap.png','rb').read(), file_name='heatmap.png')
