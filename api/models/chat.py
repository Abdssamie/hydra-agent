from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str


class ChatResponseV2(BaseModel):
    message: str
    session_id: str
