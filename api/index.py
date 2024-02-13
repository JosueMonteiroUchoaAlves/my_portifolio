from pytube import YouTube, request
from urllib.error import HTTPError
from fastapi import FastAPI
from io import BytesIO
import base64

app = FastAPI()

@app.get("/api/getVideoInfo/{idVideo}/{idCanal}", status_code = 200)
async def getVideoInfo(idVideo:str, idCanal:str):
  video_url = YouTube("https://www.youtube.com/watch?v="+idVideo+"&ab_channel="+idCanal)
  return {"thumbnail": video_url.thumbnail_url, "length": video_url.length, "title": video_url.title}

@app.get("/api/downloadVideo/{idVideo}/{idCanal}", status_code = 200)
async def downloadVideo(idVideo:str, idCanal:str):
  video_url = YouTube("https://www.youtube.com/watch?v="+idVideo+"&ab_channel="+idCanal)
  video = video_url.streams.get_highest_resolution()
  buffer = BytesIO()
  bytes_remaining = video.filesize
  try:
    for chunk in request.stream(
                  video.url,          
                  timeout=None,
                  max_retries=0):
        bytes_remaining -= len(chunk)
        video.on_progress(chunk, buffer, bytes_remaining) 
  except HTTPError as e:
                if e.code != 404:
                    raise
                # Some adaptive streams need to be requested with sequence numbers
                for chunk in request.seq_stream(video.url):
                    # reduce the (bytes) remainder by the length of the chunk.
                    bytes_remaining -= len(chunk)
                    # send to the on_progress callback.
                    video.on_progress(chunk,buffer, bytes_remaining) 
  buffer_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
  return {"video": buffer_base64}
