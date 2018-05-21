#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:54:10 2018

@author: joshwork

Playing with the Eims- a genetic algorithm designed to solve the 8-queens problem
"""

######################################################################################
# Import all needed classes
import pandas as pd
import random
import itertools
from datetime import datetime

######################################################################################
# Define the scope of the N-Queens problem
N_QUEENS = 8 # don't change this - the below code will NOT generalize
MAX_POSSIBLE_CONFLICTS = 28 # not sure yet...
ODDS_OF_MUTATION = 10 # odds are 1 in X we have a mutation with each new baby


######################################################################################
# Class to handle our fictional "Eim" creatures
class Eim:
    def __init__(self, dna, mom='None',dad='None',breed_method=0):
        """ Create a new Eim creature based on generation count and DNA sequence """
        
        # set our object variables here
        self.dna = dna
        self.queens = None # hold all the queen positions as tuples
        self.conflicts = None # hold the number of conflicts between queens
        self.fitness = None # use the baseline of 8 in this static version
        self.mom = mom # hold mom
        self.dad = dad # hold data
        self.breed_method = breed_method # hold method used to breed this Eim
        
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
                            '4clone_per':[],
                            '5unique_chromosome_pairs':[],
                            '6best_fitness':[],
                            '7avg_fitness':[],
                            '8max_conflicts':[],
                            '9min_conflicts':[]})
    
    def __init__(self):
        """ Create a new generation of Eim """
        # set our object variables here
        Generation.generation += 1
        self.gen_num = Generation.generation
        self.population = 0 # how many Eims do we have in this generation?
        self.eims = [] # hold the Eim objects for this generation        
        self.eims_df = pd.DataFrame(data={'1gen':[],
                                          '2dna':[],
                                          '3conflicts':[],
                                          '4fitness':[],
                                          '5mom':[],
                                          '6dad':[],
                                          '7breed_method':[]}) # hold Eim stats in dataframe for easy manipulation
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
        self.chromosome_pairs.append(eim.dna[4]+eim.dna[5])         
        self.chromosome_pairs.append(eim.dna[6]+eim.dna[7])  
        df = pd.DataFrame(data={'1gen':[self.gen_num],
                                '2dna':[eim.dna],
                                '3conflicts':[eim.conflicts],
                                '4fitness':[eim.fitness],
                                '5mom':[eim.mom],
                                '6dad':[eim.dad],
                                '7breed_method':[eim.breed_method]})
        self.eims_df = self.eims_df.append(df)
        self.eims_df["8mating_prob"]=self.eims_df["4fitness"]/sum(self.eims_df["4fitness"])
        self.fitness_avg = self.eims_df["4fitness"].mean()
        self.fitness_best = self.eims_df["4fitness"].max()
        self.max_conflicts = self.eims_df["3conflicts"].max()        
        self.min_conflicts = self.eims_df["3conflicts"].min()                
        
    def get_gen_stats(self):
        """ Get key stats for this generation """        
        self.stats = pd.DataFrame(data={'1gen':[self.gen_num],
                                '2pop':[self.population],
                                '3dna_unique_pop':[len(set(self.dna))],
                                '4clone_per':[(self.population-len(set(self.dna)))/self.population],
                                '5unique_chromosome_pairs':[len(set(self.chromosome_pairs))],
                                '6best_fitness':[self.fitness_best],
                                '7avg_fitness':[self.fitness_avg],
                                '8max_conflicts':[self.max_conflicts],
                                '9min_conflicts':[self.min_conflicts]})
        Generation.df = Generation.df.append(self.stats)    

        
    def breed_all_combinations(self):
        """ Brute force all possible combinations from these parents  """
        """ No mutation here because we want a discrete count """
        """ Note that after Adam and Eve we are just breeding children in the order they appear with the next child in the list """
        
        # hold the children in the next generation
        next_gen = Generation()
        
        # need 2 Eims to breed - any Eim can be mom or dad
        # find all the possible combinations of the Eims in this generation     
        for combo in itertools.combinations(self.dna, 2):            
            
            # create all 24 possible offsping of all possible combinations
            for i in range(1,25):
                baby_dna = self.generate_baby_dna(combo[0], combo[1], i)
                baby = Eim(baby_dna, combo[0], combo[1], i)
                next_gen.add_eim(baby)      
        
        # generate stats for this generation and display them
        next_gen.get_gen_stats()  
        print("==== breed_all_combinations ====")
        print("Created new generation #", next_gen.gen_num)            
        print("Population: ",next_gen.population)
        print("Clone Per: ",next_gen.stats.iloc[0]["4clone_per"])        
        print("Unique Chromosome Pairs: ",next_gen.stats.iloc[0]["5unique_chromosome_pairs"])                      
        return next_gen      
    
    
    def generate_baby_dna(self,mom_dna,dad_dna,method):
        """ All possible combinations from these parents  """
        """ No mutation here, just the method 1 to 24 as defined """
        
        # break parents into 4 chromosomes each
        cm1 = mom_dna[0]+mom_dna[1]
        cm2 = mom_dna[2]+mom_dna[3]
        cm3 = mom_dna[4]+mom_dna[5]
        cm4 = mom_dna[6]+mom_dna[7]
        cd1 = dad_dna[0]+dad_dna[1]
        cd2 = dad_dna[2]+dad_dna[3] 
        cd3 = dad_dna[4]+dad_dna[5]
        cd4 = dad_dna[6]+dad_dna[7] 
        
        # return DNA based on method
        
        # option 1 - equal spit of dna between parents
        # our dna splits into two halves and recombines
        # 8 possible combinations based on order  
        
        # mom goes first
        if(method==1):
            return(cm1+cm2+cd1+cd2) # m 12 d 12
        elif(method==2):
            return(cm1+cm2+cd3+cd4) # m 12 d 34
        elif(method==3):
            return(cm3+cm4+cd1+cd2) # m 34 d 12       
        elif(method==4):
            return(cm3+cm4+cd3+cd4) # m 34 d 34    

        # dad goes first               
        elif(method==5):
            return(cd1+cd2+cm1+cm2) # d 12 m 12               
        elif(method==6):
            return(cd1+cd2+cm3+cm4) # d 12 m 34      
        elif(method==7):
            return(cd3+cd4+cm1+cm2) # d 34 m 12   
        elif(method==8):
            return(cd3+cd4+cm3+cm4) # d 34 m 34 
            
         # option 2 - mom is gentically dominant
         # our dna splits  3/1 in favor of mom
         # 8 possible combinations based on order            
         
         # mom goes first
        elif(method==9):
            return(cm1+cm2+cm3+cd1) # m 123 d 1   
        elif(method==10):
            return(cm1+cm2+cm3+cd4) # m 123 d 4 
        elif(method==11):
            return(cm2+cm3+cm4+cd1) # m 234 d 1   
        elif(method==12):
            return(cm2+cm3+cm4+cd4) # m 234 d 4
            
        # dad goes first            
        elif(method==13):
            return(cd1+cm1+cm2+cm3) # d 1 m 123     
        elif(method==14):
            return(cd4+cm1+cm2+cm3) # d 4 m 123    
        elif(method==15):
            return(cd1+cm2+cm3+cm4) # d1 m 234     
        elif(method==16):
            return(cd4+cm2+cm3+cm4) # d 4 m 234  
            
        # option 3 - dad is gentically dominant
        # our dna splits  3/1 in favor of dad
        # 8 possible combinations based on order            
        
        # mom goes first
        elif(method==17):
            return(cm1+cd1+cd2+cd3) # m 1 d 123    
        elif(method==18):
            return(cm1+cd2+cd3+cd4) # m 1 d 234    
        elif(method==19):
            return(cm4+cd1+cd2+cd3) # m 4 d 123    
        elif(method==20):
            return(cm4+cd2+cd3+cd4) # m 4 d 234
            
        # dad goes first            
        elif(method==21):
            return(cd1+cd2+cd3+cm1) # d 123 m 1    
        elif(method==22):
            return(cd2+cd3+cd4+cm1) # d 234 m 1    
        elif(method==23):
            return(cd1+cd2+cd3+cm4) # d 123 m 4    
        elif(method==24):
            return(cd2+cd3+cd4+cm4) # d 234 m 4             


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
        if(random.randint(1,ODDS_OF_MUTATION)==1):
        #if(1==1):
            #print("~~~~~~MUTATION~~~~~~")
            replace = ['A','B','C','D']
            i = random.randint(0,3)
            j = random.randint(0,3)            
            baby_dna = list(baby_dna)
            baby_dna[i]=replace[j]
            baby_dna = "".join(baby_dna)
        return baby_dna
        


def TimerMessage(startTime, gen):
    print("------------------------------------------------------------------------------")
    print("Created generation "+str(gen)+" in "+str(datetime.now() - startTime)+" seconds")
    print("------------------------------------------------------------------------------")

######################################################################################
# create our first generation
startTime = datetime.now()
gen1 = Generation()
print("==== start with Adam & Eve ====")
# create our adam and eve
adam = Eim('AABBCCDD')
eve = Eim('EEFFGGHH')

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
TimerMessage(startTime, 2)

#######################################################################################
# create the 4th generation by breeding ALL unique combinations of the 3rd generation
startTime = datetime.now()
gen4 = gen3.breed_all_combinations()
TimerMessage(startTime, 2)

# create the 3rd generation by breeding ALL combinations of the 2nd generation
#gen3 = gen2.breed_all_combinations()
#gen4 = gen3.breed_all_combinations()



print(Generation.df)
#print(gen3.eims_df)
"""
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
    if(tmp.fitness_best==MAX_POSSIBLE_CONFLICTS):
        break
    
for eim in tmp.eims:
    if(eim.conflicts==0):
        print(eim.dna)    
        print(eim.conflicts)    
        print(eim.queens)

print("There have been a total of ",tmp.cumulative_population," Eims since the dawn of time")
for eim in gen3.eims:
    print(eim.conflicts)
"""
