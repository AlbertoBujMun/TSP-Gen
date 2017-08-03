# -*- coding: utf-8 -*-

"""
Created on Thu Jan 26 21:17:56 2017

@author: Alberto
"""

import random
from itertools import chain

testnum = 0


"""para crear cada cromosoma individual"""
def individual(length):
    return random.sample(range(0,length), length)

"""crea una nueva población con cromosomas de longitud 'length' y con 'count' número de cromosomas"""
def population(length, count):
    pop = [ individual(length) for x in range(count) ]
    print('POBLACIÓN INICIAL:')
    print(pop)
    return pop
    

"""nuestras ciudades y la lista de todas. según creemos ciudades, se añadirán a la lista"""

cities =[]

class City(object):
    
    def __init__(self, name, reach):
        """ Nombre de la ciudad y diccionario con otras ciudades y la distancia a la que se encuentran estas. """
        
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
    
    
"""fitness de la función. Hay que miniminar el coste. TODO pensar en como calcular esto.(ready to test). TODO modificar para los nuevos diccionarios."""

def fitness_traveler(individual):
	dec = decode_traveler(individual)
	sol=0
	for i in range(len(dec)):
		if(i==len(dec)-1):
			sol = sol + dec[i].reach[dec[0].name]
		elif(dec[i].reach[dec[i+1].name] is None):
			sol = sol + 999999*999999
		else:
			sol = sol + dec[i].reach[dec[i+1].name]
			
	print('FITNESS DE INDIVIDUO')
	print(sol)
	return sol



    
"""con esto sacamos el fitness medio de cada generación, para ver la evolución"""    
def grade_traveler(population):
    sum = 0
    for i in range(len(population)):
        sum = sum + fitness_traveler(population [i])
    sum = sum/len(population)
    print('NOTA DE POBLACIÓN'+ str(testnum) +':')
    print(sum)
    return sum
"""
hacemos selección de individuos que van a la siguiente generación. Yo he puesto de coger 1/5 de cada generación. Los mejores solo. 
Creo que con eso ya va bien. Si el corte sale 0 o 1, pasan 2 mínimo.
"""    
def selection(population):
    pop_len=len(population)
    cut = int(round(pop_len/5))
    if(cut<=1):
      cut=2
    part = [None]*cut
    fitnesses = [None]*pop_len
    for i in range(pop_len):
        fitnesses[i] = fitness_traveler(population[i])
    all = list(zip(fitnesses, population))
    all.sort(key=lambda tup: tup[0], reverse=False)
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
	   
	   
"""mutación de orden es la más adecuada para este problema.
Se cogen dos genes(ciudades) y se coloca uno delante del otro
mirar este artículo: http://www.permutationcity.co.uk/projects/mutants/tsp.html"""

def order_mutation(individual):
   
  condition = True
  while condition:
	  a = random.randint (0, len(individual)-1)
	  print('SE LIA A:')
	  print(a)
	  b = random.randint (0, len(individual)-1)
	  print('SE LIA B:')
	  print(b)
	  condition = (a == b or a>b)
	
  print('INDIVIDUAL ANTES')
  print(individual)
  part1 = individual[0:a]
  part2 = individual[b]
  part3 = individual[a]
  part4 = individual[a+1:b]
  part5 = individual[b+1:len(individual)]
  
    
  new_individual = []
  
  if(len(part1)!=0):
    if(len(part1)==1):
      new_individual.append(part1[0])
    else:
      new_individual.extend(part1)
  new_individual.append(part2)
  new_individual.append(part3)
  if(len(part4)!=0):
    if(len(part4)==1):
      new_individual.append(part4[0])
    else:
      new_individual.extend(part4)
  if(len(part5)!=0):
    if(len(part5)==1):
      new_individual.append(part5[0])
    else:
      new_individual.extend(part5)

  return new_individual
	
	
"""Aplica lo mismo que con la mutación. La razón y explicación en el mismo artículo"""
#TODO hay que revisar que funcione correctamente

def order_crossover(ind1, ind2):
    
    repeat = True
    
    while repeat:
        crosspoint = random.randint(0, len(ind1)-1)
        child = ind2[:crosspoint]+ind1[crosspoint:]
        if set(ind1) == set(child):
            repeat = False
  
    return child

def mutate_population(population, chance):
    new_population = []
    for i in population:
        if chance > random.random():
            if fitness_traveler(i) != 0:
                new_population.append(order_mutation(i))
#            new_population.append(insert_mutation[i])
        else:
            new_population.append(i)
    return new_population



    
    
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
    print('MUTACIONEEEEEEEEEEEEEEEEES')
    print('ANTES')
    print(res)
    res = mutate_population(res, chance)
    print('DESPUES')
    print(res)
    return res
    
def most_suited(population):
    pop_len = len(population)
    fitnesses = [None]*pop_len
    for i in range(pop_len):
        fitnesses[i] = fitness_traveler(population[i])
    all = list(zip(fitnesses, population))
    all.sort(key=lambda tup: tup[0], reverse=False)
    sort_pop = [x[1] for x in all]
    suited = sort_pop[0]

    return suited
    
    

def genetic_prob(ages, pop_size, mut_chance, cities):
    
    if(pop_size>1):
      c_len = len(cities)
      
      pop = population(c_len, pop_size)
      
      grade = [None]*ages
      
      for i in range(ages):
          grade[i] = grade_traveler(pop)
          pop = evolve(pop, mut_chance)
          print('EVOLUSAO')
          print(pop)
      
      suited = most_suited(pop)
      
      result = [None]*c_len
      s_dec = decode_traveler(suited)
      
      for i in range(c_len):
          result[i] = s_dec[i].name
      
      return {'population' : pop, 'grades' : grade, 'result' : result}
    else:
      print('THE POPULATION NEEDS TO BE AT LEAST 2. OTHERWISE, IT WILL WITHER AND DIE AS THE DINOSAURS DID.')
   
