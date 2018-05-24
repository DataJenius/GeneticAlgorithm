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

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
import pandas as pd


######################################################################################
# load data from our two tests
df1 = pd.read_pickle('results/random1/256per_100gens_4queens_random_most_solutions.pkl')
df2 = pd.read_pickle('results/evolution1/256per_100gens_4queens_evolution_most_solutions.pkl')
df3 = pd.read_pickle('results/couples2/256per_100gens_4queens_couples_most_solutions.pkl')
df4 = pd.read_pickle('results/harem1/256per_100gens_4queens_harem_most_solutions.pkl')

df3["solutions"].sum()
# combine our data
df1 = df1[['strategy','solutions']]
df2 = df2[['strategy','solutions']]
df3 = df3[['strategy','solutions']]
df4 = df4[['strategy','solutions']]
dfz=df1.append(df2).append(df3).append(df4)
dfz["solutions"] = dfz["solutions"].astype(float)

# plot it
mpl.style.use('seaborn')
mpl.rcParams.update({'font.size': 100})
my_pal = {"random": "#f97a89", "evolution": "#5eba66", "couples":"#4286f4", "harem":"#ae43e8"}
my_boxplot = sns.boxplot(x='strategy', y='solutions', data=dfz, palette=my_pal)
fig = my_boxplot.get_figure()
fig.set_size_inches(11, 8)
plt.title("Random v. Evolution v. Couples v. Harem", loc="center")
plt.ylabel("Solutions per Experiment")
plt.xlabel("100 experiments with 100 generations each")
fig.savefig("jojo.png") 
