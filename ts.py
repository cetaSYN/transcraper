#!/usr/bin/python

import urllib
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import re

def main():
    ch_URL = 'https://www.youtube.com/user/professormesser'
    video_id_table = get_vID(ch_URL)
    code = getTS(video_id_table[4])
    if (len(code) > 0):
        print(code)
    else:
        print("No code found in most recent video")


def get_vID(ch_URL):
    x = urllib.urlopen(ch_URL)
    html = x.read()
    soup = BeautifulSoup(html, "lxml")
    textSoup = soup.get_text(strip=True)
    rePat = r'HomeVideosPlaylistsCommunityChannelsAbout(.*)yt.setConfig'
    temp = re.search(rePat, textSoup).group(1)
    urlTable = re.findall(r'watch\?v=.+?(?=\")', temp)
    newTable = []
    for url in urlTable:
        tmp = url.encode("ascii")
        tmp = tmp.replace('watch?v=', '')
        newTable.append(tmp)
    return(newTable)

def getTS(vID):
    ts = YouTubeTranscriptApi.get_transcript(vID)
    hit = []
    code = ''
    for line in ts:
        if ("super secret code word" in line["text"]):
            hit.append(ts.index(line))
    for hits in hit:
        code = code + '\n'
        code = code + str(ts[hits]["start"]) + ":" + " "
        code = code + ts[hits - 6]["text"] + " "
        code = code + ts[hits - 5]["text"] + " "
        code = code + ts[hits - 4]["text"] + " "
        code = code + ts[hits - 3]["text"] + " "
        code = code + ts[hits - 2]["text"] + " "
        code = code + ts[hits - 1]["text"] + " "
        code = code + ts[hits]["text"] + " "
        code = code + ts[hits + 1]["text"] + " "
        code = code + ts[hits + 2]["text"] + " "
        code = code + ts[hits - 3]["text"] + " "
        code = code + ts[hits - 4]["text"] + " "
        code = code + ts[hits - 5]["text"] + " "
        code = code + ts[hits - 6]["text"] + " "
        code = code + '\n\n'
    return(code)

if __name__== "__main__":
  main()