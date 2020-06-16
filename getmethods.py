from config import db
from models import *
import json
from flask import abort


def read_all():
    tscript = Transcript.query.all()
    tscript_schema = TranscriptSchema(many=True)
    data = tscript_schema.dump(tscript)
    return data

# exampe speaker id 0888807074321
def read_speaker_id(speaker_id):
    tscript = Transcript.query.filter(Transcript.speaker_id == speaker_id)


    # check if query is empty
    if tscript.all():
        tscript_schema = TranscriptSchema(many=True)
        data = tscript_schema.dump(tscript)
        return data
    else:
        abort(404, "Speaker id not found")
def read_party(party):
    tscript = Transcript.query.filter(Transcript.party == party)
    if tscript.all():
        tscript_schema = TranscriptSchema(many=True)
        data = tscript_schema.dump(tscript)
        return data
    else:
        abort(404, "Nothing found")
