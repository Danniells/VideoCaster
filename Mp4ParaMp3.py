import pytube
from moviepy.editor import VideoFileClip

# Insercerção dp link
video_url = input("Link: ")
# Link teste: https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley

# Download do video do youtube
yt = pytube.YouTube(video_url)
video = yt.streams.first()
video.download()

# Tranformação do arquivo para MP3
video_nome = video.default_filename
video_clip = VideoFileClip(video_nome)
audio_clip = video_clip.audio
audio_clip.write_audiofile("audio.mp3")
#audio_clip.write_audiofile(f"{video_filename}.mp3")   # o nome do arquivo fica 'nomeVideo.mp4.mp3'
