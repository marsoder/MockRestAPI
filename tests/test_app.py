# from json import JSONEncoder
from connexion import App
import os
import pytest
import sys
import requests
import json


# Need to create db just for testing ...

# appending necessary otherwise ModuleNotFoundError is raised due to not finding httpmethods
sys.path.append("..")
# from models import Transcript, TranscriptSchema
# abs_path = os.path.abspath(__file__)

SWAGGER_PATH = "/home/xioahei/Learning/MockRiksdagAPI"

from config import fapp, connex_app
from models import Transcript, TranscriptSchema, db
# fapp = App(__name__, specification_dir=SWAGGER_PATH)
# fapp.add_api("ParlSpeeches.yml")
connex_app.add_api("ParlSpeeches.yml")
fapp.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:////' + SWAGGER_PATH + "/tests/test-db.db"

@pytest.fixture(scope="module")
def app():
    with fapp.test_client() as c:
        db.create_all()
        yield c
        db.drop_all()

def test_transcript(app) -> None:
    response = app.get("MockAPI/transcript")
    assert response.status_code == 200

def test_party(app):
    response = app.get("MockAPI/transcript?party=V")
    assert response.status_code == 200
    
def test_post(app):

    f = open("test-transcript.txt", "r").read()
    js = json.loads(f)
    ts = Transcript().from_dict(js)
    a = TranscriptSchema().dump(ts)
    response = app.post("MockAPI/transcript", json=a)
    assert response.status_code == 200
    
def test_delete(app): pass
    
def test_delete(app): pass
