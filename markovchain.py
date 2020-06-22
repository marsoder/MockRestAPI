import numpy as np
import requests
import string
import markovify

# collection to transcript?
class M(object):
   def __init__(self, url):
      self.url = url
      # self.get_resource()
      self.resource = self.get_resource()
      self.transcripts = self.transcripts()
      self.model = self.build_model()

   def get_resource(self):
      return requests.get(self.url)
      
   def transcripts(self):
      return [t.get("transcript") for t in self.resource.json()]

   def build_model(self):
      return markovify.Text("".join([t for t in self.transcripts]))

   def generate_transcript(self,quantity = 5):
      return " ".join([self.model.make_sentence() for _ in range(quantity)])
   
response = requests.get("http://localhost:5000/MockAPI/transcript/0888807074321")
url = "http://localhost:5000/MockAPI/transcript/0888807074321"
a = M(url)

def attempt(model):
    return model.make_sentence()
def gen_markov_text(model):
    markov_text = ""
    for _ in range(10):
        m = attempt(model)
        while m is None:
            m = attempt(model)
        markov_text += m
    return markov_text
   
