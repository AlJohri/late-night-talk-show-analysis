#!/usr/bin/env python3

import os
import re
import json
import lxml.html
from itertools import islice

from blessings import Terminal
t = Terminal()

def transcript_html_to_text(html):
    text = lxml.html.fromstring(html).text_content()
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'^\s+|\s$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def extract_video_clips(transcript):

    video_clips = []
    in_video_clip = False
    current_video_clip = ""
    remaining_transcript = ""

    for line in transcript.splitlines():

        if line == "(BEGIN VIDEO CLIP)":
            in_video_clip = True
            continue

        if line == "(END VIDEO CLIP)":
            in_video_clip = False
            video_clips.append(current_video_clip)
            current_video_clip = ""
            continue

        if in_video_clip:
            current_video_clip += line
        else:
            remaining_transcript += line + "\n"

    return video_clips, remaining_transcript

def parse_transcript(html):
    transcript = transcript_html_to_text(html)
    video_clips, remaining_transcript = extract_video_clips(transcript)
    return {
        "full_transcript": transcript,
        "video_clips": video_clips,
        "remaining_transcript": remaining_transcript
    }

for filename in os.listdir("data/raw"):

    with open(f"data/transcripts/raw/{filename}") as f:
        item = json.load(f)

    date, title, url = item['date'], item['title'], item['url']
    print(t.magenta(f"Parsing {date} {title}"))
    print(url)

    html = item.pop('html')
    parsed = parse_transcript(html)

    print(t.bold_white("Full Transcript:"))
    print(parsed['full_transcript'])

    print(t.bold_white("Video Clips:"))
    for i, video_clip in enumerate(parsed['video_clips']):
        print(f"Video Clip: {i+1}")
        print(video_clip)

    print(t.bold_white("Remaining Transcript:"))
    print(parsed['remaining_transcript'])

    print("----------------------------------------------------")

    output = {**item, **parsed}

    with open(f"data/transcripts/parsed/{filename}", "w") as f:
        json.dump(output, f)
