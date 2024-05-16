import os
import pytube
from moviepy.editor import VideoFileClip

def convert_video_to_mp3(video_url):
    try:
        # Download the video from YouTube
        yt = pytube.YouTube(video_url)
        video = yt.streams.first()
        video.download()

        # Get the video file name
        video_filename = video.default_filename

        # Convert the video to MP3
        video_clip = VideoFileClip(video_filename)
        audio_clip = video_clip.audio
        audio_filename = os.path.splitext(video_filename)[0] + '.mp3'
        audio_clip.write_audiofile(audio_filename)

        return audio_filename
    except Exception as e:
        print(f"Error converting video: {e}")
        return None

# Example usage:
# video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
# convert_video_to_mp3(video_url)
