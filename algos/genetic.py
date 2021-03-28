from random import choices, choice, randint, randrange, random, sample
from typing import List, Optional, Callable, Tuple, NamedTuple
from .util import *

# Define types
Genome = List[Airport]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], float]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]


def generate_genome(objects: List[object]) -> Genome:
    """ Function that generates a random genome sample (random list of objects). """
    return sample(objects, k=len(objects))


def generate_population(size: int, objects: List[object]) -> Population:
    """ Function that generates a population of genomes of a given size. """
    return [generate_genome(objects) for _ in range(size)]


def ordered_crossover(a: Genome, b: Genome) -> Genome:
    """ Breeding method that performs ordered crossover given two parents and returns two children (genomes). """
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
    return c


def ero_crossover(a: Genome, b: Genome) -> Genome:
    """ Breeding method that uses edge recombination operator (ERO) given two parents and returns two children (genomes). """
    adj_A = generate_adjacency_matrix(a)
    adj_B = generate_adjacency_matrix(b)
    adj_union = union_of_two_dicts_with_set(adj_A, adj_B)
    N = a[0] if random() < 0.5 else b[0]
    K = [N]
    for _ in range(len(a)-1):
        adj_union = remove_neighbour_from_adj(N, adj_union)
        if len(adj_union[N]) > 0:
            N_ = get_neighbour_with_fewest_adj(adj_union[N], adj_union)
        else:
            N_ = choice([ne for ne in a if ne not in K])
        K.append(N_)
        N = N_
    return K


def mutation_swap(genome: Genome, probability: float = 0.01) -> Genome:
    """ Mutation method that randomly swaps two elements in a genome. """
    num = 1
    for _ in range(num):
        start_index = randrange(len(genome))
        end_index = randrange(len(genome))
        if random() < probability:# and not start_index == end_index:
            temp = genome[start_index]
            genome[start_index] = genome[end_index]
            genome[end_index] = temp
    return genome


def mutation_scramble(genome: Genome, probability: float = 0.01) -> Genome:
    """ Mutation method that randomly scrambles a consecutive set of elements in a genome. """
    start_index = randrange(len(genome))
    end_index = randrange(len(genome))
    min_index, max_index = sorted([start_index, end_index])
    if random() < probability and not min_index == max_index:
        temp = genome[start_index:end_index]
        shuffle(temp)
        genome[start_index:end_index] = temp
    return genome


def population_fitness(population: Population, fitness_func: FitnessFunc) -> float:
    """ Returns fitness of a population. """
    return sum([fitness_func(genome) for genome in population])


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    """ Selection function that selects a pair of parents based on weighted fitness function. """
    return choices(
        population=population,
        weights=[(fitness_func(gene)) for gene in population],
        k=2)


def selection_pair_random(population: Population, fitness_func: FitnessFunc) -> Population:
    """ Selection function that selects a pair of parents randomly. """
    mating_pool = sample(population=population, k=2)
    return mating_pool


def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    """ Sort the genomes in the population based on the fitness function. """
    return sorted(population, key=lambda g: fitness_func(g), reverse=True)


def run_ga(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = ordered_crossover,
    mutation_func: MutationFunc = mutation_swap,
    generation_limit: int = 200,
    elite_size: int = 20,
    mutation_probability_func: Callable[[int],int] = lambda: 0.1) -> Tuple[Population, int]:
    """ Main genetic algorithm method that incorporates and runs the algorithm with given parameters. """

    global bestFitness, fitnessChanged, bestFitnessReason
    population = populate_func()

    for gen in range(generation_limit):
        population = sorted(population, key=fitness_func, reverse=True)
        next_generation = []
        
        for j in range(elite_size):
            next_generation.append(population[j])

        k=int(elite_size/2)
        non_elite = [p for p in population if p not in next_generation]
        next_generation = next_generation + sample(non_elite, k=k)

        for j in range(int(len(population) - 1)):
            if len(next_generation) >= len(population):
                break
            parents = selection_func(population, fitness_func)
            child = crossover_func(parents[0], parents[1])
            child = mutation_func(child, probability=mutation_probability_func(gen))
            next_generation += [child]

        population = next_generation

    return population, gen