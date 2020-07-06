from connexion import App
import os
import pytest
import sys
import requests
import json

# appending necessary otherwise ModuleNotFoundError is raised due to not finding httpmethods
sys.path.append("..")

SWAGGER_PATH = "/home/xioahei/Learning/MockRiksdagAPI"

from config import fapp, connex_app
from models import Transcript, TranscriptSchema, db
connex_app.add_api("ParlSpeeches.yml")
fapp.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:////' + SWAGGER_PATH + "/tests/test-db.db"

# reads json from file and converts into Transcript object
f = open("test-transcript.txt", "r").read()
js = json.loads(f)
ts = Transcript().from_dict(js)
 
@pytest.fixture(scope="module")
def app():
    with fapp.test_client() as c:
        db.create_all()
        # adds transcript to database before every test for testing endpoints
        db.session.add(ts)
        db.session.commit()
        yield c
        db.drop_all()

def test_transcript(app) -> None:
    response = app.get("MockAPI/transcript")
    assert response.status_code == 200

def test_party(app) -> None:
    response = app.get("MockAPI/transcript?party=")
    assert response.status_code == 200
def test_party_correct_party(app):
    response = app.get("MockAPI/transcript?party=S")
    transcript = response.get_json().pop()
    assert transcript.get("party") == "S"
def test_speaker_id(app):
    response = app.get("MockAPI/transcript/testspeakerid")
    assert response.status_code == 200
    
def test_speaker_id_not_found(app):
    response = app.get("MockAPI/transcript/nonexistingspeakerid")
    assert response.status_code == 404
    
def test_post(app):

    ts.transcript_id = "newid"
    data = TranscriptSchema().dump(ts)
    response = app.post("MockAPI/transcript", json=data)
    assert response.status_code == 200

def test_post_id_already_exists(app):
    data = TranscriptSchema().dump(ts)
    response = app.post("MockAPI/transcript", json=data)
    assert response.status_code == 404
    
def test_delete(app):
    response = app.delete("MockAPI/transcript/testid")
    assert response.status_code == 200

def test_delete_not_existing(app):
    response = app.delete("MockAPI/transcript/nonexistingid")
    assert response.status_code == 404
