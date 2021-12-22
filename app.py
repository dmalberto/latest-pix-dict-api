import json
from fastapi import FastAPI
import requests
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def main():
    df = requests.get(
        'https://api.github.com/repos/bacen/pix-dict-api/releases').json()[0]

    for asset in df['assets']:
        if ".html" in asset['name']:
            r = requests.get(asset['browser_download_url'],
                             allow_redirects=True)
    return r.content


@app.get("/update")
async def main():
    df = requests.get(
        'https://api.github.com/repos/bacen/pix-dict-api/releases').json()[0]

    return json.dumps({"status": 200, "version": df['tag_name']})
