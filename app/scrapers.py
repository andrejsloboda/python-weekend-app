import requests
from typing import List, Union
from datetime import datetime
from slugify import slugify
from .settings import settings
from .keys import create_location_key
from .schemas import Route
from .cache import Cache


class RegiojetScraper:
    def __init__(self, cache: Cache) -> None:
        self.locations_url = settings.regiojet_locations_url
        self.base_url = settings.regiojet_base_url
        self.currency_rates = dict()
        self.cities = set()
        self.cache = cache
        self.get_locations()

    def get_locations(self):
        locations = requests.get(self.locations_url)
        for loc in locations.json():
            for city in loc['cities']:
                self.cities.add(city['name'])
                location_key = create_location_key(city['name'])
                if not self.cache.is_in_cache(location_key):
                    self.cache.set_location(location_key, city['id'])
                if city['aliases']:
                    for alias in city['aliases']:
                        self.cities.add(alias)
                        location_key = create_location_key(alias)
                        if not self.cache.is_in_cache(location_key):
                            self.cache.set_location(location_key, city['id'])

    def scrape(self, origin: str, destination: str, dep_date) -> Union[List[Route], None]:
        if dep_date >= datetime.today().date():
            self.get_locations()
            origin_id = self.cache.get_location(create_location_key(origin))
            destination_id = self.cache.get_location(create_location_key(destination))

            payload = {
                'tariffs': 'REGULAR',
                'toLocationType': 'CITY',
                'toLocationId': destination_id,
                'fromLocationType': 'CITY',
                'fromLocationId': origin_id,
                'departureDate': dep_date
            }

            response = requests.get(self.base_url, params=payload).json()
            routes = list()

            for r in response['routes']:
                if r['priceFrom'] > 0:
                    route = Route(
                        origin=slugify(origin),
                        destination=slugify(destination),
                        departure=r['departureTime'],
                        arrival=r['arrivalTime'],
                        carrier="REGIOJET",
                        vehicle_type=r['vehicleTypes'].pop(0),
                        price=r['priceFrom'],
                        currency="EUR",
                        source_id=r['departureStationId'],
                        destination_id=r['arrivalStationId'],
                        free_seats=r['freeSeatsCount'])
                    routes.append(route)
            return routes
        else: 
            return None
