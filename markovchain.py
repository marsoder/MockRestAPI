import datetime
import requests
import string
import markovify
import json
from models import Transcript, TranscriptSchema


class MarkovChainTranscript(object):
    def __init__(self, url):
        self.url = url
        self.collection = self.get_collection()
        self.transcripts = self.transcripts()
        self.model = self.build_model()

    def get_collection(self):
        """ return collection of transcripts associated with speaker_id in url constructor parameter """
        return requests.get(self.url)

    def transcripts(self):
        """ return array of transcripts from url """
        return [t.get("transcript") for t in self.collection.json()]

    def build_model(self):
        """ build model from transcripts for generating new text """
        return markovify.Text("".join([t for t in self.transcripts]))

    def generate_transcript(self, **kwargs):
        """ generates new text from all transcripts contained in collection """
       # if quantity not specified, defaults to 5
       # make_sentece attempts to make valid sentence, and raises a TypeError
       # if it fails, hence the except
        quantity = kwargs.get(
            "quantity") if "quantity" in kwargs.keys() else 5
        try:
            fake = " ".join([self.model.make_sentence()
                             for _ in range(quantity)])
        except TypeError:
            fake = self.generate_transcript(quantity=quantity)
        return fake

    def to_transcript(self, new_id) -> Transcript:
        """ returns transcript database object with fake markov generated text """
        js = self.collection.json().pop()
        # create transcript object from first transcript in collection
        fake_transcript = Transcript().from_dict(js)
        # replace fields
        fake_transcript.transcript = self.generate_transcript(quantity=10)
        fake_transcript.transcript_id = new_id
        fake_transcript.date = str(datetime.datetime.now())
        return fake_transcript


u = "http://localhost:5000/MockAPI/transcript/0888807074321"
#devobj = MarkovChainTranscript(u).to_transcript()
