# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:12:06 2020

@author: strai
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:26:35 2020

@author: strai
"""


import numpy as np
import random
import matplotlib as plt

#Loading data
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
source = list(range(2, number_of_cities+1))

def calc_fit(ind):
    i = 0
    fit = 0
    while i < len(ind)-1:
        city_1 = str(ind[i])
        city_2 = str(ind[i+1])
        dist = np.sqrt((cities[city_2][0]-cities[city_1][0])**2 + (cities[city_2][1]-cities[city_1][1])**2)
        fit += dist
        i +=1
    return fit

#Create first population
population = {}
whole_population = 100

for i in range(whole_population):
    ind = [1]
    ind.extend(list(np.random.permutation(source)))
    ind.append(ind[0])
    fit = calc_fit(ind)
    population[str(i)] = (ind, fit)
        
#Iterating
number_of_generations = 2500
elite_perc = int(whole_population * 0.1)
replace_perc = int(whole_population * 0.5)
# rand_perc = int(whole_population * 0.1)
mut_perc = whole_population - elite_perc - replace_perc 
    

def crossover(parents):
    parent_1 = parents[0][0].copy()
    parent_2 = parents[1][0].copy()
    child_1 = [1]
    parent_1.pop(0)
    parent_2.pop(0)
    parent_1.pop(-1)
    parent_2.pop(-1)

    rand_pos = random.randrange(0, number_of_cities-3 )
    if number_of_cities - rand_pos == 3:
        rand_num = 1
    else:
        rand_num = random.randrange(1, number_of_cities - rand_pos)
    random_seq = parent_1[rand_pos:(rand_pos+rand_num)]
    for elem in random_seq:
        if elem in parent_2:
            parent_2.remove(elem)
    for i in range(0, rand_pos):
        elem = parent_2.pop(0)
        child_1.append(elem)
    for elem in random_seq:
        child_1.append(elem)
    for i in range(rand_pos + rand_num + 1, number_of_cities):
        elem = parent_2.pop(0)
        child_1.append(elem)
    child_1.append(child_1[0])
    if len(child_1) - len(set(child_1)) != 1:
        print(";")
    return child_1


def mutation2(indiv):
    ind = indiv[0].copy()
    ind.pop(-1)
    src = list( range(1, len(ind)))
    # mut_degree = int(number_of_cities * 0.1)
    mut_degree = 1
    for i in range(mut_degree):
        val = random.sample(src, 2)
        a = min(val[0], val[1])
        b = max(val[0], val[1])
        range_ = ind[a:b]
        new_range = []
        for i in range(len(range_)-1, -1, -1):
            new_range.append(range_[i])
        # print(val)
        ind[a:b] = new_range
        # ind[val[0]], ind[val[1]] = ind[val[1]], ind[val[0]]
    ind.append(ind[0])
    return ind


def tournament_selection(population):
    parent_1 = np.random.choice(range(whole_population))
    parent_1 = population[str(parent_1)]
    
    parent_2 = np.random.choice(range(whole_population))
    parent_2 = population[str(parent_2)]
    
    while parent_2 == parent_1:
        parent_2 = np.random.choice(range(whole_population))
        parent_2 = population[str(parent_2)]
    
    parent_3 = np.random.choice(range(whole_population))
    parent_3 = population[str(parent_3)]
    
    while parent_3 == parent_1 or parent_3 == parent_2:
        parent_3 = np.random.choice(range(whole_population))
        parent_3 = population[str(parent_3)]
        
    mkss = max([parent_1[1], parent_2[1], parent_3[1]])
    if parent_1[1] == mkss:
        return parent_1
    elif parent_2[1] == mkss:
        return parent_2
    else:
        return parent_3
    

crossover([population['1'], population['2']])
def make_children(parents):
    children = []
    while parents != []:
        samples = random.samples(parents, 2)
        
        
counter = 0
best_score = 0
plt_scores = []
    

for i in range(number_of_generations):
    num = 0
    new_population = {}
    sort = sorted(population.items(), key = lambda elem: elem[1][1])
    best_children = []
    for j in range(len(population)):
        best_children.append(population[sort[j][0]])
    print(best_children[0][1], ' ', i)
    plt_scores.append(best_children[0][1])
    new_best_score = best_children[0][1]
    if new_best_score == best_score:
        counter +=1
    else:
        counter = 0
        mutation_rate = 0.1
    if counter > 50:
        mutation_rate = 0.8
        
    if best_children[0][1] < 9000.0:
        print(best_children[0])
        break
    for i in range(elite_perc):
        new_population[str(num)] = best_children[i]
        num +=1
        
    probs = []
    prep = []
    for i in range(len(population)):
        prep.append(38000 - population[str(i)][1])
    # sum_ = sum(population[str(k)][1] for k in population.keys())
    sum_ = sum(prep[i] for i in range(len(population)))
    # for i in range(len(population)):
    #     probs.append(population[str(i)][1] / sum_)
    for i in range(len(population)):
        probs.append(prep[i] / sum_)

    
    while len(new_population) != len(population):
    # for i in range(replace_perc + mut_perc):
        parent_1 = np.random.choice(range(whole_population), p = probs)
        parent_1 = population[str(parent_1)]
        parent_2 = np.random.choice(range(whole_population), p = probs)
        parent_2 = population[str(parent_2)]
        while parent_2 == parent_1:
            parent_2 = np.random.choice(range(whole_population), p = probs)
            parent_2 = population[str(parent_2)]
        new_child = crossover([parent_1, parent_2])
        rand = random.random()
        if rand < mutation_rate:
            new_child = mutation2((new_child, calc_fit(new_child)))
        fit = calc_fit(new_child)
        new_population[str(num)] = (new_child, fit)
        num +=1

    best_score = new_best_score
    population = new_population.copy()
        
    
    