from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

@app.get("/api/getVideoInfo/{idVideo}/{idCanal}", status_code = 200)
async def getVideoInfo(idVideo:str, idCanal:str):
  video_url = YouTube("https://www.youtube.com/watch?v="+idVideo+"&ab_channel="+idCanal)
  return {"thumbnail": video_url.thumbnail_url, "length": video_url.length, "title": video_url.title}

@app.get("/api/downloadVideo/{idVideo}/{idCanal}", status_code = 200)
async def downloadVideo(idVideo:str, idCanal:str):
  video_url = YouTube("https://www.youtube.com/watch?v="+idVideo+"&ab_channel="+idCanal)
  video = video_url.streams.get_highest_resolution()
  return {"video":video}
