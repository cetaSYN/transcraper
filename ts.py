#!/usr/bin/env python3

from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from os import path
from re import search, findall
from urllib.request import urlopen
from time import sleep


def main():
    while True:
        get_secret_code()
        sleep(86400)


def get_secret_code():
    ch_URL = 'https://www.youtube.com/user/professormesser'
    video_id_table = get_vID(ch_URL)
    code = getTS(video_id_table[4])
    if (len(code) <= 0):
        print("No code found in most recent video")
    if not path.exists(('./videos/' + str(video_id_table[4]))):
        f = open(('./videos/' + str(video_id_table[4])), "w")
        f.write(code)
        f.close()
    else:
        print("Video Already Parsed")


def get_vID(ch_URL):
    x = urlopen(ch_URL)
    html = x.read()
    soup = BeautifulSoup(html, "lxml")
    textSoup = soup.get_text(strip=True)
    rePat = r'HomeVideosPlaylistsCommunityChannelsAbout(.*)yt.setConfig'
    temp = search(rePat, textSoup).group(1)
    urlTable = findall(r'watch\?v=.+?(?=\")', temp)
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


if __name__ == "__main__":
    main()
