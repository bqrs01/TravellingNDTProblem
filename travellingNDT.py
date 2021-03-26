from collections import namedtuple
from functools import partial
from genetic import run_evolution, generate_population, selection_pair, ordered_crossover, mutation, Genome, sort_population
import json, matplotlib.pyplot as plt, time, random

Airport = namedtuple('Airport', ['IATA'])
airportList = [Airport("ANR"),Airport("BRU"),Airport("CRL"),Airport("KJK"),Airport("LGG"), 
               Airport("OST"),Airport("OBL"),Airport("AMS"),Airport("MST"),Airport("EIN"), 
               Airport("GRQ"),Airport("GLZ"),Airport("DHR"),Airport("LEY"),Airport("LWR"),
               Airport("RTM"),Airport("UTC"),Airport("ENS"),Airport("LID"),Airport("WOE"),
               Airport("LUX"), Airport("UDE")]

file = open("times.json")
times = json.loads(file.read())
file.close()

highest_time = 0.0
it = 0.01
it_remembers = 0.0

def fitness_route(genome: Genome) -> float:
    #start_time = time.time()
    #print(type(genome))
    #if genome is None:
    #    return 100000000
    #start_time = time.time()
    fitness = 0.0
    for i in range(len(genome)):
        if i == (len(genome) - 1):
            fitness += times[f'{genome[i][0]}_to_{genome[0][0]}']
        else:
            fitness += times[f'{genome[i][0]}_to_{genome[i+1][0]}']
    #highest_time = max(time.time()-start_time, highest_time)
    #if random.random() < it:
    #    if not it_remembers == highest_time:
    #        print(highest_time)
    #        it_remembers = highest_time
    #print(time.time() - start_time)
    return 1/fitness

print(' -> '.join(['1', '2']))

try:
    population, generations, fitnesses = run_evolution(
        partial(generate_population, size=200, objects=airportList),
        fitness_route,
        selection_pair,
        ordered_crossover,
        mutation,
        generation_limit=300,
        eliteSize=20
    )
except KeyboardInterrupt:
    print(highest_time)

def printResults(population, generations):
    sortedPopulation = sort_population(population, fitness_route)
    bestSolution = sortedPopulation[0]
    bestSolutionList = [b[0] for b in bestSolution]
    bestSolutionStr = ' -> '.join(bestSolutionList)
    fitness = 1/fitness_route(bestSolution)
    print(f'{bestSolutionStr} (fitness={fitness}) in {generations} generations')

printResults(population, generations)

plt.plot(fitnesses)
plt.ylabel('Time')
plt.xlabel('Generation')
plt.show()

#EIN -> GLZ -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> OBL -> WOE -> ANR -> KJK -> OST -> BRU -> CRL -> LUX -> LGG -> MST (fitness=81750.0) in 349 generations
#ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> GLZ -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU -> ANR -> OBL -> WOE -> UTC -> LEY (fitness=80766.0) in 499 generations
#GLZ -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU -> ANR -> OBL -> WOE (fitness=80482.0) in 699 generations
#CRL -> LUX -> LGG -> MST -> ANR -> WOE -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> EIN -> GLZ -> OBL -> BRU -> OST -> KJK (fitness=81584.0) in 1499 generations
#BRU -> OBL -> ANR -> WOE -> LID -> AMS -> LEY -> DHR -> LWR -> GRQ -> ENS -> UTC -> RTM -> GLZ -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST (fitness=82525.0) in 599 generations
#CRL -> KJK -> OST -> BRU -> ANR -> OBL -> WOE -> RTM -> AMS -> LEY -> ENS -> GRQ -> LWR -> DHR -> LID -> UTC -> GLZ -> EIN -> MST -> LGG -> LUX (fitness=82879.0) in 299 generations
#LUX -> LGG -> MST -> EIN -> GLZ -> UTC -> LEY -> ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> WOE -> OBL -> ANR -> BRU -> OST -> KJK -> CRL (fitness=79222.0) in 499 generations
#ANR -> OBL -> WOE -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> GLZ -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU (fitness=79222.0) in 499 generations
#CRL -> LUX -> LGG -> MST -> EIN -> GLZ -> UTC -> LEY -> ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> WOE -> OBL -> ANR -> BRU -> OST -> KJK (fitness=79222.0) in 299 generations
#ANR -> BRU -> OST -> KJK -> CRL -> LUX -> LGG -> MST -> EIN -> GLZ -> UTC -> LEY -> ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> WOE -> OBL (fitness=79222.0) in 1999 generations

#BRU -> ANR -> OBL -> WOE -> RTM -> LID -> AMS -> LEY -> DHR -> LWR -> GRQ -> ENS -> UTC -> GLZ -> UDE -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST (fitness=83125.0) in 499 generations
#OST -> KJK -> CRL -> LUX -> LGG -> MST -> GLZ -> UTC -> LEY -> AMS -> RTM -> LID -> DHR -> LWR -> GRQ -> ENS -> UDE -> EIN -> OBL -> WOE -> ANR -> BRU (fitness=84922.0) in 499 generations
#MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU -> WOE -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> UDE -> EIN -> GLZ -> OBL -> ANR (fitness=83682.0) in 299 generations
#LUX -> CRL -> KJK -> OST -> BRU -> ANR -> OBL -> WOE -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> GLZ -> UDE -> EIN -> MST -> LGG (fitness=82426.0) in 299 generations
#LEY -> UTC -> AMS -> LID -> RTM -> WOE -> ANR -> BRU -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> OBL -> GLZ -> EIN -> UDE -> ENS -> GRQ -> LWR -> DHR (fitness=84906.0) in 299 generations
#LEY -> UTC -> UDE -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU -> ANR -> WOE -> OBL -> GLZ -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS (fitness=82475.0) in 499 generations
#GLZ -> UDE -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU -> ANR -> OBL -> WOE -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC (fitness=82426.0) in 499 generations
#GLZ -> UTC -> LEY -> ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> WOE -> OBL -> ANR -> BRU -> OST -> KJK -> CRL -> LUX -> LGG -> MST -> EIN -> UDE (fitness=82426.0) in 299 generations
#ANR -> OBL -> WOE -> RTM -> LID -> AMS -> DHR -> LWR -> GRQ -> ENS -> LEY -> UTC -> GLZ -> UDE -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST -> BRU (fitness=82426.0) in 2999 generations