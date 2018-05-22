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
import numpy as np
import seaborn as sns
import pandas as pd


######################################################################################
# load data from our two tests
df1 = pd.read_pickle('results/random1/256per_100gens_4queens_random_most_solutions.pkl')
df2 = pd.read_pickle('results/evolution1/256per_100gens_4queens_evolution_most_solutions.pkl')

# combine our data
df1 = df1[['strategy','solutions']]
df2 = df2[['strategy','solutions']]
dfz=df1.append(df2)
dfz["solutions"] = dfz["solutions"].astype(float)

# plot it
sns.boxplot(x='strategy', y='solutions', data=dfz)
plt.title("Random v. Evolution", loc="center")
plt.ylabel("Solutions per Experiment")
plt.xlabel("100 experiments with 100 generations each")
