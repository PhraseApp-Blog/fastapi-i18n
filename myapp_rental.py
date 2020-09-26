from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import glob
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app_language = 'en'
languages = {}

language_list = glob.glob("languages/*.json")
for lang in language_list:
    filename = lang.split('\\')
    lang_code = filename[1].split('.')[0]

    with open(lang, 'r', encoding='utf8') as file:
        languages[lang_code] = json.load(file)

@app.get("/rental/{language}", response_class=HTMLResponse)
async def rental(request: Request, language: str):
    if(language not in languages):
        language = app_language

    result = {"request": request}
    result.update(languages[language])

    return templates.TemplateResponse("index.html", result)
