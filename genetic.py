# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:17:56 2017

@author: Alberto
"""

import random


"""para crear cada cromosoma individual"""
def individual(length):
    return random.sample(range(0,length), length)

"""crea una nueva población con cromosomas de longitud 'length' y con 'count' número de cromosomas"""
def population(length, count):
    return [ individual(length) for x in range(count) ]    
    

"""nuestras ciudades y la lista de todas. según creemos ciudades, se añadirán a la lista"""

cities =[]

class City(object):
    
    def __init__(self, name, reach):
        # Name and coordinates:
        self.name = name
        """reach es una lista de nombres. Ciudades a las que podrá ir. Es más fácil que añadirle ciudades directamente porque
        habría que hacer que cada ciudad nueva que creas compruebe a donde puede llegar y actualizar el resto"""
        self.reach= reach
        cities.append(self)

    
"""Otro método para mutar fácilmente aplicable y que podemos modificar. Usa el mutador de Problem_Genetic"""
def mutate_individuals(problem_genetic, population, prob):
    sol=[]
    for j in range(0,len(population)):
        sol.extend(problem_genetic.mutation(population[j],prob))
    return sol
    

"""decode coge el cromosoma en forma de lista desordenada, y devuelve los elementos ordenados. Testeado y funcional"""
def decode_traveler(individual):
    dec = [None]*len(cities)
    for i in range(len(individual)):
        dec[individual[i]] = cities[i]
    
    return dec
    
    
"""fitness de la función. Va maximizando así que las penalizaciones restan"""
def fitness_traveler(individual):
    dec = decode_traveler(individual)
    sol=0
    
    for i in range(len(dec)):  
        if(i==0 or i==len(dec)):  
            if not dec[0].name in dec[len(dec)-1].reach:
                sol = sol - 1
        else:
            if not dec[i].name in dec[i-1].reach:
                sol = sol - 1
    
    return sol
    
"""con esto sacamos el fitness medio de cada generación, para ver la evolución"""    
def grade_traveler(population):
    sum = 0
    for i in range(len(population)):
        sum = sum + fitness_traveler(population [i])
    sum = sum/len(population)
    return sum
"""
hacemos selección de individuos que van a la siguiente generación. Yo he puesto de coger 1/5 de cada generación. Los mejores solo. 
Creo que con eso ya va bien.
"""    
def selection(population):
    pop_len=len(population)
    cut = round(pop_len/5)
    part = [None]*cut
    fitnesses = [None]*pop_len
    for i in range(pop_len):
        fitnesses[i] = fitness_traveler(population[i])
    all = list(zip(fitnesses, population))
    all.sort(key=lambda tup: tup[0], reverse=True)
    sort_pop = [x[1] for x in all]
    for x in range(cut):
        if(x<cut):
            part[x] = sort_pop[x]
    return part
    
"""la población debe ser mayor a 1"""    
def select_individual_crossover(population):
    
       rand1 = random.randint(0,len(population)-1)
       rand2 = random.randint(0,1)
       ind1 = population[rand1]
       ind2 = None
       if rand1 == 0:
           ind2 =population[1] 
       elif rand1 == (len(population)-1):
           ind2 = population[rand1-1]
       else:
           if rand2 == 0:
               ind2 = population[rand1-1]
           elif rand2==1:
               ind2 = population[rand1+1]
           
       inds = (ind1, ind2)
       return inds
   
def swap_mutation(individual):
   
    condition = True
    
    while condition:
        a = random.randint (0, len(individual)-1)
        b = random.randint (0, len(individual)-1)
        condition = (a == b)
    
    individual[a], individual[b] = individual[b], individual[a]
    
    return individual
    
    
def insert_mutation(individual):
    
    condition = True
    
    while condition:
        a = random.randint (0, len(individual)-1)
        b = random.randint (0, len(individual)-1)
        condition = (a == b)
    
    temp_elem = individual[b]
    individual.remove(individual[b])
    individual.insert(individual[a+1], temp_elem)
    
    return individual
    
def mutate_population(population, chance):
    new_population = []
    for i in population:
        if chance > random.random():
            if fitness_traveler(i) != 0:
                new_population.append(swap_mutation(i))
#            new_population.append(insert_mutation[i])
        else:
            new_population.append(i)
    return new_population


def order_crossover(ind1, ind2):
    
    repeat = True
    
    while repeat:
        crosspoint = random.randint(0, len(ind1)-1)
        child = ind2[:crosspoint]+ind1[crosspoint:]
        if set(ind1) == set(child):
            repeat = False
  
    return child
    
    
def evolve(population, chance):
    pop_len = len(population)
    part = selection(population)
    new_size = pop_len - len(part)
    new_part = [None]*new_size
    for i in range(new_size):
        individuals = select_individual_crossover(part)
        p1 = individuals[0]
        p2 = individuals[1]
        individual = order_crossover(p1, p2)
        new_part[i] = individual
    res = part + new_part
    res = mutate_population(res, chance)
    
    return res
    
def most_suited(population):
    pop_len = len(population)
    fitnesses = [None]*pop_len
    for i in range(pop_len):
        fitnesses[i] = fitness_traveler(population[i])
    all = list(zip(fitnesses, population))
    all.sort(key=lambda tup: tup[0], reverse=True)
    sort_pop = [x[1] for x in all]
    suited = sort_pop[0]

    return suited
    
    

def genetic_prob(ages, pop_size, mut_chance, cities):
    
    c_len = len(cities)
    
    pop = population(c_len, pop_size)
    
    grade = [None]*ages
    
    for i in range(ages):
        grade[i] = grade_traveler(pop)
        pop = evolve(pop, mut_chance)
    
    suited = most_suited(pop)
    
    result = [None]*c_len
    s_dec = decode_traveler(suited)
    
    for i in range(c_len):
        result[i] = s_dec[i].name
    
    return {'population' : pop, 'grades' : grade, 'result' : result}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


