# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:27:56 2020

@author: strai"""
import time
from copy import deepcopy

file = 'Assignment 1 Spain map.txt'
locations = 77

class City:
    
    def __init__(self, name=None, straight_distance=0, distances=None):
        self.name = name
        self.straight_distance = straight_distance
        self.distances = distances
        
    def __eq__(self):
        return self.name
    
    def __str__(self):
        return str(self.name)
    

with open(file, 'r') as f:
    lines = f.readlines()
    lines_dist = lines[5:5+locations]
    lines_straight = lines[8+locations:]
    names = set(map(lambda x: x.split(' ')[0], lines_straight))
    cities = {}
    for city in names:
        distances = {}
        straight = 0
        for line in lines_dist:
            splt = line.split(' ')
            if splt[0] == city:
                key = splt[1]
                distances[key] = int(splt[2])
            if splt[1] == city:
                key = splt[0]
                distances[key] = int(splt[2])
        for line in lines_straight:
            splt = line.split(' ')
            if splt[0] == city:
                straight = int(splt[1])
                break
        new_city = City(name = city, straight_distance = straight, distances = distances)
        cities[city] = new_city
        

def greedy_search(city, dest_city, path, expanded, path_length):
    #Look only at straight distances
    global cities
    dst = list(cities[city].distances.keys())
    while dst != []:
        min_ = 1000000
        for node in dst:
            #Check expanded to avoid circles
            if node not in expanded:
                if cities[node].straight_distance < min_:
                    min_ = cities[node].straight_distance
                    next_city = node
        # next_city = min(dst.keys(), key=(lambda k: dst[k]))
        if next_city == dest_city:
            path.append(next_city)
            path_length += cities[city].distances[next_city]
            return path, path_length
        else:
            if next_city not in expanded:
                path.append(next_city)
                path_length += cities[city].distances[next_city]
                expanded.append(next_city)
                final_path, path_length = greedy_search(next_city, dest_city, path, expanded, path_length)
                if dest_city in final_path:
                    return final_path, path_length
        # dst.pop(city)
        # path.remove(next_city)
        #This one is for when we didn't find solution in recursion, step back
        path.remove(city)
        path_length -= cities[city].distances[next_city]
    
            
def greedy():
    city = 'Malaga'
    dest_city = 'Valladolid'
    expanded = ['Malaga']
    path = ['Malaga']
    path_length = 0
    global cities
    dst = list(cities[city].distances.keys())
    while dst != []:
        min_ = 1000000
        #Look for minimal children of the root
        for node in dst:
            if node not in expanded:
                if cities[node].straight_distance < min_:
                    min_ = cities[node].straight_distance
                    next_city = node
        # next_city = min(dst.keys(), key=(lambda k: dst[k]))
        if next_city == dest_city:
            path.append(next_city)
            path_length += cities[city].distances[next_city]
            return path, path_length
        else:
            if next_city not in expanded:
                path.append(next_city)
                path_length += cities[city].distances[next_city]
                expanded.append(next_city)
                final_path, path_length = greedy_search(next_city, dest_city, path, expanded, path_length)
                if dest_city in final_path:
                    return final_path, path_length
        
        dst.pop(city)
        path.remove(next_city)
        path_length -= cities[city].distances[next_city]

def A_search(city, dest_city, path, expanded, path_length):
    global cities
    dst = list(cities[city].distances.keys())
    while dst != []:
        min_ = 1000000
        for node in dst:
            if node not in expanded:
                check = cities[node].straight_distance + cities[city].distances[node]
                if check < min_:
                    min_ = check
                    next_city = node
        # next_city = min(dst.keys(), key=(lambda k: dst[k]))
        if next_city == dest_city:
            path.append(next_city)
            path_length += cities[city].distances[next_city]
            return path, path_length
        else:
            if next_city not in expanded:
                path.append(next_city)
                path_length += cities[city].distances[next_city]
                expanded.append(next_city)
                final_path, path_length = A_search(next_city, dest_city, path, expanded, path_length)
                if dest_city in final_path:
                    return path, path_length
        # dst.pop(city)
        # path.remove(next_city)
        path.remove(city)
        path -= cities[city].distances[next_city]

def A_mod():
    city = 'Malaga'
    path = []
    path_length = 0
    expanded = []
    global cities
    smallest = []
    dst = list(cities[city].distances.keys())
    for node in dst:
        check = cities[node].straight_distance + cities[city].distances[node]
        pt = [city, node]
        smallest.append((pt, check))
        # expanded.append(str(pt))
        if node == 'Valladolid':
            path.append((pt, check))
    sort = sorted(smallest, key=lambda x: x[1])
    while sort != []:
        next_node = sort[0]
        smallest.remove(next_node)
        # for i in range(len(sort)):
        #     if str(sort[i][0]) not in expanded:
        #         next_node = sort[i]
        #         expanded.append(str(next_node[0]))
        #         break
        # print(next_node[0])
        if 'Valladolid' in next_node[0]:
            return next_node
        city = next_node[0][-1]
        dst = list(cities[city].distances.keys())
        for node in dst:
            str_check = cities[node].straight_distance 
            us_check = 0
            for i in range(len(next_node[0])-1):
                first_city = str(next_node[0][i])
                second_city = str(next_node[0][i+1])
                us_check += cities[first_city].distances[second_city]
            us_check += cities[next_node[0][-1]].distances[node]
            pt = deepcopy(next_node[0])
            pt.append(node)
            check = str_check + us_check
            smallest.append((pt, check))
        sort = sorted(smallest, key=lambda x: x[1])
    # return path
        
    
    
    
start = time.time()    
path, past_length = greedy()
end = time.time() - start
print('Algorithm Greedy Best-First Search, path:', path, ' length of path:', past_length, f'time: {end}')   
start = time.time() 
p = A_mod()
end = time.time() - start
print('Algorithm A*, path: ', p[0], ' length of path:', p[1], f'time: {end}')    
    