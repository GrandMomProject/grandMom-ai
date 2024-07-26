from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from first_interview import CompletionExecutor
from models import FirstInterviewReq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return "hello2222"


@app.post('/first-interview')
def first_interview(firstInterview: FirstInterviewReq):
    return CompletionExecutor().first_interview(firstInterview.imageSummary)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
