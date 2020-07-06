import requests
import sys
import re
import json


class RiksdagenAPI(object):
    """ object for a given parliament year """
    BASE_URL = "https://data.riksdagen.se/anforandelista/"
    def __init__(self, year="2019%2F20", size=100000):
        # check whether year is valid, need 
        self.year = year
        self.size = size
        self.url  = f"{self.BASE_URL}?rm={self.year}&anftyp=&d=&ts=&parti=&iid=&sz={size}&utformat=json"
        # this takes long time for large size values
        # Haven't identified the bottleneck yet
        response = requests.get(self.url)
        if response.status_code != 200:
            response.raise_for_status()
        self.response = response
        
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, number):
        if number < 1:
            raise ValueError("size parameter must be a positive integer")
        self._size = number
        
    @property
    def count(self) -> int:
        count = self.response.json()['anforandelista']['@antal'] 
        return int(count)

    @property
    def transcript_ids(self) -> iter:
        transcripts = self.response.json()['anforandelista']['anforande']
        return (js.get("anforande_id") for js in transcripts)

a = RiksdagenAPI(size=100)
