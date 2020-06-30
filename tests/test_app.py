import unittest
import os
import sys
import requests
import json
sys.path.insert(0, "/home/xioahei/Learning/MockRiksdagAPI/")
import config 
from models import TranscriptSchema, Transcript
from markovchain import MarkovChainTranscript
from werkzeug import exceptions


# havent implemented pagination yet, so postponing writing some tests
class HTTPMethodsTest(unittest.TestCase):
    party_url = "http://localhost:5000/MockAPI/transcript?party=V"
    speaker_id_url = "http://localhost:5000/MockAPI/transcript/0992800527915"
    all_url = "http://localhost:5000/MockAPI/transcript"
    dummy_transcript = json.loads(open("/home/xioahei/Learning/MockRiksdagAPI/tests/test-transcript.txt", "r").read())

    def test_party_status(self):
        response = requests.get(self.party_url)
        return self.assertEqual(response.status_code, 200)

    def test_party_content(self):
        response = requests.get(self.party_url)
        all_true = all(js.get("party") == "V" for js in response.json())
        return self.assertTrue(all_true)
    
    def test_all(self):
        response = requests.get(self.all_url)
        return self.assertEqual(response.status_code, 200)

    def test_speaker_id_status(self):
        response = requests.get(self.speaker_id_url)
        all_true = all(js.get("speaker_id") == "0992800527915" for js in response.json())
        return self.assertTrue(all_true)
    
    def test_post(self):
        schema = TranscriptSchema()
        data = schema.dump(self.dummy_transcript)
        response = requests.post(self.all_url, json=data)
        return self.assertEqual(response.status_code, 200)

    def test_already_in_db(self):
        schema = TranscriptSchema()
        data = schema.dump(self.dummy_transcript)
        response = requests.post(self.all_url, json=data)
        return self.assertRaises(exceptions.NotFound)
    def test_dummy_in_db(self):
        questionmark = Transcript.query.filter(Transcript.transcript_id=="testid").one_or_none()
        return self.assertFalse(questionmark is not None)

        
    def test_delete_not_existing(self):
        r = requests.delete(self.all_url + "/135098u51")
        return self.assertRaises(exceptions.NotFound)
    def test_delete(self):
        response = requests.delete(self.all_url)
        return self.assertEqual(response.status_code, 200)
    def test_delete_success(self):
         questionmark = Transcript.query.filter(Transcript.transcript_id=="testid").one_or_none()
         return self.assertFalse(questionmark is None)
if __name__ == "__main__":
    unittest.main()
