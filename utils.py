import tempfile
from moviepy.editor import VideoFileClip
import io
from pytube import YouTube

def convert_mp4_to_mp3(mp4_bytes):
    video = io.BytesIO(mp4_bytes)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(mp4_bytes)

        temp_video.close()

        video_clip = VideoFileClip(temp_video.name)

        audio_clip = video_clip.audio

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.close()

            audio_clip.write_audiofile(temp_audio.name, codec="mp3")

            with open(temp_audio.name, "rb") as f:
                mp3_bytes = f.read()

    return mp3_bytes

def download_video(url, caminho_salvar):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video.download(caminho_salvar)
    return video.default_filename
