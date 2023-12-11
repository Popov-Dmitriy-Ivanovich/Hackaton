from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse 
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
class SendHelloWorld:
    #data: str
    def __init__(self):
        self.data = "Hello world"
@app.get("/")
async def main():
    return FileResponse('placeholder.html')