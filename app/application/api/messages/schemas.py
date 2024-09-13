from pydantic import BaseModel

class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str
