from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from babel.plural import PluralRule

import glob
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

default_fallback = 'en'
languages = {}
plural_rule = PluralRule({'one': 'n in 0..1'})

language_list = glob.glob("languages/*.json")
for lang in language_list:
    filename = lang.split('\\')
    lang_code = filename[1].split('.')[0]

    with open(lang, 'r', encoding='utf8') as file:
        languages[lang_code] = json.load(file)


# custom filters for Jinja2
def plural_formatting(key_value, input, locale):
    key = ''
    for i in languages[locale]:
        if(key_value == languages[locale][i]):
            key = i
            break

    if not key:
        return key_value

    plural_key = f"{key}_plural"

    if(plural_rule(input) != 'one' and plural_key in languages[locale]):
        key = plural_key

    return languages[locale][key]


# assign filter to Jinja2
templates.env.filters['plural_formatting'] = plural_formatting


@app.get("/rental/{locale}", response_class=HTMLResponse)
async def rental(request: Request, locale: str):
    if(locale not in languages):
        locale = default_fallback

    result = {"request": request}
    result.update(languages[locale])
    result.update({'locale': locale, 'bedroom_value': 2})

    return templates.TemplateResponse("index.html", result)
