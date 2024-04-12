import tempfile
from typing import Annotated
from fastapi import FastAPI, File, HTTPException, UploadFile,Request
from fastapi.responses import StreamingResponse,HTMLResponse
from pydantic import BaseModel
import io
from moviepy.editor import *
from fastapi.templating import Jinja2Templates
from utils import convert_mp4_to_mp3, download_video

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
class Conversion(BaseModel):
    filename: str

class DownlaodPayload(BaseModel):
    url: str


# @app.get("/")
# def alive():
#     return {"status":"alive"}

@app.get("/authors")
def authors():
    return {
        "authors":["Jean","Danilo", "Cassiane", "Vinicius", "Daniel", "Caio", "Luis"],
    }


@app.post("/file/size")
async def fileSize(file: Annotated[bytes, File()]):
    convertBytesToMegaBytes = (len(file) / (1024 * 1024))
    return {"file_size": "{:.2f}mb".format(convertBytesToMegaBytes)}

@app.post("/file/filename")
async def fileName(file: UploadFile):
    print("\n\n\n>>> File: ", file)
    return {"filename": file.filename }

@app.post("/file/convert_to_mp3")
async def convertToMP3(mp4_file: UploadFile = File(...)):
    mp4_bytes = await mp4_file.read()

    mp3_bytes = convert_mp4_to_mp3(mp4_bytes)

    return StreamingResponse(io.BytesIO(mp3_bytes), media_type="audio/mpeg")

@app.post("/file/download-youtube")
async def downloadYoutube(downlaod_payload: DownlaodPayload):
    try:
        caminho_video = download_video(downlaod_payload.url, ".")
        video = AudioFileClip(caminho_video)
        
        with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_audio:
            video.write_audiofile(temp_audio.name)
            temp_audio.seek(0)
            mp3_bytes = temp_audio.read()
        
        return StreamingResponse(io.BytesIO(mp3_bytes), media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="./home/index.html"
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request, name="./about/about.html"
    )