# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:40:30 2020

@author: strai
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 08:58:40 2020

@author: strai
"""

import pandas as pd
import time

dimension = 0
max_weight = 0
knapsack = {}
file = 'Assignment 1 knapsack.txt'


def read_assignment(file):
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            if 'DIMENSION:' in line:
                spl = line.split(" ")
                global dimension
                dimension = int(spl[1])
            if 'MAXIMUM' in line:
                spl = line.split(" ")
                global max_weight
                max_weight = int(spl[2])
            if line[0].isdigit():
                spl = line.split(" ")
                # knapsack.loc[int(spl[0])] = spl[1:]
                key = spl[0]
                ben = int(spl[1])
                weight = int(spl[2])
                knapsack[key] = [ben, weight]
        return knapsack
            
knapsack = read_assignment(file)
class Node:
    
    def __init__(self, name=None, left = None, right = None, weight = None, benefit = None):
        self.name = name
        self.weight = weight
        self.benefit = benefit
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.data)
    
class Tree:
    
    def __init__(self):
        self.root = Node(name = '1', weight=knapsack['1'][1], benefit = knapsack['1'][0])
        
    def build_tree(self, dimension):
        left_param = decode('10')
        right_param = decode('11')
        left = Node(name = '10', weight = left_param[1], benefit = left_param[0])
        right = Node(name = '11', weight = right_param[1], benefit = right_param[0])
        self.root.left = left
        self.root.right = right
        self.add_successor(left, dimension)
        self.add_successor(right, dimension)
        
    
    def add_successor(self, node, dimension):
        new_left_name = node.name + '0'
        new_right_name = node.name + '1'
        if len(new_left_name) > dimension or len(new_right_name) > dimension:
            return
        new_left_param = decode(new_left_name)
        #When I build a tree, I add only combinations which weight is ok
        if new_left_param[1] <= max_weight:
            new_left = Node(name = new_left_name, weight = new_left_param[1], benefit = new_left_param[0])
            node.left = new_left
            self.add_successor(new_left, dimension)
            
        new_right_param = decode(new_right_name)
        if new_right_param[1] <= max_weight:
            new_right = Node(name = new_right_name, weight = new_right_param[1], benefit = new_right_param[0])
            node.right = new_right
            self.add_successor(new_right, dimension)
            
    def BFS(self):
        #Save and expand first node
        #Max benefit is benefit of combination
        max_benefit = self.root.benefit
        self.max_node = self.root
        queue = []
        #Append to queue
        queue.append(self.root.left)
        queue.append(self.root.right)
        while queue != []:
            node = queue[0]
            # print(node.name)
            if node.benefit > max_benefit:
                max_benefit = node.benefit
                self.max_node = node
            if node.left != None:
                queue.append(node.left)
            if node.right != None:
                queue.append(node.right)
            queue.remove(node)
            
    def DFS(self):
        max_benefit = self.root.benefit
        self.max_node = self.root
        stack = []
        stack.append(self.root.left)
        stack.append(self.root.right)
        while stack != []:
            node = stack.pop()
            # print(node.name)
            if node.benefit > max_benefit:
                max_benefit = node.benefit
                self.max_node = node
            if node.left != None:
                stack.append(node.left)
            if node.right != None:
                stack.append(node.right)

#Use decode to know benefit and weight of current combination
def decode(code):
    benefit = 0
    weight = 0
    dm = len(code)
    for c, i in enumerate(code):
        if i == '1':
            key = str(dm - c)
            benefit += knapsack[key][0]
            weight += knapsack[key][1]
    return (benefit, weight)

def decode_name(code):
    items = []
    dm = len(code)
    for c, i in enumerate(code):
        if i == '1':
            item = str(dm - c)
            items.append(item)
    return items
        
start = time.time()
tree = Tree()
tree.build_tree(dimension)   
tree.BFS()
end = time.time() - start             
items = decode_name(tree.max_node.name)
print(f'Time: {end}, maximum benefit: {tree.max_node.benefit}, this weight: {tree.max_node.weight}, items: {items}')
        

            
    