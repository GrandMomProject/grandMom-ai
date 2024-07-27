from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

from first_interview import CompletionExecutor
from additional_interview import CompletionExecutorAdd
from summary import CompletionExecutorSummary
from models import FirstInterviewReq, AdditionalInterviewReq, SummaryReq, SummaryRes

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
    return "hello22223333"


@app.post('/first-interview')
def first_interview(firstInterview: FirstInterviewReq):
    log_time()
    return CompletionExecutor().get_first_interview(firstInterview.imageSummary)


@app.post('/additional-interview')
def additional_interview(additionalInterview: AdditionalInterviewReq):
    log_time()
    return CompletionExecutorAdd().get_additional_interview(additionalInterview)


@app.post('/summary', response_model=SummaryRes)
def additional_interview(summaryReq: SummaryReq):
    log_time()
    return CompletionExecutorSummary().get_summary(summaryReq)


def log_time():
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print("현재 시간:", current_time_str)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=False)
