import unittest
import os,sys
sys.path.insert(0, "/home/xioahei/Learning/ilovecovid/")
import config
class AppTest(unittest.TestCase):
    def testport(self):
        self.assertEqual(app.port, 5000)
    def testserver(self):
        self.assertEqual(app.server, "flask")

class EndPointTest(unittest.TestCase):
    response = None
    def testcollection(self):
        self.assertIsInstance(response, list)
