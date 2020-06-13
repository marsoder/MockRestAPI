from config import db
from models import *
import json
def read():
    tscript = Transcript.query.first()
    tscript_schema = TranscriptSchema()
    the_dump = tscript_schema.dump(tscript)
    return the_dump
