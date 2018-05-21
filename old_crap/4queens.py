#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:54:10 2018

@author: joshwork

Playing with the Eims- a genetic algorithm designed to solve the n-queens problem
"""

######################################################################################
# Import all needed classes
import pandas as pd
import random
import itertools
from datetime import datetime
from scipy.stats import truncnorm

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
    
######################################################################################
# Define the scope of the N-Queens problem
N_QUEENS = 4 # don't change this - the below code will NOT generalize
MAX_POSSIBLE_CONFLICTS = 10 # largest possible number of conflicts
ODDS_OF_MUTATION = 3 # odds are 1 in X we have a mutation with each new baby
EIMS_PER_GENERATION = 256 # max number of Eims to create in each generation

######################################################################################
# Class to handle our fictional "Eim" creatures
class Eim:
    def __init__(self, dna, mom='None',dad='None',breed_method=0, is_mutant=0):
        """ Create a new Eim creature based on generation count and DNA sequence """
        
        # set our object variables here
        self.dna = dna
        self.queens = None # hold all the queen positions as tuples
        self.conflicts = None # hold the number of conflicts between queens
        self.fitness = None # use the baseline of 8 in this static version
        self.mom = mom # hold mom
        self.dad = dad # hold data
        self.breed_method = breed_method # hold method used to breed this Eim
        self.is_mutant = is_mutant
        
        # calculate the fitness of this Eim  (n-queens)
        self.count_conflicts(dna)
        
        
    def count_conflicts(self, dna):
        """ Count the number of conflicts for any Eim based on N-Queens """
        
        # hold our queen coordinates in a list of tuples
        self.queens = []
        for key, chromosome in enumerate(dna): 
            row = key+1            
            col = self.mapper(chromosome)            
            self.queens.append((row,col))
            
        # check each of our queens for all possible conflicts
        self.conflicts = 0
        for queen in self.queens:
            # no need to check left or right since we only have 1 queen per row
            #self.conflicts += self.check_conflicts_for_single_queen(queen,'R')
            #self.conflicts += self.check_conflicts_for_single_queen(queen,'L')            
            self.conflicts += self.check_conflicts_for_single_queen(queen,'U')
            self.conflicts += self.check_conflicts_for_single_queen(queen,'D')
            self.conflicts += self.check_conflicts_for_single_queen(queen,'UR') 
            self.conflicts += self.check_conflicts_for_single_queen(queen,'UL')             
            self.conflicts += self.check_conflicts_for_single_queen(queen,'DR')
            self.conflicts += self.check_conflicts_for_single_queen(queen,'DL')            
        self.fitness = MAX_POSSIBLE_CONFLICTS-self.conflicts

    def check_conflicts_for_single_queen(self, queen, direction):        
        """ Move queen until we find a conflict or the edge of board """
        row = queen[0]
        col = queen[1]
        #print("OUR QUEEN:")
        #print(row, col) 
        #print("checking...")
        
        # check right
        if(direction=='R'):
            while(col < N_QUEENS):
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
            while(row < N_QUEENS):
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
            while(row < N_QUEENS and col < N_QUEENS):
                row += 1
                col += 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check up-left
        if(direction=='UL'):
            while(row < N_QUEENS and col > 1):
                row += 1
                col -= 1     
                #print(row, col)
                if (row,col) in self.queens:
                    #print("CONFLICT!")
                    return 1  

        # check down-right
        if(direction=='DR'):
            while(row > 1 and col < N_QUEENS):
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
                
    def mapper(self, chromosome):
        """ This is super hacky """
        """ Trying to use conventional chess notation """
        """ Can handle up to 8 queens as-is """
        if(chromosome=='A'): return 1
        if(chromosome=='B'): return 2
        if(chromosome=='C'): return 3
        if(chromosome=='D'): return 4        
        if(chromosome=='E'): return 5
        if(chromosome=='F'): return 6
        if(chromosome=='G'): return 7
        if(chromosome=='H'): return 8        
        return 0
   



######################################################################################
# Class to handle a specific generation of Eim
class Generation:
        
    # class variables
    generation = 0
    cumulative_population = 0
    df = pd.DataFrame(data={'1gen':[],
                            '2pop':[],
                            '3dna_unique_pop':[],
                            '4dna_diversity':[],
                            '5unique_chromosome_pairs':[],
                            '6best_fitness':[],
                            '7avg_fitness':[],
                            '8max_conflicts':[],
                            '9min_conflicts':[],
                            '10method':[],
                            '91critical_chromosomes':[],
                            '92perfect_eims':[],
                            '93perfect_eims_c':[],
                            '94avg_conflicts':[]})
    
    def __init__(self, method):
        """ Create a new generation of Eim """
        # set our object variables here
        Generation.generation += 1        
        self.gen_num = Generation.generation
        self.method = method # which method did we use to create this generation?
        self.population = 0 # how many Eims do we have in this generation?
        self.eims = [] # hold the Eim objects for this generation        
        self.eims_df = pd.DataFrame(data={'1gen':[],
                                          '2dna':[],
                                          '3conflicts':[],
                                          '4fitness':[],
                                          '5mom':[],
                                          '6dad':[],
                                          '7breed_method':[],
                                          'mutant':[]}) # hold Eim stats in dataframe for easy manipulation
        self.max_conflicts = 0 # hold the max number of conflicts in this generation
        self.min_conflicts = 0 # hold the min number of conflicts in this generation        
        self.fitness_avg = 0 # hold the average fitness of a generation
        self.fitness_best = 0 # hold the best fitness of a generation 
        self.dna = [] # hold all dna for this generation in a list
        self.chromosome_pairs = [] # hold all chromosome pairs for this generation
        self.stats = None # hold our generation stats once generated
        
        
    def add_eim(self, eim):
        """ Add an Eim object (creature) to this generation """
        Generation.cumulative_population += 1
        self.population += 1
        self.eims.append(eim)
        self.dna.append(eim.dna)
        self.chromosome_pairs.append(eim.dna[0]+eim.dna[1])        
        self.chromosome_pairs.append(eim.dna[2]+eim.dna[3])         
        df = pd.DataFrame(data={'1gen':[self.gen_num],
                                '2dna':[eim.dna],
                                '3conflicts':[eim.conflicts],
                                '4fitness':[eim.fitness],
                                '5mom':[eim.mom],
                                '6dad':[eim.dad],
                                '7breed_method':[eim.breed_method],
                                'mutant':[eim.is_mutant]})
        self.eims_df = self.eims_df.append(df)
        self.eims_df["8mating_prob"]=self.eims_df["4fitness"]/sum(self.eims_df["4fitness"])
        self.fitness_avg = self.eims_df["4fitness"].mean()
        self.fitness_best = self.eims_df["4fitness"].max()
        self.max_conflicts = self.eims_df["3conflicts"].max()        
        self.min_conflicts = self.eims_df["3conflicts"].min()  
        self.conflicts_avg = self.eims_df["3conflicts"].mean()               
        
        
    def get_gen_stats(self):
        """ Get key stats for this generation """
        
        # do we have the needed chromosomes yet?
        critical_chromosomes = 0
        chromosome_pairs = set(self.chromosome_pairs)
        if 'BD' in chromosome_pairs:
            critical_chromosomes += 1
        if 'AC' in chromosome_pairs:
            critical_chromosomes += 1
        if 'CA' in chromosome_pairs:
            critical_chromosomes += 1
        if 'DB' in chromosome_pairs:
            critical_chromosomes += 1
            
        # how many perfect eims have we created?            
        perfect_eims = len(self.eims_df.loc[self.eims_df['3conflicts']==0])
        perfect_eims_c = Generation.df["92perfect_eims"].sum()+perfect_eims
        #len(gen5.eims_df.loc[gen5.eims_df['3conflicts']==0])
        
        # set into a dataframe
        self.stats = pd.DataFrame(data={'1gen':[self.gen_num],
                                '2pop':[self.population],
                                '3dna_unique_pop':[len(set(self.dna))],
                                '4dna_diversity':[1-(self.population-len(set(self.dna)))/self.population],
                                '5unique_chromosome_pairs':[len(set(self.chromosome_pairs))],
                                '6best_fitness':[self.fitness_best],
                                '7avg_fitness':[self.fitness_avg],
                                '8max_conflicts':[self.max_conflicts],
                                '9min_conflicts':[self.min_conflicts],
                                '10method':[self.method],
                                '91critical_chromosomes':[critical_chromosomes],
                                '92perfect_eims':[perfect_eims],
                                '93perfect_eims_c':[perfect_eims_c],
                                '94avg_conflicts':[self.conflicts_avg]})
        Generation.df = Generation.df.append(self.stats)    

        
    def breed_all_combinations(self):
        """ Brute force all possible unique combinations from these parents  """
        """ No mutation here because we want a discrete count """
        
        # hold the children in the next generation
        next_gen = Generation('All Unique Combos')
        
        # need 2 Eims to breed - any Eim can be mom or dad
        # find all the possible combinations of the Eims in this generation             
        for combo in itertools.combinations(set(self.dna), 2):            
            
            # create all 8 possible offsping of all possible combinations
            for i in range(1,9):
                baby_dna = self.generate_baby_dna(combo[0], combo[1], i)
                baby = Eim(baby_dna, combo[0], combo[1], i)
                next_gen.add_eim(baby)      
        
        # generate stats for this generation and display them
        next_gen.get_gen_stats()  
        print("==== breed_all_combinations ====")
        print("Created new generation #", next_gen.gen_num)            
        print("Population: ",next_gen.population)
        print("DNA Diversity: ",next_gen.stats.iloc[0]["4dna_diversity"])        
        print("Unique Chromosome Pairs: ",next_gen.stats.iloc[0]["5unique_chromosome_pairs"])                      
        return next_gen  


    def breed_natural_selection(self, mutate=True):    
        """ Breed our Eims based on the rules of natural selection  """

        # hold the children in the next generation
        next_gen = Generation('Natural Selection')
        
        # number of babies created is normally distributed between 1 and 5
        # generate a list of 1,280 items each representing the number of babies for a pair to make
        num_babies_list = get_truncated_normal(mean=3, sd=.75, low=1, upp=5)
        num_babies_list = list(num_babies_list.rvs(1280))

        # select two different parents from our population based on fitness_prob and make some fresh baby dna
        # make babies until we get to EIMS_PER_GENERATION population
        while(next_gen.population < EIMS_PER_GENERATION):
            parents = self.eims_df.sample(n=2, 
                                replace=False, 
                                weights=self.eims_df["8mating_prob"],
                                random_state=42)
            
            # parents always create a single baby
            
            # all 8 methods of combination are equally likely
            method = random.randint(1, 8)
            baby_dna = self.generate_baby_dna(parents['2dna'].iloc[0],parents['2dna'].iloc[1], method)
                
            # do we mutate? if so how??
            is_mutant = 0
            if(mutate==True):
                    if(random.randint(1,ODDS_OF_MUTATION)==1):
                        is_mutant = 1                        
                        replace = ['A','B','C','D']
                        i = random.randint(0,3)
                        j = random.randint(0,3)            
                        baby_dna = list(baby_dna)
                        baby_dna[i]=replace[j]
                        baby_dna = "".join(baby_dna)

            # make a baby Eim
            baby = Eim(baby_dna, parents['2dna'].iloc[0],parents['2dna'].iloc[1], method, is_mutant)
            next_gen.add_eim(baby)    


        # generate stats for this generation and display them
        next_gen.get_gen_stats()  
        print("==== breed_natural_selection ====")
        print("Created new generation #", next_gen.gen_num)            
        print("Population: ",next_gen.population)
        print("DNA Diversity: ",next_gen.stats.iloc[0]["4dna_diversity"])        
        print("Unique Chromosome Pairs: ",next_gen.stats.iloc[0]["5unique_chromosome_pairs"])                      
        return next_gen  


    def breed_random_plan(self):
        """ Breed our Eims based on pure random selection """

        # hold the children in the next generation
        next_gen = Generation('Random Plan')
       
        # create random babies
        while(next_gen.population < EIMS_PER_GENERATION):
            i = 0
            baby_dna = ''
            while(i < N_QUEENS):
                i += 1
                baby_dna=baby_dna+self.random_gene()
            baby = Eim(baby_dna)
            next_gen.add_eim(baby)    

        # generate stats for this generation and display them
        next_gen.get_gen_stats()  
        print("==== breed_random_plan ====")
        print("Created new generation #", next_gen.gen_num)            
        print("Population: ",next_gen.population)
        print("DNA Diversity: ",next_gen.stats.iloc[0]["4dna_diversity"])        
        print("Unique Chromosome Pairs: ",next_gen.stats.iloc[0]["5unique_chromosome_pairs"])                      
        return next_gen  

    
    def generate_baby_dna(self,mom_dna,dad_dna,method):
        """ All possible combinations from these parents  """
        """ No mutation here, just the method 1 to 8 as defined """
        
        # break parents into 2 chromosomes each
        cm1 = mom_dna[0]+mom_dna[1]
        cm2 = mom_dna[2]+mom_dna[3]
        cd1 = dad_dna[0]+dad_dna[1]
        cd2 = dad_dna[2]+dad_dna[3] 

        # return DNA based on method - 8 possible combinations
                      
        # mom goes first
        if(method==1):
            return(cm1+cd1) # m 1 d 1
        elif(method==2):
            return(cm1+cd2) # m 1 d 2
        elif(method==3):
            return(cm2+cd1) # m 2 d 1            
        elif(method==4):
            return(cm2+cd2) # m 2 d 2                        

        # dad goes first        
        elif(method==5):
            return(cd1+cm1) # d 1 m 1      
        elif(method==6):
            return(cd1+cm2) # d 1 m 2
        elif(method==7):
            return(cd2+cm1) # d 2 m 1                       
        elif(method==8):
            return(cd2+cm2) # d 2 m 2                                

    def random_gene(self):
        chromosome = random.randint(1, 4)
        """ Just pick a random gene """
        if(chromosome==1): return 'A'
        if(chromosome==2): return 'B'
        if(chromosome==3): return 'C'
        if(chromosome==4): return 'D'      
        return 0



def TimerMessage(startTime, gen):
    print("------------------------------------------------------------------------------")
    print("Created generation "+str(gen)+" in "+str(datetime.now() - startTime)+" seconds")
    print("------------------------------------------------------------------------------")



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
#Generation.df.to_pickle("test1.pkl")
#print(Generation.df["92perfect_eims"].sum())
#print(Generation.df["7avg_fitness"].mean())
#print(gen5.eims_df)

"""
#######################################################################################
# pure random method - generate 100 generations
loop = Generation('Random Start')
x = 1
while x < 100:
#while gen5.min_conflicts > 0: 
    x += 1
    startTime = datetime.now()    
    loop = loop.breed_random_plan()
    TimerMessage(startTime, x)
Generation.df.to_pickle("random2.pkl")
"""