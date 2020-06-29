import unittest
import os
import sys
import requests
sys.path.insert(0, "/home/xioahei/Learning/MockRiksdagAPI/")
import config 
from models import TranscriptSchema, Transcript
from markovchain import MarkovChainTranscript

# havent implemented pagination yet, so postponing writing some tests
class HTTPMethodsTest(unittest.TestCase):
    party_url = "http://localhost:5000/MockAPI/transcript?party=V"
    speaker_id_url = "http://localhost:5000/MockAPI/transcript/0992800527915"
    all_url = "http://localhost:5000/MockAPI/transcript"

    dummy_transcript = None
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
        # bad test need fix
        a = MarkovChainTranscript(self.speaker_id_url).to_transcript("test_id")
        t = TranscriptSchema()
        a = t.dump(a)
        r = requests.post(self.all_url, json=a)
        return self.assertEqual(r.status_code, 200)

    def test_delete(self):
        r = requests.delete(self.all_url + "/test_id")
        return self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()
