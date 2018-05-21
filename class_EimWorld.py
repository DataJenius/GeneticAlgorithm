#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 08:22:38 2018

@author: joshwork

These classes contain everything needed to breed and measure eims using 
the "random" and "natural selection" methods
"""

######################################################################################
# Import all needed dependencies
import random
import string
from math import factorial

######################################################################################
# Class to manage each individual experiment
# Each experiment contains multiple generations
class Experiment:
    def __init__(self, method, fitness_goal, generations):        
        """ Initialize a new experiment in Eim World """
        
        ### These variables are set when we initialize a new experiment ###
        self.init={}
        self.init["method"] = method                # random | evolution
        self.init["fitness_goal"]= fitness_goal     # max | min | switch - are we trying to min or max the number of queen conflicts?        
        self.init["generations"] = generations      # number of generations to spawn

        ### These experiment settings are manually set by the scientist experimenting ###   
        self.settings={}
        self.settings["n_queens"] = 8               # how many queens? must be even number so we get even chromosome pairs
        self.settings["eims_per_generation"] = 5    # how many eims should each generation contain?
        # adam
        # max conflicts
        # etc

        ### These experiment settings are held in state and can change mid experiment ###   
        self.state={}
        self.state["fitness_goal"] = self.init["fitness_goal"]               # reference this instead of self.init["fitness"] so we can switch goals mid experiment        
        self.state["DNA_options"] = self.get_dna_options()                   # all DNA chromosomes we are allowed to use in this experiment
        self.state["max_queen_conflicts"] = self.get_max_queen_conflicts()   # the maximum possible number of queen conflicts in this experiment        
        

        # TODO
        # JOJO
        # enforce n-queens limit and raise error if not even
        # limit to 26 because of chromosome size
        
        
        ### Call one of our experiment methods ###
        if(self.init["method"]=='random'):
            self.experiment_random()
            
        
    def experiment_random(self):
        """ Run a random experiment based on randomly generated eims """
        
        # loop through all needed generations...
        print("Run a random experiment!")        
        gen = Generation(self, 'random')  
        
        
    def get_dna_options(self):
        """ Get a list of all valid DNA chromosomes based on experiment settings """
        i = 0
        allowed = []
        for chromosome in list(string.ascii_uppercase):
            i += 1
            allowed.append(chromosome)
            if(i >= self.settings["n_queens"]):
                break
        return(allowed)     
        
        
    def get_max_queen_conflicts(self): 
        """ Get the maximum number of conflicts based on n-queens """
        n = self.settings["n_queens"]
        r = 2
        return((factorial(n)/(factorial(r)*factorial(n-r)))*2) # multiply by 2 because we count all conflicts in both directions
        
                
        

######################################################################################
# Class to manage each individual generation
# Each generation contains multiple eims
class Generation:
    def __init__(self, experiment, gentype):          
        """ Create a new generation of eims """
        self.parent = experiment    # hold experiment as parent
        
        ### method allows for weird starter generations for evolution

        # Generate a random generation  
        if(gentype=='random'):
            self.create_generation_by_random(experiment)
        
        
    def create_generation_by_random(self, experiment):
        """ Make a generation based on random eims """
        print("Make a generation full of random eims!")
        
        params = {"eimtype":'random'}
        baby = Eim(self,params)
        print("DNA",baby.dna)
        print("CONFLICTS",baby.conflicts)
        print("FITNESS",baby.fitness)
        print("QUEENS",baby.queens)
        print("IS SOLUTION",baby.is_solution)        

        
        
######################################################################################
# Class to manage each individual eim
class Eim:    
    def __init__(self, generation, params):    
        """ Create a new individual eim """
        # all eims share these variables
        self.parent = generation    # hold generation as parent
        self.dna = None             # hold DNA of the eim
        self.conflicts = None       # hold number of queen conflicts for this eim
        self.fitness = None         # hold our fitness score here
        self.queens = []            # hold our queen coordinates in a list of tuples
        self.is_solution = None     # 1 if perfection, 0 otherwise
        
        # these variables must be filled in specific functions where applicable
        self.mom = None
        self.dad = None
        self.breed_method = None
        self.is_mutant = None
        
        # Make a random eim
        if(params["eimtype"]=='random'):
            new_dna = self.get_eim_dna_by_random()      # get our random DNA
            self.create_eim_from_dna(new_dna)           # create eim from DNA
            return None


    def get_eim_dna_by_random(self):
        """ Create a totally random eim dna """
        i = 0
        new_dna = ""
        while(i < self.parent.parent.settings["n_queens"]):
            i += 1
            r = random.randint(0,len(self.parent.parent.state["DNA_options"])-1)
            new_dna = new_dna + self.parent.parent.state["DNA_options"][r]
        return(new_dna)            
        
        
    def create_eim_from_dna(self, dna):
        """ Once we have the final eim DNA run this function to complete the object """
        self.dna = dna
        self.determine_fitness()
    
    
    def determine_fitness(self):
        """ Determine the fitness of an eim based on final DNA """
        # hold our queen coordinates in a list of tuples
        for key, chromosome in enumerate(self.dna): 
            row = key+1            
            col = self.map_chromosome_to_column(chromosome)            
            self.queens.append((row,col))
             
        # check each of our queens for all possible conflicts
        self.conflicts = 0
        for queen in self.queens:
            # no need to check left or right since we only have 1 queen per row
            #self.conflicts += self.determine_queen_conflicts(queen,'R')
            #self.conflicts += self.determine_queen_conflicts(queen,'L')            
            self.conflicts += self.determine_queen_conflicts(queen,'U')
            self.conflicts += self.determine_queen_conflicts(queen,'D')
            self.conflicts += self.determine_queen_conflicts(queen,'UR') 
            self.conflicts += self.determine_queen_conflicts(queen,'UL')             
            self.conflicts += self.determine_queen_conflicts(queen,'DR')
            self.conflicts += self.determine_queen_conflicts(queen,'DL')   
            

        # determine the fitness of the eim based on state fitness_goal  
        # assume 0 unless set otherwise
        self.fitness = 0
        self.is_solution = 0        
        
        # trying to minimize conflict
        if(self.parent.parent.state["fitness_goal"]=='min'):
            self.fitness = self.parent.parent.state["max_queen_conflicts"]-self.conflicts
            if(self.conflicts==0):
                self.is_solution = 1
               
        # trying to maximize conflict
        if(self.parent.parent.state["fitness_goal"]=='max'):
            self.fitness = self.conflicts
            if(self.conflicts==self.parent.parent.state["max_queen_conflicts"]):
                self.is_solution = 1


    def determine_queen_conflicts(self, queen, direction):        
        """ Move queen until we find a conflict or the edge of board """
        row = queen[0]
        col = queen[1]
        #print("OUR QUEEN:")
        #print(row, col) 
        #print("checking...")
        
        # check right
        if(direction=='R'):
            while(col < self.parent.parent.settings["n_queens"]):
                col += 1
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  
                
        # check left
        if(direction=='L'):
            while(col > 1):
                col -= 1
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check up
        if(direction=='U'):
            while(row < self.parent.parent.settings["n_queens"]):
                row += 1
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1 
                
        # check down
        if(direction=='D'):
            while(row > 1):
                row -= 1
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1   
                
        # check up-right
        if(direction=='UR'):
            while(row < self.parent.parent.settings["n_queens"] and col < self.parent.parent.settings["n_queens"]):
                row += 1
                col += 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check up-left
        if(direction=='UL'):
            while(row < self.parent.parent.settings["n_queens"] and col > 1):
                row += 1
                col -= 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check down-right
        if(direction=='DR'):
            while(row > 1 and col < self.parent.parent.settings["n_queens"]):
                row -= 1
                col += 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1   

        # check down-left
        if(direction=='DL'):
            while(row > 1 and col > 1):
                row -= 1
                col -= 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1                   
                
        # if we get here there was no conflict in this direction                
        #print("NO CONFLICT!")                    
        return 0              
    
                
    def map_chromosome_to_column(self, chromosome):
        """ Map the chromosomes (A, B, C...) to column numbers (1, 2, 3...) """
        col = self.parent.parent.state["DNA_options"].index(chromosome)
        return(col+1)
