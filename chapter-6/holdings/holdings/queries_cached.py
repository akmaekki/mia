import logging

import requests
from cachetools import cached, TTLCache, LRUCache

logging.basicConfig(level=logging.DEBUG)

class MarketDataClient(object):
    logger = logging.getLogger(__name__)
    cache = TTLCache(maxsize=10, ttl=5*60)
    base_url = 'http://market-data:8000'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__dict__.values())

    def _make_request(self, url):
        response = requests.get(
            f"{self.base_url}/{url}", headers={'content-type': 'application/json'})
        return response.json()

    @cached(cache)
    def all_prices(self):
        self.logger.debug("Making request to get all_prices")
        self.logger.debug(self.cache)
        return self._make_request("prices")

    def price(self, code):
        return self._make_request(f"prices/{code}")
