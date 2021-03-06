import requests
import sys
import re


class RiksClient(object):
    """ object for a given parliament year used for fetching data from riksdagen
    """

    BASE_URL = "https://data.riksdagen.se/anforandelista/"
    def __init__(self, year="2019%2F20", size=100000):

        self.year = year
        self.size = size
        self.url = f"{self.BASE_URL}?rm={self.year}&anftyp=&d=&ts=&parti=&iid=&sz={size}&utformat=json"

        # this takes long time for large size values
        # Haven't identified the bottleneck yet
        response = requests.get(self.url)
        if response.status_code != 200:
            response.raise_for_status()
        self.response = response

        # make sure response does not containg 0 transcripts
        count_error_message = "0 transcripts in response, make sure year paramter is properly formatted, e.g 2019&2F20"
        assert self.count != 0, count_error_message

        assert self.count != 0, "make sure year parameter correctly formatted"

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
        count = int(count)
        return count

    @property
    def transcript_ids(self) -> iter:
        transcripts = self.response.json()['anforandelista']['anforande']
        return (js.get("anforande_id") for js in transcripts)

    # get the transcripts given set of transcript ids
    def get_transcripts_urls(self, tids):
        documents = self.response.json()['anforandelista']['anforande']
        urls = (js['anforande_url_xml'] +
                '&utformat=json' for js in documents if js.get("anforande_id") in tids)
        return urls
