from typing import Dict, List, Set, Tuple
from random import shuffle, sample
from collections import namedtuple
import json

file = open("data/times.json")
times = json.loads(file.read())
file.close()

Airport = namedtuple('Airport', ['IATA'])

def from_str_to_route(routeStr: str) -> List[Airport]:
    names = routeStr.split(' -> ')
    return [Airport(name) for name in names]

def from_route_to_str(route: List[Airport]) -> str:
    names = [b[0] for b in route]
    return ' -> '.join(names)

def get_time(route: List[Airport]) -> float:
    fitness = 0.0
    for i in range(len(route)):
        if i == (len(route) - 1):
            fitness += times[f'{route[i][0]}_to_{route[0][0]}']
        else:
            fitness += times[f'{route[i][0]}_to_{route[i+1][0]}']
    return fitness

def generate_adjacency_matrix(a: List[object]) -> Dict[object, Set]:
    adjacency_matrix = {}
    for i in range(len(a)):
        previous, nex = (i-1, i+1)
        nex = 0 if (nex == len(a)) else nex
        adjacency_matrix[a[i]] = set([a[i] for i in [previous, nex]])
    return adjacency_matrix

def union_of_two_dicts_with_set(a: Dict[object, Set], b: Dict[object, Set]) -> Dict[object, Set]:
    c = {}
    for key in a.keys():
        setA = a[key]
        setB = b[key]
        union_set = setA.union(setB)
        c[key] = union_set
    return c

def remove_neighbour_from_adj(neighbour: object, adj: Dict[object, Set]) -> Dict[object, Set]:
    for adj_set in adj.values():
        adj_set.discard(neighbour)
    return adj

def get_neighbour_with_fewest_adj(neighbors_list: Set[object], adj_dict: Dict[object, Set]) -> object:
    adj_list: List[Tuple[object, Set]] = [(ne, adj_dict[ne]) for ne in neighbors_list]
    shuffle(adj_list)
    sorted_adj_list = sorted(adj_list, key=lambda item: len(item[1]))
    return sorted_adj_list[0][0]

# if __name__ == "__main__":
#     a = generate_adjacency_matrix([1, 2, 3, 4])
#     b = generate_adjacency_matrix([2, 1, 3, 4])
#     c = (union_of_two_dicts_with_set(a, b))
#     d = (remove_neighbour_from_adj(3, c))
#     e = (get_neighbour_with_fewest_adj(d[1], d))