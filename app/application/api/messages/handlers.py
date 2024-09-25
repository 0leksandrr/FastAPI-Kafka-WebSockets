from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from punq import Container

from app.application.api.messages.filters import GetMessagesFilter
from app.application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema, ChatDetailSchema, GetMessagesQueryResponseSchema, MessageDetailSchema,
)
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.logic import (
    CreateChatCommand,
    init_container,
    Mediator, GetChatDetailQuery, GetMessagesQuery,
)
from app.logic.commands.message import CreateMessageCommand

router = APIRouter(
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to create new message, if message with the same title already exists return 400 error",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Create new message."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    "/{chat_oid}/message",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint to add message",
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
    """Create new message in message."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(CreateMessageCommand(text=schema.text, chat_oid=chat_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    '/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    description="Endpoint to receive specific message",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    }
)
async def get_chat_handler(
        chat_oid: str,
        container: Container = Depends(init_container)
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return ChatDetailSchema.from_entity(chat)


@router.get(
    '/{chat_oid}/messages/',
    status_code=status.HTTP_200_OK,
    description="Endpoint to receive message from collection",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_messages_handler(
        chat_oid: str,
        filters: GetMessagesFilter = Depends(),
        container: Container = Depends(init_container)
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infra())
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message=message) for message in messages],
    )

