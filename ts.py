#!/usr/bin/python

import urllib
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup

def get_vID(ch_URL):
    x = urllib.request.urlopen(ch_URL)
    x = BeautifulSoup(x, 'html.parser')
    print(x)

def getTS(vID):
    ts = YouTubeTranscriptApi.get_transcript(vID)
    print(ts)

ch_URL = 'https://www.youtube.com/user/professormesser'
get_vID(ch_URL)
#vID = '29djfdomUYM'
#getTS(vID)