# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:14:34 2020

@author: strai
"""
from math import sqrt
import random
import matplotlib.pyplot as plt

file = 'Assignment 3 berlin52.tsp'
cities = {}
with open(file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line[0].isdigit():
            spl = line.split(' ')
            id_ = spl[0]
            x = float(spl[1])
            y = float(spl[2][:-1])
            cities[str(id_)] = (x, y)
            
            

number_of_cities = len(cities)
ant_num = 50
alpha = 0.6
beta = 5
evap_cof = 0.4
init_pheromone_value = 100

def calc_dist(city_1, city_2):
    dist = sqrt((city_2[1] - city_1[1])**2 + (city_2[0]-city_1[0])**2)
    return dist

def calc_route_dist_test(path):
    dist = 0
    for i in range(len(path)-1):
        city_1 = path[i]
        city_2 = path[i+1]
        dist += calc_dist(cities[str(city_1)], cities[str(city_2)])
    return dist


class Ant():
    def __init__(self, cur_loc = 1, pheromone_map = {}):

        self.current_location = cur_loc
        self.path = []
        self.distance = 0
        self.possible_locations = list(cities.keys())
        self.pheromone_map = pheromone_map
        # self.ant_pheromone_map = self.init_pheromone_map()
        self.pher_const = 10
        self.update_path(int(cur_loc))
        
        
        
    def update_path(self, city):
        self.path.append(city)
        self.possible_locations.remove(str(city))

        
    def calc_route_dist(self):
        dist = 0
        for i in range(len(self.path)-1):
            city_1 = self.path[i]
            city_2 = self.path[i+1]
            dist += calc_dist(cities[str(city_1)], cities[str(city_2)])
        return dist
    
    def run(self):
        while self.possible_locations != []:
            self.traverse()
        self.path.append(1)
        self.distance = self.calc_route_dist()
    
    #If it is not first run, then I use this function
    # For each possible location I calculate attractiveness pherm^^alpha  *  1/dist^^beta
    def traverse(self):
        attractiveness = dict()
        sum_total = 0.0
        next_location = 0
        pos_loc_lst = []
        attr_lst = []
    
        for possible_next_location in self.possible_locations:
            pheromone = float(self.pheromone_map[str((self.current_location, int(possible_next_location)))])
            distance = float(calc_dist(cities[str(self.current_location)], cities[possible_next_location]))
            try:
                attractiveness[possible_next_location] = pow(pheromone, alpha)*pow(1/distance, beta)
            except ZeroDivisionError:
                print(self.current_location, cities[possible_next_location])
            sum_total += attractiveness[possible_next_location]
            
        #     pos_loc_lst.append(possible_next_location)
        #     attr_lst.append((pow(pheromone, alpha)*pow(1/distance, beta)))
 			
        # next_location = int(random.choices(pos_loc_lst, weights = attr_lst, k = 1)[0])
        toss = random.random()				
        
        #Weighted random choice
        cummulative = 0
        for possible_next_location in attractiveness:
            weight = (attractiveness[possible_next_location] / sum_total)
            if toss <= weight + cummulative:
                next_location = int(possible_next_location)
                break
            cummulative += weight
             
        self.update_path(next_location)
        self.current_location = next_location
        # self.distance = self.calc_route_dist()

        
        
    def first_run(self):
        while self.possible_locations != []:
            next_city = random.choice(self.possible_locations)
            self.update_path(int(next_city))
            self.current_location = next_city
        self.path.append(1)
        self.distance = self.calc_route_dist()

        
        

class ant_colony():
    
    def __init__(self):
        self.colony = []
        self.shortest_distance = 400000
        self.shortest_path = []
        self.pheromone_map = self.init_pheromone_map(init_pheromone_value)
        self.current_generation_pheromone_map = self.init_pheromone_map()
        
        #When initializing, first run - each ant has random walk, then I looking for shortest dist, then I use random locations for updating pheromone map
        #After each walk I clean ants, each has it's own pheromone map, and they updare it one by one, and in the end I calculate common map
        for i in range(ant_num):
            ant = Ant(pheromone_map = self.pheromone_map)
            ant.first_run()
            if ant.distance < self.shortest_distance:
                self.shortest_distance = ant.distance
                self.shortest_path = ant.path
            self.colony.append(ant)
            self.update_generation_pheromone_map(ant)
        print(self.shortest_distance)
        self.update_pheromone_map()
        self.clean()        
        
    def clean(self):
        for ant in self.colony:
            ant = ant.__init__(pheromone_map = self.pheromone_map)
        
        self.current_generation_pheromone_map = self.init_pheromone_map()
        
    # Each ant runs, update generation pheromone map, in the end whole map is updated        
    def generation(self):
        for ant in self.colony:
            ant.run()
            if ant.distance < self.shortest_distance:
                self.shortest_distance = ant.distance
                self.shortest_path = ant.path
            self.update_generation_pheromone_map(ant)
        self.update_pheromone_map()
        self.clean()
    
    def init_pheromone_map(self, value = 0):
        pheromone_map = {}
        for i in range(1, number_of_cities+2):
            for j in range(1, number_of_cities+2):
                pheromone_map[str((i, j))] = value
        return pheromone_map
        
    #Pheromone map only for one generation
    def update_generation_pheromone_map(self, ant):
        for i in range(1, len(ant.path)):
            city_1 = i
            city_2 = i + 1
            edge_1 = str((city_1, city_2))
            edge_2 = str((city_2, city_1))
            new_value = ant.pher_const / ant.distance
            try:
                self.current_generation_pheromone_map[edge_1] = self.current_generation_pheromone_map[edge_1] + new_value
                self.current_generation_pheromone_map[edge_2] = self.current_generation_pheromone_map[edge_2] + new_value
            except KeyError:
                print( edge_1, edge_2)
            # self.ant_pheromone_map[edge_2] = self.ant_pheromone_map[edge_2] + new_value
            
    #Pheromone map for all excisting generations, evaporations + add values for current generation
    def update_pheromone_map(self):
        for i in range(1, number_of_cities + 1):
            for j in range(1, number_of_cities + 1):
                self.pheromone_map[str((i, j))] = (1 - evap_cof) * self.pheromone_map[str((i, j))]
                self.pheromone_map[str((i, j))] += self.current_generation_pheromone_map[str((i, j))]
                
        

colony = ant_colony()  
dist = []
    
number_of_iterations = 1000
for i in range(number_of_iterations):
    colony.generation()
    print(colony.shortest_distance)
    dist.append(colony.shortest_distance)
    if colony.shortest_distance < 9000:
        print(colony.shortest_path)
        break

plt.title('Performance of the population evolves with generations')
plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.plot(list(range(1, len(dist)+1)), dist)
            
            