#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:54:10 2018

@author: joshwork

Playing around with a genetic algorithm

Playing with the Eims
"""
######################################################################################
# Import all needed classes
from math import factorial
import pandas as pd
import random


######################################################################################
# Define the scope of the N-Queens problem
N_QUEENS = 4 # don't change this - the below code will NOT generalize
MAX_POSSIBLE_CONFLICTS = 10
ODDS_OF_MUTATION = 3 # odd are 1 in X we have a mutation with each new baby

######################################################################################
# Class to handle our fictional "Eim" creatures
class Eim:
    def __init__(self, dna):
        """ Create a new Eim creature based on generation count and DNA sequence """
        
        # set our object variables here
        self.dna = dna
        self.queens = None # hold all the queen positions as tuples
        self.conflicts = None # hold the number of conflicts between queens
        self.fitness = None # use the baseline of 8 in this static version
        
        # calculate the fitness of this Eim  (n-queens)
        self.count_conflicts(dna)
        
        
    def count_conflicts(self, dna):
        """ Count the number of conflicts for any Eim based on N-Queens """
        
        # hold our queen coordinates in a list of tuples
        self.queens = []
        for key, chromosome in enumerate(dna): 
            row = self.mapper(chromosome)            
            col = key+1
            self.queens.append((row,col))
            
        # check each of our queens for all possible conflicts
        self.conflicts = 0
        for queen in self.queens:
            self.conflicts += self.check_right(queen)
            self.conflicts += self.check_left(queen)
            # no need to check up or down since we only have 1 per column
            #self.conflicts += self.check_up(queen)
            #self.conflicts += self.check_down(queen)     
            self.conflicts += self.check_upright(queen)  
            self.conflicts += self.check_upleft(queen) 
            self.conflicts += self.check_downright(queen)             
            self.conflicts += self.check_downleft(queen)
        self.fitness = MAX_POSSIBLE_CONFLICTS-self.conflicts
        
        
    def check_right(self, queen):        
        """ Move queen right until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(col < N_QUEENS):
            col += 1
            if (row,col) in self.queens:
                return 1                      
        return 0
    
    
    def check_left(self, queen):        
        """ Move queen left until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(col > 0):
            col -= 1
            if (row,col) in self.queens:
                return 1
        return 0   
    
    
    def check_up(self, queen):        
        """ Move queen up until conflict or edge of board """
        row = queen[0]
        col = queen[1]     
        while(row < N_QUEENS):
            row += 1
            if (row,col) in self.queens:
                return 1
        return 0  


    def check_down(self, queen):        
        """ Move queen down until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(row > 0):
            row -= 1
            if (row,col) in self.queens:
                return 1
        return 0   


    def check_upright(self, queen):        
        """ Move queen up and right until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(row < N_QUEENS and col < N_QUEENS):
            row += 1
            col += 1            
            if (row,col) in self.queens:
                return 1
        return 0            


    def check_upleft(self, queen):        
        """ Move queen up and left until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(row < N_QUEENS and col > 0):
            row += 1
            col -= 1            
            if (row,col) in self.queens:
                return 1
        return 0 


    def check_downright(self, queen):        
        """ Move queen down and left until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(row > 0 and col < N_QUEENS):
            row -= 1
            col += 1            
            if (row,col) in self.queens:
                return 1
        return 0  
    
    
    def check_downleft(self, queen):        
        """ Move queen down and left until conflict or edge of board """
        row = queen[0]
        col = queen[1]
        while(row > 0 and col > 0):
            row -= 1
            col -= 1            
            if (row,col) in self.queens:
                return 1
        return 0     
    
        
    def mapper(self, chromosome):
        """ This is super hacky """
        """ JOJO: This will break once N != 4 queens """
        if(chromosome=='A'): return 4
        if(chromosome=='B'): return 3
        if(chromosome=='C'): return 2
        if(chromosome=='D'): return 1        
        return 0
        
        
    @classmethod
    def how_many(cls):
        """Prints the current population of Eims"""
        print("We have {:d} Eims.".format(cls.population))         


######################################################################################
# Class to handle a specific generation of Eim
class Generation:
        
    # class variables
    generation = 0 
    
    def __init__(self):
        """ Create a new generation of Eim """
        
        # set our object variables here
        Generation.generation += 1
        self.gen_num = Generation.generation
        self.population = 0 # how many Eims do we have?
        self.eims = [] # hold the Eim objects for this generation
        self.fitness_avg = 0 # hold the best fitness of a generation
        self.fitness_best = 0 # hold the best fitness of a generation       
        
    def add_eim(self, eim):
        """ Add an Eim object (creature) to this generation """
        self.population += 1
        self.eims.append(eim)
        
        
    def breed_all_combinations(self):
        """ Brute force all possible combinations from these parents  """
        """ No mutation here because we want a discrete count """
        
        # hold the children in the next generation
        next_gen = Generation()
        
        dad = None
        for mom in self.eims:
            
            # need 2 Eims to breed
            if(mom and dad):

                # break both parents into X and Y chromosome pairs
                momA = mom.dna[0]+mom.dna[1]
                momB = mom.dna[2]+mom.dna[3]                
                dadA = dad.dna[0]+dad.dna[1]
                dadB = dad.dna[2]+dad.dna[3]   

                # each pair of Eims could produce up to 8 unique offspring 
                # break DNA in half, each chunk can go into either half of the offspring, order matters                            

                # mom goes first
                baby1 = Eim(momA+dadA)
                next_gen.add_eim(baby1)
                baby2 = Eim(momA+dadB)
                next_gen.add_eim(baby2)
                baby3 = Eim(momB+dadA)
                next_gen.add_eim(baby3)
                baby4 = Eim(momB+dadB)
                next_gen.add_eim(baby4)  
                
                # dad goes first
                baby5 = Eim(dadA+momA)
                next_gen.add_eim(baby5) 
                baby6 = Eim(dadA+momB)
                next_gen.add_eim(baby6)                 
                baby7 = Eim(dadB+momA)
                next_gen.add_eim(baby7) 
                baby8 = Eim(dadB+momB)
                next_gen.add_eim(baby8)                 
                
            # behold the pansexual Eims!
            dad = mom
            
        print("Created new generation #", next_gen.gen_num)            
        print("Population: ",next_gen.population)
        print("Unique: ",next_gen.get_count_unique())        
        #print(next_gen.get_list_dna())        
        return next_gen       

    def breed_via_natural_selection(self):
        """ Breed our Eims based on the rules of natural selection  """
        
        # hold the children in the next generation
        next_gen = Generation()
        print("----- TIME TO BREED ------")
        print("This is Generation #", self.gen_num)            
        print("Eims with Unique DNA:",self.get_count_unique())              
        print("Population:",self.population)
        print("Clone Ratio:",round(((self.population-self.get_count_unique())/self.population)*100,2),"%")                

        # organize this generation into a dataframe
        eim_dna = []
        eim_fitness = []   
        for eim in self.eims:
            eim_dna.append(eim.dna)
            eim_fitness.append(eim.fitness)            
        df = pd.DataFrame(data={'dna':eim_dna,'fitness':eim_fitness})

        # normalize fitness as a % probability of breeding & set generation stats
        df["fitness_prob"]=df["fitness"]/sum(df["fitness"])
        self.fitness_avg = df["fitness"].mean()
        self.fitness_best = df["fitness"].max()
        print("Best Fitness:", self.fitness_best)          
        print("Avg Fitness:", self.fitness_avg)          
        
        # select two different parents from our population based on fitness_prob and make some fresh baby dna
        # make babies until we get to replacement population
        # keep track of avg fitness and best fitness in this generation
        i = 0
        fitness = []
        while(i < 56):
            i+=1
            parents = df.sample(n=2, replace=False, weights=df["fitness_prob"],random_state=42)
            baby_dna = self.breed_via_natural_selection_generate_new_dna(parents['dna'].iloc[0],parents['dna'].iloc[1])
            baby = Eim(baby_dna)
            next_gen.add_eim(baby)
            fitness.append(baby.fitness)
            if(baby.fitness > next_gen.fitness_best):
                next_gen.fitness_best = baby.fitness
        next_gen.fitness_avg = sum(fitness) / float(len(fitness))
        
        # show some stats
        fitness_change = next_gen.fitness_avg-self.fitness_avg
        if(fitness_change > 0):
            print("Generation Improvement: ",fitness_change)
        else:
            print("We did worse: ",fitness_change)            
        return next_gen
    
    
    def breed_via_natural_selection_generate_new_dna(self, mom, dad):
        """ Generate baby Eims DNA based on the rules of natural selection  """    
        
        # break both parents into A and B chromosome pairs
        mom = [mom[0]+mom[1],mom[2]+mom[3]]
        dad = [dad[0]+dad[1],dad[2]+dad[3]]
        
        # pick a random chromosome from both parents
        mom_chromosome = random.choice(mom)
        dad_chromosome = random.choice(dad) 
        
        # order the chromosomes at random
        if(random.randint(1,2)==1):
            baby_dna = mom_chromosome+dad_chromosome
        else:
            baby_dna = dad_chromosome+mom_chromosome                

        # do we have a mutation?
        # if so, randomly pick one of the 4 letters and randomly replace it
        # note: 1 in 16 probability of mutation resulting in same DNA we started with
        #if(random.randint(1,ODDS_OF_MUTATION)==1):
        if(1==1):
            #print("~~~~~~MUTATION~~~~~~")
            replace = ['A','B','C','D']
            i = random.randint(0,3)
            j = random.randint(0,3)            
            baby_dna = list(baby_dna)
            baby_dna[i]=replace[j]
            baby_dna = "".join(baby_dna)
        return baby_dna
        

            
    def get_count_unique(self):
        """ Get a count of the members of this generation with unique DNA """
        return len(set(self.get_list_dna()))  
                            
    def get_list_dna(self):
        """ Get a list of the DNA of all members of this generation """
        my_list = []
        for eim in self.eims:
            my_list.append(eim.dna)
        return sorted(my_list) 
    


######################################################################################
# create our first generation
gen1 = Generation()

# create our adam and eve
adam = Eim('BBDD')
eve = Eim('CCAA')

# add to the first generation
gen1.add_eim(adam)
gen1.add_eim(eve)

# see what happens if we breed ALL combinations
# we get 8 unique children in the first iteration
gen2 = gen1.breed_all_combinations()

# grandchildren
# by this point we have a population of 56, but only 16 are unique
# we are just playing with legos at this point
gen3 = gen2.breed_all_combinations()
#print(sorted(set(gen3.get_list_dna())))

# can we get there starting with 56 population?
print("---- START EVOLVING ----")
gen4 = gen3.breed_via_natural_selection()
gen5 = gen4.breed_via_natural_selection()
gen6 = gen5.breed_via_natural_selection()

# how do we loop this bitch?
i = 0
tmp = gen6
while(i < 1000):
    i+=1
    tmp = tmp.breed_via_natural_selection()
    #if(tmp.fitness_best==MAX_POSSIBLE_CONFLICTS):
    #    break
    
for eim in tmp.eims:
    if(eim.conflicts==0):
        print(eim.dna)    
        print(eim.conflicts)    
        print(eim.queens)

"""
for eim in gen3.eims:
    print(eim.conflicts)
"""
