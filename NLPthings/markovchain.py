import datetime
import requests
import string
import markovify
import json
from models import Transcript, TranscriptSchema


class MarkovChainTranscript(object):
    """  """
    def __init__(self, url):
        self.url = url

    @property
    def collection(self) -> requests.models.Response:
        return requests.get(self.url)

    @property
    def transcripts(self):
        return (t.get("transcript") for t in self.collection.json())

    @property
    def model(self) -> markovify.text.Text:
        return markovify.Text("".join([t for t in self.transcripts]))

    def generate_transcript(self, **kwargs) -> str:
        """ generates new text from all transcripts contained in response body """
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

