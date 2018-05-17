#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:54:10 2018

@author: joshwork

Playing around with a genetic algorithm

Playing with the Eims
"""

######################################################################################
# Define the scope of the N-Queens problem
N_QUEENS = 4

######################################################################################
# Class to handle our fictional "Eim" creatures
class Eim:
    # class variables
    population = 0 
    
    def __init__(self, generation, dna):
        """ Create a new Eim creature based on generation count and DNA sequence """
        
        # increment population by 1 new Eim
        Eim.population += 1        
        
        # set our generation and dna for this Eim
        self.generation = 1
        self.dna = dna

        # calculate the fitness of this Eim 
        self.calculate_fitness(dna)
        
        
    def calculate_fitness(self, dna):
        """ Calculate the fitness of any Eim based on N-Queens """

        # hold our queen coordinates in a list of tuples
        self.queens = []
        for key, chromosome in enumerate(dna): 
            row = self.mapper(chromosome)            
            col = key+1
            self.queens.append((row,col))
            
        # check each of our queens for all possible conflicts
        conflicts = 0
        for queen in self.queens:
            conflicts += self.check_right(queen)
            conflicts += self.check_left(queen)
            # no need to check up or down since we only have 1 per column
            #conflicts += self.check_up(queen)
            #conflicts += self.check_down(queen)             
            conflicts += self.check_upright(queen)  
            conflicts += self.check_upleft(queen) 
            conflicts += self.check_downright(queen)             
            conflicts += self.check_downleft(queen)              
            #break
        
        self.fitness = 7  
        print(conflicts)
        print(self.queens)
        
        
        
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
        print("OUR QUEEN")
        print(row, col)
        print("CHECK!")        
        while(row > 0 and col < N_QUEENS):
            row -= 1
            col += 1            
            print(row, col) 
            print(self.queens)
            if (row,col) in self.queens:
                print("CONFLICT!")
                return 1
        print("NO CONFLICT!")            
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



# create our first generation
adam = Eim(1,'DDCC')
#eve = Eim(1,'BBAA')

#print(adam.dna)
#print(adam.fitness)

#Eim.how_many()