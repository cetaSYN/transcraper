#!/usr/bin/env python3

from bs4 import BeautifulSoup
import logging
from os import path
import re
from urllib.request import urlopen
from youtube_transcript_api import YouTubeTranscriptApi

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)


def main():
    channel_url = 'https://www.youtube.com/user/professormesser'

    video_ids = get_video_ids(channel_url)
    log.debug("Video IDs:\n{}".format(video_ids))
    target_video = video_ids[0]
    log.debug("Targeting video: {}".format(target_video))

    # Setup log file
    if not path.exists(path.join('videos', target_video)):
        try:
            f = open(path.join('videos', target_video), "w")
            f.write("Matches:\n")
            for phrase in find_phrases_re(target_video, r"super secret code word"):
                log.info("Found matching phrase: {}".format(phrase))
                f.write("{}: {}\n".format(phrase[0], phrase[1]))
        except Exception as ex:
            log.exception(ex)
        finally:
            f.close()
    else:
        print("Video Already Parsed")


def get_video_ids(channel_url):
    """Returns a list of uploaded videos from a given YouTube channel"""
    soup = BeautifulSoup(urlopen(video_page(channel_url)).read(), "html.parser")
    return [
        a['href'][9:]  # Only grab video ID
        for a
        in soup.find(id="content").find_all("a", href=True)  # Find all links within content
        if re.search(r'watch\?v=[a-zA-Z0-9]+', a['href'])  # Must be a video link
    ][1:]  # Drop the first entry, it's just an auto-play link


def video_page(channel_url):
    """Returns the /videos/ page to a given YouTube channel"""
    videos_url = channel_url
    trailing_slashes = re.search('/+$', videos_url)
    # Strip trailing slashes
    if trailing_slashes:
        videos_url = videos_url[:-len(trailing_slashes)]
    # Add /videos if not pre-existing
    if videos_url.split('/')[-1] != 'videos':
        videos_url = "{}/videos".format(videos_url)
    return videos_url


def find_phrases_re(video_id, pattern):
    """Iterates over a given YouTube video transcript searching for phrases matching a given regex pattern
    @param video_id The ID of the YouTube video to search
    @param pattern A regex pattern to search for; may be a simple set of words
    @return An iterator, returning a tuple of the phrase timestamp and the matching phrase
    """
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    skip, SKIP_MAX = 2, 2
    for i in range(len(transcript)):
        if skip < 0:  # Stop skipping indexes
            skip = SKIP_MAX
        if skip < SKIP_MAX:  # Skip indexes so we don't get duplicate returns from context
            skip -= 1
            continue
        if re.search(pattern, " ".join([m["text"] for m in adjacent_lines(transcript, i, 1)])):
            skip -= 1  # Skip indexes so we don't get duplicate returns from context

            # Get additional context and yield
            match = adjacent_lines(transcript, i, 8)
            ex_line = " ".join([m["text"] for m in match])
            yield (
                match[0]["start"],  # Timestamp
                ex_line
            )


def adjacent_lines(transcript, index, extend_by):
    """Returns an extended phrase, including the previous and next phrases that are adjacent to the specified index
    This ensures that the searchable phrase is not missed by being cut off at a timestamp break
    @note If data is unavailable (e.g. no previous indexes), the returned data will be truncated
    @param transcript The transcript to include text from
    @param The index that will represent the middle of the extended phrase
    @param The number of indexes to extend into
    @return A list of transcript items within the specified extension
    """
    items = list()
    items.append(transcript[index])
    # Insert previous indexes at the front of the list
    try:
        for i in range(extend_by):
            items.insert(0, transcript[index-(i+1)])
    except IndexError:
        pass
    # Insert next indexes at the end of the list
    try:
        for i in range(extend_by):
            items.append(transcript[index+(i+1)])
    except IndexError:
        pass
    return items


if __name__ == "__main__":
    main()
