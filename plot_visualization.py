# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 16:21:35 2022

@author: m3lo4
"""
import os
import pandas as pd
import plotly.express as px

os.chdir(r'C:\Users\m3lo4\OneDrive\GitHub\music-visualization')

# load my data set as a dataframe
df = pd.read_csv(r'note_counts.csv')

# examine the first few rows to figure out the structure
print(df.head(5))

#plot figure
fig = px.scatter(df, x="Piano_key_num", y="Composer",
           size="Count", color="Pitch", 
           hover_name="Note_w_octave", log_x=False, size_max=100
           )
fig.update_xaxes(showticklabels=False)

fig.show()

fig.write_image(r'visualized.png')

fig.write_html(r'visualized.html')
