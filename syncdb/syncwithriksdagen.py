import sys
import os
import requests
sys.path.insert(0,"..")
from models import Transcript
from riksdagen import RiksdagenAPI
from config import db

a = RiksdagenAPI(size=100)
riksdagen_count = a.count
my_db_count = Transcript().query.count()
riksdagen_ids = a.transcript_ids
db_ids = (x.transcript_id for x in db.session.query(Transcript.transcript_id))

def difference(a,b):
    return set(a) - set(b)

# requests.delete("http://localhost:5000/MockAPI/transcript/testid")


print(difference(db_ids, riksdagen_ids))
print("testid" in set(db_ids))
