from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import json

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost",
    "https://loaclhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginResponce:
    def __init__(self, success: bool) -> None:
        self.data = {"status": "OK" if success else "ERR"}


class Course:
    def __init__(self, name: str, desc: str) -> None:
        self.name = name
        self.description = desc


class CoursesList:
    def __init__(self, courses: list[Course]) -> None:
        self.data = {"courses": courses}


@app.get("/")
async def main():
    return FileResponse("resourses/frontend/placeholder.html")


@app.post("/api/login")
async def main():
    return LoginResponce(True)


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
