import os
import pytest
import sys
import requests
import json

# appending necessary otherwise ModuleNotFoundError is raised due to not finding httpmethods
sys.path.append("..")

BASE_DIR = "/home/xioahei/Learning/MockRiksdagAPI"

from config import flask_app, connex_app
from models import Transcript, TranscriptSchema, db
connex_app.add_api("ParlSpeeches.yml")
flask_app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:////' + BASE_DIR + "/tests/test-db.db"
 
@pytest.fixture(scope="module")
def app_test():
    """ yields a test app with a test database that contains one test transcrip where transcript_id = testid, party=S, speaker_id = testspeakerid"""
 
# reads json from file and converts into Transcript object
    with open("test-transcript.txt", "r") as f:
        content = f.read()
        js = json.loads(content)
        global mock_transcript
        mock_transcript = Transcript().from_dict(js)
    with flask_app.test_client() as c:
        db.create_all()
        # adds transcript to database before every test for testing endpoints
        db.session.add(mock_transcript)
        db.session.commit()
        yield c
        db.drop_all()

def test_transcript(app_test) -> None:
    response = app_test.get("MockAPI/transcript")
    assert response.status_code == 200

def test_party(app_test) -> None:
    response = app_test.get("MockAPI/transcript?party=")
    assert response.status_code == 200
def test_party_correct_party(app_test):
    response = app_test.get("MockAPI/transcript?party=S")
    transcript = response.get_json().pop()
    assert transcript.get("party") == "S"
def test_speaker_id(app_test):
    response = app_test.get("MockAPI/transcript/testspeakerid")
    assert response.status_code == 200
    
def test_speaker_id_not_found(app_test):
    response = app_test.get("MockAPI/transcript/nonexistingspeakerid")
    assert response.status_code == 404
    
def test_post(app_test):
    
    mock_transcript.transcript_id = "newid"
    data = TranscriptSchema().dump(mock_transcript)
    response = app_test.post("MockAPI/transcript", json=data)
    assert response.status_code == 200

def test_post_id_already_exists(app_test):
    data = TranscriptSchema().dump(mock_transcript)
    response = app_test.post("MockAPI/transcript", json=data)
    assert response.status_code == 404
    
def test_delete(app_test):
    response = app_test.delete("MockAPI/transcript/testid")
    assert response.status_code == 200

def test_delete_not_existing(app_test):
    response = app_test.delete("MockAPI/transcript/nonexistingid")
    assert response.status_code == 404
