import sys

sys.path.insert(0,"./syncdb")
sys.path.insert(0, "/home/xioahei/Learning/MockRiksdagAPI")

from models import Transcript
from riksdagen import RiksYearData
from config import db


def db_count() -> int:
    return Transcript.query.count()
def db_ids() -> set:
    ids = (x.transcript_id for x in db.session.query(Transcript.transcript_id))
    return set(ids)


def synced(riks) -> bool:
    return riks.count == db_count()

def missing(riksobj) -> set:
    riks = set(riksobj.transcript_ids)
    mine = set(x.transcript_id for x in db.session.query(Transcript.transcript_id))
    return riks.difference(mine)

# input paramter is url identifying the transcript to be inserted
def insert_db(url): pass
