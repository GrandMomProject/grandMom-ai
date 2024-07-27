from pydantic import BaseModel


class FirstInterviewReq(BaseModel):
    imageSummary: str


class AdditionalInterviewReq(BaseModel):
    chatHistory: str
    answer: str
