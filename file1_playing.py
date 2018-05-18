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

######################################################################################
# Define the scope of the N-Queens problem
N_QUEENS = 4

######################################################################################
# Class to handle our fictional "Eim" creatures
class Eim:
    def __init__(self, dna):
        """ Create a new Eim creature based on generation count and DNA sequence """
        
        # set our object variables here
        self.dna = dna
        self.queens = None # hold all the queen positions as tuples
        self.conflicts = None # hold the number of conflicts between queens

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
            
                            
    def get_list_dna(self):
        """ Get a list of the DNA of all members of this generation """
        my_list = []
        for eim in self.eims:
            my_list.append(eim.dna)
        return sorted(my_list) 
    
    def get_count_unique(self):
        """ Get a count of the members of this generation with unique DNA """
        return len(set(self.get_list_dna()))


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
gen2 = gen1.breed_all_combinations()

# grandchildren
# by this point we have a population of 56, but only 16 are unique
# we are just playing with legos at this point
gen3 = gen2.breed_all_combinations()
#print(sorted(set(gen3.get_list_dna())))

# a 4th generation of the "breed all" yields 440 pop, still 16 unique
gen4 = gen3.breed_all_combinations()
#print(sorted(set(gen4.get_list_dna())))

gen5 = gen4.breed_all_combinations()
gen6 = gen5.breed_all_combinations()
gen7 = gen6.breed_all_combinations()
gen8 = gen7.breed_all_combinations()
gen9 = gen8.breed_all_combinations()
gen10 = gen9.breed_all_combinations()
# here we can start the magic evolution

"""
print("JOJOOJO")
for eim in gen2.eims:
    print(eim.dna)
    print(eim.conflicts)  
    print(eim.queens)    
"""