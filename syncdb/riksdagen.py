import requests
import sys
import re
import json

# Should look into @property


y = "2019%2F20"
class RiksdagenAPI(object):
    """ object for a given parliament year """
    BASE_URL = "https://data.riksdagen.se/anforandelista/"
    def __init__(self, year, size=100000):
        # check whether year is valid, need 
        self.year = year
        self.size = size
        self.url  = f"{self.BASE_URL}?rm={self.year}&anftyp=&d=&ts=&parti=&iid=&sz={size}&utformat=json"
        self.response = None  

    def get_count(self) -> int:
        # in the byte stream, the @antal (count) parameter is on the third line,
        # hence the following code :)
        self.set_response()

        response_iterator = self.response.iter_lines()
        line_counter = 0
        while line_counter != 2:
            next(response_iterator)
            line_counter += 1
        count_line = next(response_iterator).decode("utf-8")
        if "@antal" in count_line:
            return int(re.findall(r"\d+", count_line).pop())
        else:
            return "Something weird happened"


    def get_transcript_ids(self) -> iter:
        self.set_response()
        return (js.get("anforande_id") for js in self.response.json())

        
    def set_response(self) -> None:
        if not self.response:
            self.response = requests.get(self.url, stream=True)
            if self.response.status_code != 200:
                self.response.raise_for_status()

a = RiksdagenAPI(y, size=123123)

# d = requests.get(a.url, stream=True)

# digit_finder = r"\d+"
# s = """   "@antal": "1235","""
# def f():
#     line_counter = 0
#     while line_counter != 2:
#         next(d)
#         line_counter += 1
#     k = next(d).decode("utf-8")
#     if "@antal" in k:
#         return int(re.findall(digit_finder, k))
#     else:
#         return "sumting wong"
#     #return next(d).decode("utf-8")

# for r in f():
#     print(r)
#     try:
#         json.loads(r)
#     except ValueError as e:
#         print(e)
#         continue
    


# with requests.get(a.url, stream=True) as r:
#     for x in r.json():
#         yield x
