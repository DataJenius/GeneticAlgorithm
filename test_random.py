#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 08:23:24 2018

@author: joshwork

Breed and measure eims based on the "random" method
"""

######################################################################################
# Import all needed classes
from datetime import datetime
from class_EimWorld import Experiment

# run our experiment
experiment = Experiment(method="random", fitness_goal="max", generations=100)

