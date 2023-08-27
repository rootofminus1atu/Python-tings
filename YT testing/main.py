from pytube import YouTube, Stream
from typing import List
from io import BytesIO

# Replace 'video_url' with the URL of the YouTube video you want to download
video_url = 'https://www.youtube.com/watch?v=njX2bu-_Vw4'

# Create a YouTube object
yt: YouTube = YouTube(video_url)
streams: List[Stream] = yt.streams

valid_streams = [stream for stream in streams if stream.includes_audio_track and stream.includes_video_track]

for stream in streams:
    print(stream)

hq: Stream = yt.streams.get_highest_resolution()



video_data = BytesIO()
hq.stream_to_buffer(video_data)
video_bytes = video_data.getvalue()

"""
video_stream = yt.streams.get_highest_resolution()

download_path = './downloads'
video_stream.download(download_path)

print('Video downloaded successfully!')
"""