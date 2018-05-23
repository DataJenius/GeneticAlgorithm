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
df1 = pd.read_pickle('results/random1/256per_100gens_4queens_random_fitness_over_generations.pkl')
df2 = pd.read_pickle('results/evolution1/256per_100gens_4queens_evolution_fitness_over_generations.pkl')
df3 = pd.read_pickle('results/harem1/256per_100gens_4queens_harem_fitness_over_generations.pkl')
df4 = pd.read_pickle('results/couples1/256per_100gens_4queens_couples_fitness_over_generations.pkl')

# average all columns (experiments) for each row (generation)
df = pd.DataFrame([], columns=['random','evolution','harem','couples'])
df['random'] = df1.mean(axis=1)
df['evolution'] = df2.mean(axis=1)
df['harem'] = df3.mean(axis=1)
df['couples'] = df4.mean(axis=1)



# make Bokeh chart
colors_list = ['red', 'green','blue','purple']
legends_list = ['random', 'evolution','harem','couples']
jojo = range(1,101)
xs=[jojo, jojo, jojo,jojo]
ys=[df['random'], df['evolution'],df['harem'],df['couples']]
p = figure(title="Random v. Evolution v. Harem", plot_width=800, plot_height=500)
for (colr, leg, x, y ) in zip(colors_list, legends_list, xs, ys):
    my_plot = p.line(x, y, color= colr, line_width=2, legend=leg)
    my_plot = p.line(x, y, color= colr)    
p.xaxis.axis_label = 'Generation'
p.yaxis.axis_label = 'Average Fitness over 100 Experiments'
p.legend.location = "bottom_right"
show(p)
