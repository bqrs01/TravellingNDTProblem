from typing import NamedTuple

'''class Airport:
  def __init__(self, lat, longi, IATA):
        self.lat = lat
        self.long = longi
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
'''

