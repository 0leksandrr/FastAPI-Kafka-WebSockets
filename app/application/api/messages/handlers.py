from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from app.application.api.dependencies.containers import container
from app.application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from app.domain.exceptions.base import ApplicationException
from app.logic import Mediator, CreateChatCommand

router = APIRouter(
    tags=["Chat"],
)


@router.post("/", response_model=CreateChatResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_chat_handler(schema: CreateChatRequestSchema):
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateChatResponseSchema.from_entity(chat)
