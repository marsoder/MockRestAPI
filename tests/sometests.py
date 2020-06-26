import unittest
import os,sys
import requests
sys.path.insert(0, "/home/xioahei/Learning/ilovecovid/")
import config

# check if server is running
def check():
    pass

class AppTest(unittest.TestCase):
    def testport(self):
        self.assertEqual(app.port, 5000)
    def testserver(self):
        self.assertEqual(app.server, "flask")

class EndPointTest(unittest.TestCase):
    party_url = "http://localhost:5000/MockAPI/transcript?party=V" 
    speaker_id_url  = "http://localhost:5000/MockAPI/transcript/0888807074321"
    all_url = "http://localhost:5000/MockAPI/transcript"

    def testcollection(self):
        self.assertIsInstance(response, list)
    def party_endpoint(self):
        response = requests.get(self.party_url)
        return self.assertEqual(response.status_code, 200)
    def all_endpoint(self):
        response = requests.get(self.all_url)
        return self.assertEqual(response.status_code, 200)

a = EndPointTest()
a.party_endpoint()
a.all_endpoint()
