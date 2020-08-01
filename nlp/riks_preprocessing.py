import nltk
from nltk.corpus import stopwords
import string
import re
import sys
import json
import scipy
import textblob
with open("/home/xioahei/Learning/MockRiksdagAPI/tests/test-transcript.txt", "r") as f:
    s = f.read()
    global d
    d = json.loads(s).get("transcript")
    
stopwords = stopwords.words("swedish")
translate_table = dict((ord(char), None) for char in string.punctuation)  
stopwords_translate_table = dict((word, None) for word in stopwords)



# functions
        
# remove noise
def remove_noise(text) -> str:
    return text.translate(translate_table)

# remove tags
def remove_tags(text) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', text)
    return cleantext

def remove_stopwords(text) -> str:
    return text.translate(stopwords_translate_table)
f = [remove_tags, remove_noise, remove_stopwords]
def compose(data, functions):
    for f in functions:
        data = f(data)
    return data

def pre_processing(df,fs):
    return df.applymap(lambda x: compose(x,fs))
