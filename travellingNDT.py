from collections import namedtuple
from math import exp
from functools import partial
from algos.genetic import *
import json, matplotlib.pyplot as plt, time, random
from algos.util import *

# Define data types to be used
Airport = namedtuple('Airport', ['IATA'])
AirportWithLoc = namedtuple('AirportWithLoc', ['lat', 'longi', 'IATA'])

# Initialise and fill airportList and airportListWithLoc
airportList = [Airport("ANR"),Airport("BRU"),Airport("CRL"),Airport("KJK"),Airport("LGG"), 
               Airport("OST"),Airport("OBL"),Airport("AMS"),Airport("MST"),Airport("EIN"), 
               Airport("GRQ"),Airport("GLZ"),Airport("DHR"),Airport("LEY"),Airport("LWR"),
               Airport("RTM"),Airport("UTC"),Airport("ENS"),Airport("LID"),Airport("WOE"),
               Airport("LUX"), Airport("UDE")]

airportListWithLoc = [AirportWithLoc(51.189400,4.460280,"ANR"),AirportWithLoc(50.901402,4.484440,"BRU"),AirportWithLoc(50.459202,4.453820,"CRL"),AirportWithLoc(50.817200,3.204720,"KJK"),AirportWithLoc(50.637402,5.443220,"LGG"), 
               AirportWithLoc(51.198898,2.862220,"OST"),AirportWithLoc(51.264702,4.753330,"OBL"),AirportWithLoc(52.308601,4.763890,"AMS"),AirportWithLoc(50.911701,5.770140,"MST"),AirportWithLoc(51.450100,5.374530,"EIN"), 
               AirportWithLoc(53.119701,6.579440,"GRQ"),AirportWithLoc(51.567402,4.931830,"GLZ"),AirportWithLoc(52.923401,4.780620,"DHR"),AirportWithLoc(52.460300,5.527220,"LEY"),AirportWithLoc(53.228600,5.760560,"LWR"),
               AirportWithLoc(51.956902,4.437220,"RTM"),AirportWithLoc(52.127300,5.276190,"UTC"),AirportWithLoc(52.275833,6.889167,"ENS"),AirportWithLoc(52.166100,4.417940,"LID"),AirportWithLoc(51.449100,4.342030,"WOE"),
               AirportWithLoc(49.623333,6.204444,"LUX"),AirportWithLoc(51.656400,5.708611,"UDE")]

# Get the data file with travel time between two airports
file = open("data/times.json")
times = json.loads(file.read())
file.close()

def fitness_route(genome: Genome) -> float:
    """ Returns fitness of a genome. """
    fitness = 0.0
    for i in range(len(genome)):
        if i == (len(genome) - 1):
            fitness += times[f'{genome[i][0]}_to_{genome[0][0]}']
        else:
            fitness += times[f'{genome[i][0]}_to_{genome[i+1][0]}']
    return 1/fitness

def travelling_NDT_mutation_probability(gens: int) -> float:
    """ Variable mutation probability function. """
    return (1 - exp(-0.001*gens))

def printResults(population, generations):
        sortedPopulation = sort_population(population, fitness_route)
        bestSolution = sortedPopulation[0]
        bestSolutionList = [b[0] for b in bestSolution]
        bestSolutionStr = ' -> '.join(bestSolutionList)
        fitness = 1/fitness_route(bestSolution)
        print(f'{bestSolutionStr} \n(fitness={fitness}) in {generations} generations')

if __name__ == "__main__":
    # Main function: run ga and get final population and number of generations run
    population, generations = run_ga(
        partial(generate_population, size=200, objects=airportList),
        fitness_route,
        selection_pair_random,
        ero_crossover,
        mutation_scramble,
        generation_limit=300,
        elite_size=20,
        mutation_probability_func=travelling_NDT_mutation_probability
    )
    # Print results to console
    printResults(population, generations)