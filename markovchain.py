import requests
import string
import markovify
import json
from models import Transcript,TranscriptSchema


class MarkovChainTranscript(object):
    def __init__(self, url):
        self.url = url
        self.resource = self.get_resource()
        self.transcripts = self.transcripts()
        self.model = self.build_model()

    def get_resource(self):
        return requests.get(self.url)

    def transcripts(self):
        # transcripts from which fake ones are generated
        return [t.get("transcript") for t in self.resource.json()]

    def build_model(self):
        return markovify.Text("".join([t for t in self.transcripts]))

    def generate_transcript(self, **kwargs):
       # if quantity not specified, defaults to 5
       # high quantity not recommended
        quantity = kwargs.get(
            "quantity") if "quantity" in kwargs.keys() else 5
        try:
            fake = " ".join([self.model.make_sentence()
                             for _ in range(quantity)])
        except TypeError:
            fake = self.generate_transcript(quantity=quantity)
        return fake

    def to_transcript(self, new_id):
        js = self.resource.json()[0]
        t = Transcript()
        t.from_dict(js)
        t.transcript = self.generate_transcript(quantity = 10)
        t.transcript_id = new_id
        schema = TranscriptSchema()
        return t

u = "http://localhost:5000/MockAPI/transcript/0888807074321"
#devobj = MarkovChainTranscript(u).to_transcript()
