from config import db
from models import *
import json
from flask import abort

def serialize(db_objects):
    schema = TranscriptSchema(many=True)
    return schema.dump(db_objects)

def read_all():
    tscript = Transcript.query.all()
    tscript_schema = TranscriptSchema(many=True)
    data = tscript_schema.dump(tscript)
    return data

# example speaker id 0888807074321
def read_speaker_id(speaker_id):
    """ serve all data in database """
    tscript = Transcript.query.filter(Transcript.speaker_id == speaker_id)


    # check if query is empty
    if tscript.all():

        return serialize(tscript)
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
def read_filter(**kwargs):
    try:
        return serialize(Transcript.query.filter_by(**kwargs))
    except:
        return read_all()
def read(**kwargs):
    if not kwargs:
        return read_all()
    else:
        return read_filter(**kwargs)

