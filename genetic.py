from random import choices, randint, randrange, random, sample
from typing import List, Optional, Callable, Tuple, NamedTuple
import time

Genome = List[object]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], float]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

def generate_genome(objects: List[object]) -> Genome:
    #print(objects)
    #print(objects)
    return sample(objects, k=len(objects))

def generate_population(size: int, objects: List[object]) -> Population:
    #print(objects)
    #([generate_genome(objects) for _ in range(size)])
    #raise BaseException('test')
    population = []
    for _ in range(size):
        population.append(generate_genome(objects))
    return population

def ordered_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    childs = []
    for _ in range(2):
        geneAIndex = int(random()*len(a))
        geneBIndex = int(random()*len(a))
        startIndex = min(geneAIndex, geneBIndex)
        endIndex = max(geneAIndex, geneBIndex)
        childP1 = []
        childP2 = []
        for i in range(startIndex, endIndex):
            childP1.append(a[i])

        childP2 = [c for c in b if c not in childP1]
        child = childP1 + childP2
        childs.append(child)
    c, d = childs
    return (c, d)

def mutation(genome: Genome, num: int = 4, probability: float = 0.01) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        if random() < probability:
            #print('mutated')
            temp = genome[index]
            if index+1 < len(genome):
                genome[index] = genome[index+1]
                genome[index+1] = temp
            else:
                genome[index] = genome[0]
                genome[0] = temp
    
    return genome

def population_fitness(population: Population, fitness_func: FitnessFunc) -> float:
    return sum([fitness_func(genome) for genome in population])

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    )

def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)

def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = ordered_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 200,
    eliteSize: int = 20) -> Tuple[Population, int]:

    population = populate_func()

    fitnesses = []

    for i in range(generation_limit):
        
        print("g =", i)
        
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
        
        
        next_generation = []
        
        for j in range(eliteSize):
            next_generation.append(population[j])

        k=int(eliteSize/2) 

        next_generation = next_generation + sample(population, k=k)

        fitnesses.append(1/fitness_func(next_generation[0]))
        
        for j in range(int(len(population) / 2 - 1)):
            if len(next_generation) >= len(population):
                break
            parents = selection_func(population, fitness_func)
            parents_random = sample(parents, 2)
            offspring_a, offspring_b = crossover_func(parents_random[0], parents_random[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]
        
        #print(len(next_generation))
        population = next_generation
        
    
    return population, i, fitnesses

