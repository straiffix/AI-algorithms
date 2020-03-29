# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:05:53 2020

@author: strai
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:14:48 2020

@author: strai
"""
from itertools import cycle, product
import copy
import time

file = 'Assignment 2 sudoku.txt'
global_domain = set(range(1, 10))


class Sudoku():
    
    def __init__(self):
        self.rows = []
    
    def check_square(self, cr):
        
        x = cr[0] // 3
        y = cr[1] // 3
        if x == 0:
            rows = [0, 1, 2]
        elif x == 1:
            rows = [3, 4, 5]
        elif x == 2:
            rows = [6, 7, 8]
        if y == 0:
            columns = [0, 1, 2]
        elif y == 1:
            columns = [3, 4, 5]
        elif y == 2:
            columns = [6, 7, 8]
        
        return product(rows, columns)

    
    def check_square_for_domain(self, cr):
        x = cr[0] // 3
        y = cr[1] // 3
        if x == 0:
            rows = [0, 1, 2]
        elif x == 1:
            rows = [3, 4, 5]
        elif x == 2:
            rows = [6, 7, 8]
        if y == 0:
            columns = [0, 1, 2]
        elif y == 1:
            columns = [3, 4, 5]
        elif y == 2:
            columns = [6, 7, 8]
        
        Square = set()
        for row in rows:
            for column in columns:
                Square.add(self.rows[row][column])
        return Square
            
    
    def check_row(self, cr):
        row = cr[0]
        return set(self.rows[row])
    
    def check_columns(self, cr):
        column_num = cr[1]
        column = set()
        for row in self.rows:
            column.add(row[column_num])
        return set(column)
    
    def create_domain(self, cr):
        domain = set()
        row = self.check_row(cr)
        column = self.check_columns(cr)
        square = self.check_square_for_domain(cr)
        ex = row.union(column)
        ex = ex.union(square)
        domain = global_domain.difference(ex)
        return domain
    
    def create_variables(self):
        variables = []
        for num, row in list(enumerate(self.rows)):
            for column in range(9):
                if row[column] == 0:
                    variables.append((num, column))
        return variables
                    
    def solve_rec(self, variables, domains, variable, path):
        #Unnecesary check
        if variables == []:
            return path
        dom = domains[str(variable)]
        #Check if we have possible values for all remain cells, unnecessary
        if dom == set():
            return 0
        for value in dom:
            new_domains = copy.deepcopy(domains)
            nxt = 0
            new_variables = copy.deepcopy(variables)
            #Expand cell
            new_variables.remove(variable)
            #Removind chosen value from other domains in rows and columns
            for var in new_variables:
                if variable[0] == var[0] or variable[1] == var[1]:
                    if value in new_domains[str(var)]:
                        new_domains[str(var)].remove(value)
            #Removing chosen value from domains of square
            square = self.check_square(variable)
            for cr in square:
                if cr in new_variables:
                    if value in new_domains[str(cr)]:
                        new_domains[str(cr)].remove(value)
            #If we have some cells without possible values, step back
            for dm in new_domains:
                if new_domains[dm] == set():
                   nxt +=1
            if nxt!= 0:
                continue
            result = 0
            #Assign value
            del new_domains[str(variable)]
            #If we dont have other domains than it solved right
            if new_domains == {}:
                path[str(variable)] = value
                return path
            path[str(variable)] = value
            #Sort to chose variable with the smallest domain
            new_variables = sorted(new_variables, key = lambda x: len(new_domains[str(x)]))
            for var in new_variables:
                result = self.solve_rec(new_variables, new_domains, var, path)
                #If only one cells don't have solution, than this assigned value is wrong
                if result == 0:
                    break
                else:
                    return result

        return 0        
            
            
    def solve(self):
        #Create list of all unknown cells
        variables = self.create_variables()
        #Domains represent domains of possible value for each cell
        domains = {}
        for variable in variables:
            domains[str(variable)] = self.create_domain(variable)
        #I sort variables and always take next cell which have the smallest amount of possible values
        variables = sorted(variables, key = lambda x: len(domains[str(x)]))
        path = {}
        for var in variables:
            #I return to beginning
            result = self.solve_rec(variables, domains, var, path)
            if result == 0:
                    continue
            else:
                return result
    
                    
    def print_result(self, result):
        for num, row in enumerate(self.rows):
            for nm, col in enumerate(row):
                cell = [num, nm]
                cell = str(tuple(cell))
                if cell in result.keys():
                    if self.rows[num][nm] == 0:
                        self.rows[num][nm] = result[cell]
        for row in self.rows:
            print(row)
        
    
    
sudokues = []

with open(file, 'r') as f:
    lines = f.readlines()
    sudoku = 0
    for line in range(len(lines)):
        if 'SUDOKU' in lines[line]:
            sudoku +=1
            continue
        if sudoku!=0:
            sud = Sudoku()
            for sud_line in range(line, line+9):
                sud.rows.append([int(i) for i in list(lines[sud_line])[:-1]])            
            line += 9
            sudokues.append(sud)
            sudoku = 0
for sudoku in sudokues:
    start = time.time()
    result = sudoku.solve()
    end = time.time() - start
    print(end, 's')
    sudoku.print_result(result)
