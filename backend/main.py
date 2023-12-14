from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from src.login import LoginData, process_login
from src.register import RegisterData, register_user
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from src.process_form import process_favourites, ProfileFormResult
from requests import request
import json
app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
templates = Jinja2Templates(directory="../frontend/build")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost",
    "https://loaclhost:8080",
    "http://localhost:3000",
    "http://192.168.111.205:3000",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Course:
    def __init__(self, name: str, desc: str) -> None:
        self.name = name
        self.description = desc
class CoursesList:
    def __init__(self, courses: list) -> None:
        self.data = {"courses": courses}

@app.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/login")
async def main(log_data: LoginData):
    print(log_data)
    return process_login(log_data)

@app.post('/api/register')
async def main(reg_data: RegisterData):
    return register_user(reg_data)

@app.post("/api/get_courses")
async def main():
    return CoursesList(
        [
            Course("1 course", "description of 1 course"),
            Course("2 course", "description of 2 course"),
        ]
    )


@app.get("/api/get_profile_form")
async def main():
    return json.load(open("resourses/forms/TEST_form.json"))

@app.get('/api/login_index')

@app.post('/api/profile_form_res')
async def main(form_res: ProfileFormResult):
    return process_favourites(form_res)
async def main(code:str, state:str):
    auth_url = 'https://oauth.vk.com/access_token'
    auth_url += '?client_id=51813528'
    auth_url += '&client_secret=VXE0bHDlD2n9zNIolh2h'
    auth_url += '&redirect_uri=https://89.232.176.33:443/api/login_index'
    auth_url += '&code='+code
    r = request('get',auth_url)
    return {'data': r.text}
