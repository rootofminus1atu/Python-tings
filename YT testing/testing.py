from pytube import YouTube, Stream
from typing import List
from io import BytesIO

yt: YouTube = YouTube('https://www.youtube.com/watch?v=njX2bu-_Vw4')

hq: Stream = yt.streams.get_highest_resolution()

video_data = BytesIO()
hq.stream_to_buffer(video_data)
video_bytes = video_data.getvalue()

# now I can send the vide_bytes to my react frontend