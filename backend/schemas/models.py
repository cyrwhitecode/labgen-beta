from pydantic import BaseModel
from typing import Literal

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: dict | None = None

class TpData(BaseModel):
    titre: str
    matiere: str
    principe_mode_operatoire: str

class GenerateRequest(BaseModel):
    tp: TpData
    tableaux: list[dict[str, list[float | str | None]]]

class RapportValidationRequest(BaseModel):
    markdown_content: str