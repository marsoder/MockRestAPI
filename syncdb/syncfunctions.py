import datetime
import sys
import json
import requests

from RiksApp.config import db
from RiksApp.models import Transcript
from .riksdagen import RiksClient


fields_eng_swe_map = {"anforande_id": "transcript_id","anforandetext" : "transcript", "talare": "speaker_title", "parti": "party", "dok_datum": "date", "avsnittsrubrik": "section", "intressent_id": "speaker_id"}
    
def db_count() -> int:
    return Transcript.query.count()


def db_ids() -> set:
    ids = (x.transcript_id for x in db.session.query(Transcript.transcript_id))
    return set(ids)


def synced(riks) -> bool:
    return riks.count == db_count()
    
def unsynced_transcripts(riksobj) -> (set,str):
    riks = set(riksobj.transcript_ids)
    mine = set(x.transcript_id for x in db.session.query(
        Transcript.transcript_id))

    if len(riks) > len(mine):
        return riks.difference(mine), "update"
    else:
        return mine.difference(riks), "delete"

    
def filter_and_translate(d) -> dict:
    """ return the dictionary d with correct schema """
    return {fields_eng_swe_map[k]:v for k,v in d.items() if k in fields_eng_swe_map.keys()}

def remove_db(ids) -> None:
    for id_ in ids:
        t = Transcript.query.filter(Transcript.transcript_id == id_).first()
        db.session.delete(t)
        
def insert_db(urls) -> None:
    
    for url in urls:
        js = json.loads(requests.get(url).content)['anforande']
        transcript = filter_and_translate(js)
        transcript = Transcript().from_dict(transcript)
        # bandaid fix
        db.session.add(transcript)

def sync(riks) -> None:
    unsynced_ids, operation = unsynced_transcripts(riks)
    if operation == "update":
        missing_urls = riks.get_transcripts_urls(missing_ids)
        insert_db(missing_urls)
    if operation == "delete":
        remove_db(unsynced_ids)
    db.session.commit()
