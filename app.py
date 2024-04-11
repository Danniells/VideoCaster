from flask import Flask, jsonify, render_template, request, send_file #from flask import Flask
from flask_cors import CORS
import youtube_dl
import moviepy.editor as mp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        # Lógica para lidar com solicitações POST
        data = request.json
        youtube_url = data.get('url')
        # Código para converter o vídeo do YouTube para MP3
        return jsonify({'message': 'Aqui você pode retornar uma mensagem de sucesso ou erro'}), 200
    elif request.method == 'GET':
        # Lógica para lidar com solicitações GET
        return jsonify({'message': 'Esta é uma resposta de uma solicitação GET'}), 200


    if not youtube_url:
        return "Por favor, insira a URL do YouTube", 400

    try:
        # Configurações para baixar o vídeo do YouTube
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/video.%(ext)s'
        }

        # Baixa o vídeo do YouTube
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Extrai áudio do vídeo
        mp4_path = 'downloads/video.mp4'
        mp3_path = 'converted/audio.mp3'
        clip = mp.VideoFileClip(mp4_path)
        clip.audio.write_audiofile(mp3_path)

        # Exclui o vídeo MP4 após a conversão
        os.remove(mp4_path)

        # Retorna o arquivo MP3 para download
        return send_file(mp3_path, as_attachment=True)

    except Exception as e:
        return f"Erro ao converter o vídeo: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
