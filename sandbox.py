from typing import List
from collections import namedtuple
import json

file = open("times.json")
times = json.loads(file.read())
file.close()

Airport = namedtuple('Airport', ['IATA'])
airportList = [Airport("ANR"),Airport("BRU"),Airport("CRL"),Airport("KJK"),Airport("LGG"), 
               Airport("OST"),Airport("OBL"),Airport("AMS"),Airport("MST"),Airport("EIN"), 
               Airport("GRQ"),Airport("GLZ"),Airport("DHR"),Airport("LEY"),Airport("LWR"),
               Airport("RTM"),Airport("UTC"),Airport("ENS"),Airport("LID"),Airport("WOE"),
               Airport("LUX")]

def from_str_to_route(routeStr: str) -> List[Airport]:
    names = routeStr.split(' -> ')
    return [Airport(name) for name in names]

def get_time(route: List[Airport]) -> float:
    fitness = 0.0
    for i in range(len(route)):
        if i == (len(route) - 1):
            fitness += times[f'{route[i][0]}_to_{route[0][0]}']
        else:
            fitness += times[f'{route[i][0]}_to_{route[i+1][0]}']
    return fitness

def printDetailsOfRoute(routeStr: str):
    route = from_str_to_route(routeStr)
    time = get_time(route)
    print(f'Route (starting with {route[0][0]} and ending with {route[len(route)-1][0]}) takes {time} seconds.')

printDetailsOfRoute('LUX -> LGG -> MST -> EIN -> GLZ -> UTC -> LEY -> ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> WOE -> OBL -> ANR -> BRU -> OST -> KJK -> CRL')