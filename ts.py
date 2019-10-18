#!/usr/bin/python

import urllib
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import re


def get_vID(ch_URL):
    x = urllib.request.urlopen(ch_URL)
    html = x.read()
    soup = BeautifulSoup(html, "html5lib")
    textSoup = soup.get_text(strip=True)
    rePat = r'HomeVideosPlaylistsCommunityChannelsAbout(.*)yt.setConfig'
    temp = re.search(rePat, textSoup).group(1)
    temp = re.search(r'\[\{(.*)\}\]', temp).group(1)
    #table = re.search(r'\{(.*)', temp.group(1)).group(1)
    #table = '{' + table
    #table = table.split(',')
    itemTable = re.findall(r'\"position(.*)\}', temp)
    urlTable = re.findall(r'\"url(.*)\}', temp)
    print(urlTable)
    vID = {} 

def getTS(vID):
    ts = YouTubeTranscriptApi.get_transcript(vID)
    print(ts)

ch_URL = 'https://www.youtube.com/user/professormesser'
get_vID(ch_URL)
#vID = '29djfdomUYM'
#getTS(vID)

#vfl3z5WfW

#2102920123