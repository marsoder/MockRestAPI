from .config import db
from .models import *
import json
from flask import abort, make_response
############### HELPER FUNCTIONS #############


def serialize(db_objects):
    
    if isinstance(db_objects, list):
        return TranscriptSchema(many=True).dump(db_objects)
    else:
        return TranscriptSchema().dump(db_objects)

############### HELPER FUNCTIONS #############


def read_all():
    return serialize(Transcript.query.all())


def read_speaker_id(speaker_id):
    query = Transcript.query.filter(Transcript.speaker_id == speaker_id)

    # check if query is empty
    if query.all():

        return serialize(query.all())
    else:
        abort(404, "Speaker id not found")


def read_filter(**kwargs):
    """  function for parsing queries with parameters  """
    try:
        return serialize(Transcript.query.filter_by(**kwargs).all())
    except:
        return read_all()


def read(**kwargs):
    if not kwargs:
        return read_all()
    else:
        return read_filter(**kwargs)


def post(transcript):
    tid = transcript.get("transcript_id")
    exists = Transcript.query.filter(
        Transcript.transcript_id == tid).one_or_none()

    if exists is None:
        new_transcript = Transcript().from_dict(transcript)
        db.session.add(new_transcript)
        db.session.commit()
        schema = TranscriptSchema()
        return schema.dump(new_transcript), 200
    else:
        return abort(404, f"transcript with id: {tid} already exists")


def delete(transcript_id):
    transcript = Transcript.query.filter(
        Transcript.transcript_id == transcript_id).one_or_none()
    if transcript is not None:
        db.session.delete(transcript)
        db.session.commit()
        return make_response("deleted", 200)
    else:
        return abort(404, "doesnt exist")

def put(transcript_id):
    pass
