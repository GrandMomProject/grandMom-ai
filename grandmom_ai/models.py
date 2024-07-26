from pydantic import BaseModel


class FirstInterviewReq(BaseModel):
    imageSummary: str
