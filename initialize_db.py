import sys
import requests
import json
import os
from config import db
from models import Transcript

"""  This script creates the database and populates it with 100 transcripts from 2019/2020 by default  """

if os.path.exists("transcripts.db"):
    os.remove("transcripts.db")
db.create_all()


BASE_URL = "https://data.riksdagen.se/anforandelista/"

def fetch_data(date="2019%2F20", size=100):
    """function that generates urls for resource where texts are"""
    identifier = f"{BASE_URL}?rm={date}&anftyp=&d=&ts=&parti=&iid=&sz={size}&utformat=json"

    js_response = requests.get(identifier).json()[
        'anforandelista']['anforande']
    urls = (js['anforande_url_xml'] + '/json' for js in js_response)
    return urls

def insert_db(urls):
    for url in urls:
        jsresp = json.loads(requests.get(url).content)['anforande']
        t = Transcript()                  
        t.transcript_id = jsresp.get("anforande_id")
        t.transcript = jsresp.get("anforandetext")
        t.speaker_id = jsresp.get("intressent_id")
        t.speaker_title = jsresp.get("talare")
        t.party = jsresp.get("parti")
        t.section = jsresp.get("avsnittsrubrik")
        t.date = jsresp.get("dok_datum")
        db.session.add(t)

if __name__ == "__main__":
    # inserting first batch of data
    print("fetching and inserting first batch of data, might take a while")
    urls = fetch_data()
    insert_db(urls)
    db.session.commit()
