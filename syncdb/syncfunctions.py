import datetime
import sys
import asyncio
sys.path.insert(0, "./syncdb")
sys.path.insert(0, "/home/xioahei/Learning/MockRiksdagAPI")
from config import db
from riksdagen import RiksClient
from models import Transcript
import json
import requests


fields_eng_swe_map = {"anforande_id": "transcript_id", "talare": "speaker_title", "parti": "party", "dok_datum": "date", "avsnittsrubrik": "section", "intressent_id": "speaker_id"}
    
def db_count() -> int:
    return Transcript.query.count()


def db_ids() -> set:
    ids = (x.transcript_id for x in db.session.query(Transcript.transcript_id))
    return set(ids)


def synced(riks) -> bool:
    return riks.count == db_count()
    
def missing_transcripts(riksobj) -> set:
    riks = set(riksobj.transcript_ids)
    mine = set(x.transcript_id for x in db.session.query(
        Transcript.transcript_id))
    return riks.difference(mine)


def filter_and_translate(d):
    """ return the dictionary d with correct schema """
    return {fields_eng_swe_map[k]:v for k,v in d.items() if k in fields_eng_swe_map}


def insert_db(urls) -> None:
    
    for url in urls:
        js = json.loads(requests.get(url).content)['anforande']
        transcript = filter_and_translate(js)
        transcript = Transcript().from_dict(transcript)
        db.session.add(transcript)

def sync(riks):
    missing_ids = missing_transcripts(riks)
    missing_urls = riks.get_transcripts_urls(missing_ids)
    insert_db(missing_urls)
    db.session.commit()
