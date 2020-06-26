
from config import db
from models import Transcript, TranscriptSchema
import json
from flask import abort
#from markovchain import devobj
# 
def post(transcript_obj):
    tid = transcript_obj["transcript_id"]
    exists = Transcript.query.filter(Transcript.transcript_id == transcript_obj["transcript_id"]).one_or_none()

    if exists is None:
        schema = TranscriptSchema()
        t = Transcript()
        t = t.from_dict(transcript_obj)
        db.session.add(t)
        db.session.commit()
        schema = TranscriptSchema()
        t = schema.dump(t)
        return t
    else:
        return abort(404, f"transcript with id: {tid} already exists")
