#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:54:10 2018

@author: joshwork

Visualizing the results of the eims
"""

import pandas as pd

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file


# average min number of conflicts across all tests
master = pd.DataFrame()
for i in range(1,11):
    key = "Trial "+str(i)
    file = "data/100gen/test"+str(i)+".pkl"
    df = pd.read_pickle(file)
    master[key]=10-df["7avg_fitness"]
    print(i)
    
master['Average'] = master.mean(axis=1)
#print(master)


colors_list = ['blue', 'yellow']
legends_list = ['first', 'second']
jojo = range(1,101)
xs=[jojo, jojo]
ys=[master['Trial 1'], master['Average']]
p = figure(plot_width=300, plot_height=300)
for (colr, leg, x, y ) in zip(colors_list, legends_list, xs, ys):
    #my_plot = p.line(x, y, color= colr, legend= leg)
    my_plot = p.line(x, y, color= colr)
show(p)
