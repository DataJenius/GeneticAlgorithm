#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 08:22:38 2018

@author: joshwork

These classes contain everything needed to breed and measure eims using 
the "random" and "natural selection" methods with options
"""

######################################################################################
# Import all needed dependencies
from math import factorial
import pandas as pd
import random
import string


######################################################################################
# Class to manage each study
# Each study contains multiple experiments and compares two given methods
class Study:
    def __init__(self, iterations):  
    
        ### These experiment settings are manually set by the scientist experimenting ###   
        self.settings={}
        self.settings["methodA"] = 'evolution'          # random | evolution | harem
        self.settings["methodB"] = 'random'             # random | evolution | harem        
        self.settings["fitness_goal"]= 'min'            # max | min | switch - are we trying to min or max the number of queen conflicts? can also "switch" at halfway point of experiment      
        self.settings["generations"] = 100              # number of generations to spawn in each experiment
        self.settings["eims_per_generation"] = 5        # how many eims should each generation contain?
        self.settings["n_queens"] = 4                   # how many queens? must be even number so we get even chromosome pairs, max is 26 letters in alphabet       
        self.settings["DNA_adam"] = 'AABB'              # DNA for "Adam", len must equal n-queens
        self.settings["DNA_eve"] = 'CCDD'               # DNA for "Eve", len must equal n-queens
        self.settings["DNA_options"] = self.get_dna_options()                   # all DNA chromosomes we are allowed to use in this experiment
        self.settings["max_queen_conflicts"] = self.get_max_queen_conflicts()   # the maximum possible number of queen conflicts in this experiment        
                
        # we need to iterate through this....
        print("Run",iterations,"iterations")
        exp = Experiment(self, self.settings["methodA"], self.settings["fitness_goal"])
        #print(exp.generations_df)
        
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
# Class to manage each individual experiment
# Each experiment contains multiple generations
class Experiment:
    def __init__(self, study, method, fitness_goal):        
        """ Initialize a new experiment in Eim World """
                
        ### all experiments have these variables once completed
        self.parent = study    # hold study as parent    
        self.generations_df = pd.DataFrame([], columns=['gen','method','pop','solutions','conflicts','fitness','fitness_metric']) # hold all generations in single dataframe
        self.fitness_goal = fitness_goal # the static fitness goal of this experiment
        
        ### These experiment settings are held in state and can change mid experiment ###   
        self.state={}
        if(self.fitness_goal=='switch'):
            self.state["fitness_goal"] = 'min' # start with min, switch to max at halfway point
        else:            
            self.state["fitness_goal"] = self.fitness_goal            
        
        ### Call one of our experiment methods ###
        if(method=='random'):
            self.experiment_random()
            return None
        
        if(method=='evolution'):
            self.experiment_evolution()
            return None        
                 
    def add_to_generations_df(self, eims_df, gen_num, gen_method):        
        """ Set the dataframe of all eims in this generation """
        row = {'gen':gen_num,
               'method':gen_method,
               'pop':len(eims_df),
               'solutions':eims_df["is_solution"].sum(),
               'conflicts':eims_df["conflicts"].sum(),
               'fitness':eims_df["fitness"].sum(),
               'fitness_metric':self.state["fitness_goal"]}
        self.generations_df=self.generations_df.append(row, ignore_index=True)
        
        
    def experiment_evolution(self):
        """ Run a evolution experiment based on natural selection method """       
        print("Run an evolution experiment!")
        
        # start with Adam and Eve (generation -1)
        i = -1
        gen = Generation(self, 'genesis')
        self.add_to_generations_df(gen.eims_df, i, 'genesis')

        # all genetic combinations from Adam and Eve (generation 0)
        i = 0
        gen = Generation(self, 'genesis')
        self.add_to_generations_df(gen.eims_df, i, 'genesis')
        
        # start evolution loop at 1 and call this guy
        self.switch_fitness_metric(i)
        
        # pull these to parent class and do something with them...            
        print(self.generations_df)
        print(gen.eims_df)
                    
        
    def experiment_random(self):
        """ Run a random experiment based on randomly generated eims """
        print("Run a random experiment!")   
        
        # generate all needed generations, all random
        i = 0
        while(i < self.parent.settings["generations"]):
            i += 1
            gen = Generation(self, 'random')
            self.add_to_generations_df(gen.eims_df, i, 'random')
            self.switch_fitness_metric(i)
        
        
    def switch_fitness_metric(self, gen_num):
        """ Switch the fitness metric at the halfway point """
        if(gen_num > (self.parent.settings["generations"]/2)):
            if(self.fitness_goal=='switch'):
                self.state["fitness_goal"]='max'
                       
   
        
                
        

######################################################################################
# Class to manage each individual generation
# Each generation contains multiple eims
class Generation:
    def __init__(self, experiment, gentype, parents=[]):          
        """ Create a new generation of eims """
        
        ### all generations have these variables once completed
        self.parent = experiment    # hold experiment as parent
        self.eims_df = None         # hold all eims in single dataframe
        
        ### gentype allows for weird starter generations for evolution

        # Generate a random generation  
        if(gentype=='genesis'):
            self.create_generation_by_genesis()
            return None

        # Generate a random generation  
        if(gentype=='random'):
            self.create_generation_by_random()
            return None

       
    def create_generation_by_genesis(self):
        """ Make a generation from Adam and Eve """
        
        # generate eims df as we generate the eims themselves
        eim_dna = []
        eim_conflicts = []
        eim_fitness = []
        eim_is_solution = []     
        
        # create Adam
        params = {"eimtype":'dna',
                  "dna":self.parent.parent.settings["DNA_adam"]}
        baby = Eim(self,params)
        eim_dna.append(baby.dna)
        eim_conflicts.append(baby.conflicts)            
        eim_fitness.append(baby.fitness)
        eim_is_solution.append(baby.is_solution) 

        # create Eve
        params = {"eimtype":'dna',
                  "dna":self.parent.parent.settings["DNA_eve"]}
        baby = Eim(self,params)
        eim_dna.append(baby.dna)
        eim_conflicts.append(baby.conflicts)            
        eim_fitness.append(baby.fitness)
        eim_is_solution.append(baby.is_solution) 
        
        # create dataframe
        self.set_eim_df([eim_dna,eim_conflicts,eim_fitness,eim_is_solution]) # order matters                
          
        
    def create_generation_by_random(self):
        """ Make a generation full of random eims """
        
        # set eim parameters        
        params = {"eimtype":'random'}

        # generate eims df as we generate the eims themselves
        eim_dna = []
        eim_conflicts = []
        eim_fitness = []
        eim_is_solution = []        
        i = 0
        while(i < self.parent.parent.settings["eims_per_generation"]):
            i += 1
            baby = Eim(self,params)
            eim_dna.append(baby.dna)
            eim_conflicts.append(baby.conflicts)            
            eim_fitness.append(baby.fitness)
            eim_is_solution.append(baby.is_solution)                    
        self.set_eim_df([eim_dna,eim_conflicts,eim_fitness,eim_is_solution]) # order matters                

        
    def set_eim_df(self, lists):        
        """ Set the dataframe of all eims in this generation """
        self.eims_df = pd.DataFrame({'dna': lists[0],
                                     'conflicts': lists[1],
                                     'fitness': lists[2],
                                     'is_solution': lists[3]
                                    })
        self.eims_df = self.eims_df[['dna','conflicts','fitness','is_solution']]
        # add optional info here when present
        
        
        
        
        
        
######################################################################################
# Class to manage each individual eim
class Eim:    
    def __init__(self, generation, params):    
        """ Create a new individual eim """
        
        ### all eims have these variables once completed
        self.parent = generation    # hold generation as parent
        self.dna = None             # hold DNA of the eim
        self.conflicts = None       # hold number of queen conflicts for this eim
        self.fitness = None         # hold our fitness score here
        self.queens = []            # hold our queen coordinates in a list of tuples
        self.is_solution = None     # 1 if perfection, 0 otherwise
        
        # these variables must be filled in specific functions where applicable
        self.mom = None             # DNA of our mom
        self.dad = None             # DNA of our dad
        self.breed_method = None    # random breed method used
        self.mutated = None         # did this eim mutate during creation? 0/1
        
        # Make an eim from predefined DNA
        if(params["eimtype"]=='dna'):
            self.create_eim_from_dna(params["dna"])     # create eim from DNA
            return None
        
        # Make a random eim
        if(params["eimtype"]=='random'):
            new_dna = self.get_eim_dna_by_random()      # get our random DNA
            self.create_eim_from_dna(new_dna)           # create eim from DNA
            return None


    def get_eim_dna_by_random(self):
        """ Create a totally random eim dna """
        i = 0
        new_dna = ""
        while(i < self.parent.parent.parent.settings["n_queens"]):
            i += 1
            r = random.randint(0,len(self.parent.parent.parent.settings["DNA_options"])-1)
            new_dna = new_dna + self.parent.parent.parent.settings["DNA_options"][r]
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
            self.fitness = self.parent.parent.parent.settings["max_queen_conflicts"]-self.conflicts
            if(self.conflicts==0):
                self.is_solution = 1
               
        # trying to maximize conflict
        if(self.parent.parent.state["fitness_goal"]=='max'):
            self.fitness = self.conflicts
            if(self.conflicts==self.parent.parent.parent.settings["max_queen_conflicts"]):
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
            while(col < self.parent.parent.parent.settings["n_queens"]):
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
            while(row < self.parent.parent.parent.settings["n_queens"]):
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
            while(row < self.parent.parent.parent.settings["n_queens"] and col < self.parent.parent.parent.settings["n_queens"]):
                row += 1
                col += 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check up-left
        if(direction=='UL'):
            while(row < self.parent.parent.parent.settings["n_queens"] and col > 1):
                row += 1
                col -= 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check down-right
        if(direction=='DR'):
            while(row > 1 and col < self.parent.parent.parent.settings["n_queens"]):
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
        col = self.parent.parent.parent.settings["DNA_options"].index(chromosome)
        return(col+1)
