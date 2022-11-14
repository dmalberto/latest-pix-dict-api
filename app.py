from fastapi import FastAPI
import requests
from fastapi.responses import HTMLResponse
from pydantic import BaseSettings


class Settings(BaseSettings):
    content: str = ""
    dict_version: str = ""


settings = Settings()
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def main():
    if not settings.content:
        await update()
    return settings.content


@app.get("/update")
async def update():
    df = requests.get(
        "https://api.github.com/repos/bacen/pix-dict-api/releases"
    ).json()[0]
    if settings.dict_version != df["tag_name"]:
        for asset in df["assets"]:
            if ".html" in asset["name"]:
                settings.content = requests.get(
                    asset["browser_download_url"], allow_redirects=True
                ).content
        settings.dict_version = df["tag_name"]

    return '{"status": 200, "version": ' + settings.dict_version + "}"
