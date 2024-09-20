from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from punq import Container

from app.application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
)
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.logic import (
    CreateChatCommand,
    init_container,
    Mediator,
)
from app.logic.commands.message import CreateMessageCommand


router = APIRouter(
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to create new chat, if chat with the same title already exists return 400 error",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Create new chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    "/{chat_oid}/message",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to send message to chat",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_message_handler(
        chat_oid: str,
        schema: CreateMessageRequestSchema,
        container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Create new message in chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message = await mediator.handle_command(CreateMessageCommand(text=schema.text, chat_oid=chat_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateMessageResponseSchema.from_entity(message)
