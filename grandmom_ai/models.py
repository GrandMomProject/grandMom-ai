from typing import List

from pydantic import BaseModel


class FirstInterviewReq(BaseModel):
    imageSummary: str


class AdditionalInterviewReq(BaseModel):
    chatHistory: str
    answer: str


class SummaryReq(BaseModel):
    chatHistory: str


class SummaryRes(BaseModel):
    diaries: List[str] = []
