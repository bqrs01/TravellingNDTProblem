from datetime import datetime
import json, random, operator
import random
import operator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Here I am following a procedure given by this website: https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
now = datetime(2021, 3, 25)

# Get cached times
cached = True
file = open("times.json")
times = json.loads(file.read())
file.close()

#print(times)

class Airport:
  def __init__(self, lat, longI, IATA):
        self.lat = lat
        self.long = longI
        self.IATA = IATA
  
  def time(self,airport):
    global cached
    global times
    if cached:
        key = f'{self.IATA}_to_{airport.IATA}'
        time = times[key] / 10000
        return time
    else:
        distance_matrix = gmaps.distance_matrix((self.lat,self.long),
                                            (airport.lat,airport.long),
                                            mode="driving",
                                            departure_time=now)
        time = distance_matrix["rows"][0]["elements"][0]["duration"]["value"]
        return time

  def __repr__(self):
    return f'Airport({self.IATA})'

class Fitness:
  def __init__(self,route):
    self.route = route
    self.time = 0
    self.fitness = 0.0

    #if len(self.route) == 0:
    #    raise BaseException("Route can't be empty.")

  # Calculates total time based on a given route
  def routeTime(self):
    if self.time == 0:
      pathTime = 0
      for i in range(0,len(self.route)):
        fromAirport = self.route[i]
        toAirport = None
        if i + 1 < len(self.route):
          toAirport = self.route[i + 1]
        else:
          toAirport = self.route[0]
        pathTime += fromAirport.time(toAirport)
      self.time = pathTime
    return self.time

  # Calculates fitness (number used to rank the routes based on time taken)
  def routeFitness(self):
    if self.fitness == 0:
      #print(f"Calculating route time for {self.route}")
      try:
        routeTime = self.routeTime()
        self.fitness = 1/float(routeTime)
      except:
        #print(routeTime, self.route)
        #print(self)
        pass
    return self.fitness

def createRoute(AirportList):
  route = random.sample(AirportList, len(AirportList))
  return route

def initialPopulation(popsize, AirportList):
  population = []
  for _ in range(popsize):
    population.append(createRoute(AirportList))              
  return population

def rankRoutes(population):
  fitnessResults = {}
  for i in range(len(population)):
    fitnessResults[i] = Fitness(population[i]).routeFitness()
  return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
  selectionResults = []
  df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
  df['cum_sum'] = df.Fitness.cumsum()
  df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
  for i in range(eliteSize):
    selectionResults.append(popRanked[i][0])
  for i in range(len(popRanked) - eliteSize):
    pick = 100*random.random()
  for i in range(len(popRanked)):
    if pick <= df.iat[i,3]:
      selectionResults.append(popRanked[i][0])
      break
  return selectionResults

def matingPool(population, selectionResults):
  matingpool = []
  for i in range(len(selectionResults)):
    index = selectionResults[i]
    matingpool.append(population[index])
  return matingpool

def breed(parent1, parent2):
  child = []
  childP1 = []
  childP2 = []
    
  geneA = int(random.random() * len(parent1))
  geneB = int(random.random() * len(parent1))
    
  startGene = min(geneA, geneB)
  endGene = max(geneA, geneB)

  for i in range(startGene, endGene):
    childP1.append(parent1[i])
    childP2 = [item for item in parent2 if item not in childP1]
    child = childP1 + childP2
  return child

def breedPopulation(matingpool, eliteSize):
  children = []
  length = len(matingpool) - eliteSize
  pool = random.sample(matingpool, len(matingpool))
  for i in range(eliteSize):
    children.append(matingpool[i])
  for i in range(length):
    child = breed(pool[i], pool[len(matingpool)-i-1])
    children.append(child)
  return children

def mutate(individual, mutationRate):
  for swapped in range(len(individual)):
    if (random.random() < mutationRate):
      swapWith = int(random.random() * len(individual))
      city1 = individual[swapped]
      city2 = individual[swapWith]
      individual[swapped] = city2
      individual[swapWith] = city1
  return individual

def mutatePopulation(population, mutationRate):
  mutatedPop = []
  for ind in range(len(population)):
    mutatedInd = mutate(population[ind], mutationRate)
    mutatedPop.append(mutatedInd)
  return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
  popRanked = rankRoutes(currentGen)
  selectionResults = selection(popRanked, eliteSize)
  matingpool = matingPool(currentGen, selectionResults)
  children = breedPopulation(matingpool, eliteSize)
  nextGeneration = mutatePopulation(children, mutationRate)
  return nextGeneration

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
  pop = initialPopulation(popSize, population)
  print("Initial time: " + str(1 / rankRoutes(pop)[0][1]), "seconds.")
  for i in range(generations):
    pop = nextGeneration(pop, eliteSize, mutationRate)
  print("Final time: " + str(1 / rankRoutes(pop)[0][1]), "seconds.")
  bestRouteIndex = rankRoutes(pop)[0][0]
  bestRoute = pop[bestRouteIndex]
  return bestRoute


AirportList = [Airport(51.189400,4.460280,"ANR"),Airport(50.901402,4.484440,"BRU"),Airport(50.459202,4.453820,"CRL"),Airport(50.817200,3.204720,"KJK"),Airport(50.637402,5.443220,"LGG"), 
               Airport(51.198898,2.862220,"OST"),Airport(51.264702,4.753330,"OBL"),Airport(52.308601,4.763890,"AMS"),Airport(50.911701,5.770140,"MST"),Airport(51.450100,5.374530,"EIN"), 
               Airport(53.119701,6.579440,"GRQ"),Airport(51.567402,4.931830,"GLZ"),Airport(52.923401,4.780620,"DHR"),Airport(52.460300,5.527220,"LEY"),Airport(53.228600,5.760560,"LWR"),
               Airport(51.956902,4.437220,"RTM"),Airport(52.127300,5.276190,"UTC"),Airport(52.275833,6.889167,"ENS"),Airport(52.166100,4.417940,"LID"),Airport(51.449100,4.342030,"WOE"),
               Airport(49.623333,6.204444,"LUX")]

#result = geneticAlgorithm(population=AirportList, popSize=500, eliteSize=25, mutationRate=0.01, generations=10000)
#print(result)

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial time: " + str(1 / rankRoutes(pop)[0][1]), "seconds.")
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])
    
    print(pop[0])

    plt.plot(progress)
    plt.ylabel('Time')
    plt.xlabel('Generation')
    plt.show()

geneticAlgorithmPlot(population=AirportList, popSize=100, eliteSize=10, mutationRate=0.01, generations=500)

##airport1 = Airport(52, 4.5, "TES")
##airport2 = Airport(1, 2, "ASR")

##print(airport1.lat, airport2.lat)