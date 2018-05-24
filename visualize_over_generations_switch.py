#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 22:16:01 2018

@author: joshwork

Compare different results to see which found the most solutions relative to each other

Displays the results via a Bokeh box and whiskers plot
"""

######################################################################################
# Import all needed dependencies
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file


######################################################################################
# load data from our two tests
df1 = pd.read_pickle('results/random2_switch/256per_100gens_4queens_switch_random_conflicts_over_generations.pkl')
df2 = pd.read_pickle('results/evolution2_switch/256per_100gens_4queens_switch_evolution_conflicts_over_generations.pkl')
df3 = pd.read_pickle('results/harem2_switch/256per_100gens_4queens_switch_harem_conflicts_over_generations.pkl')
df4 = pd.read_pickle('results/couples3_switch/256per_100gens_4queens_switch_couples_conflicts_over_generations.pkl')
df1 = df1.drop("gen", axis=1)
df2 = df2.drop("gen", axis=1)
df3 = df3.drop("gen", axis=1)
df4 = df4.drop("gen", axis=1)

# average all columns (experiments) for each row (generation)
df = pd.DataFrame([], columns=['random','evolution','couples','harem'])
df['random'] = df1.mean(axis=1)
df['evolution'] = df2.mean(axis=1)
df['harem'] = df3.mean(axis=1)
df['couples'] = df4.mean(axis=1)

# make Bokeh chart
colors_list = ['red','green','blue','purple']
legends_list = ['random','evolution','couples','harem']
jojo = range(1,101)
xs=[jojo,jojo,jojo,jojo]
ys=[df['random'],df['evolution'],df['couples'].iloc[1:],df['harem']]
p = figure(title="Number of Conflicts", plot_width=800, plot_height=500)
for (colr, leg, x, y ) in zip(colors_list, legends_list, xs, ys):
    my_plot = p.line(x, y, color= colr, line_width=2, legend=leg)
    my_plot = p.line(x, y, color= colr)    
p.xaxis.axis_label = 'Generation'
p.yaxis.axis_label = 'Average Conflicts over 100 Experiments'
p.legend.location = "bottom_right"
show(p)
