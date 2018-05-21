#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 19:27:05 2018

@author: Generate 100 tests 
"""
######################################################################################
# Import all needed classes
from datetime import datetime
from dj4queens import Generation, Eim, TimerMessage


######################################################################################
# create our first generation
startTime = datetime.now()
gen1 = Generation('Genesis')
print("==== start with Adam & Eve ====")
# create our adam and eve
adam = Eim('AABB')
eve = Eim('CCDD')

# add to the first generation
gen1.add_eim(adam)
gen1.add_eim(eve)

# get stats for first generation
gen1.get_gen_stats()
TimerMessage(startTime, 1)

######################################################################################
# create the 2nd generation by breeding ALL unique combinations of Adam and Eve
startTime = datetime.now()
gen2 = gen1.breed_all_combinations()
TimerMessage(startTime, 2)


#######################################################################################
# create the 3rd generation by breeding ALL unique combinations of the 2nd generation
startTime = datetime.now()
gen3 = gen2.breed_all_combinations()
TimerMessage(startTime, 3)

#######################################################################################
# continue X generations out - Natural Selection method
x = 3
gen4 = gen3
while x < 103:
#while gen4.min_conflicts > 0: 
    x += 1
    startTime = datetime.now()    
    gen4 = gen4.breed_natural_selection()
    TimerMessage(startTime, x)
 
    
print(Generation.df)
