import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from src.login import LoginData, process_login
from src.register import RegisterData, register_user
from src.vk_auth import VkAuth
from src.courses_generator import CoursesRequest, get_courses
from src.process_form import process_favourites, ProfileFormResult

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
templates = Jinja2Templates(directory="../frontend/build")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/login")
async def main(log_data: LoginData):
    return process_login(log_data)


@app.post("/api/register")
async def main(reg_data: RegisterData):
    return register_user(reg_data)


@app.post("/api/get_courses")
async def main(body: CoursesRequest):
    try:
        return get_courses(body.data.login)
    except Exception as e:
        return {"err": str(e)}


@app.get("/api/get_profile_form")
async def main():
    return json.load(open("resourses/forms/TEST_form.json"))


@app.get("/api/login_index")
async def main(code: str, state: str):
    authentificator = VkAuth(code, state)
    try:
        authentificator.add_user_vk_data_to_db()
    except Exception as e:
        return {"err": str(e)}
    return FileResponse("resourses/frontend/placeholder.html")


@app.post("/api/profile_form_res")
async def main(form_res: ProfileFormResult):
    return process_favourites(form_res)
