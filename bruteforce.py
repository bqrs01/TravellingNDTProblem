from itertools import permutations
from collections import namedtuple
from sandbox import from_str_to_route, from_route_to_str, printDetailsOfRoute
Airport = namedtuple('Airport', ['IATA'])
airportList = [Airport("ANR"),Airport("BRU"),Airport("CRL"),Airport("KJK"),Airport("LGG"), 
               Airport("OST"),Airport("OBL"),Airport("AMS"),Airport("MST"),Airport("EIN"), 
               Airport("GRQ"),Airport("GLZ"),Airport("DHR"),Airport("LEY"),Airport("LWR"),
               Airport("RTM"),Airport("UTC"),Airport("ENS"),Airport("LID"),Airport("WOE"),
               Airport("LUX"),Airport("UDE")]

#BRU -> ANR -> OBL -> WOE -> RTM -> LID -> AMS -> LEY -> DHR -> LWR -> GRQ -> ENS -> UTC -> GLZ -> UDE -> EIN -> MST -> LGG -> LUX -> CRL -> KJK -> OST (fitness=83125.0) in 499 generations

route = from_str_to_route("ANR -> BRU -> OST -> KJK -> CRL -> LUX -> LGG -> MST -> EIN -> GLZ -> UTC -> LEY -> ENS -> GRQ -> LWR -> DHR -> AMS -> LID -> RTM -> WOE -> OBL")

for i in range(len(route)):
    new_route = []
    for j in range(i):
        new_route += route[:i]
    new_route += [Airport('UDE')]
    new_route += route[i+1:]
    printDetailsOfRoute(from_route_to_str(new_route))