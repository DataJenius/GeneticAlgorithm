#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 22:16:01 2018

@author: joshwork
"""

######################################################################################
# Import all needed dependencies
import pandas as pd

# see random results
jojo = pd.read_pickle('results/random1/256per_100gens_4queens_random_solutions_over_generations.pkl')
print(jojo.head())
jojo = pd.read_pickle('results/random1/256per_100gens_4queens_random_conflicts_over_generations.pkl')
print(jojo.head())
jojo = pd.read_pickle('results/random1/256per_100gens_4queens_random_fitness_over_generations.pkl')
print(jojo.head())
jojo = pd.read_pickle('results/random1/256per_100gens_4queens_random_most_solutions.pkl')
print(jojo.head())

jojo["solutions"].sum()
# 20,026 after 100 iterations of 100, just about perfect