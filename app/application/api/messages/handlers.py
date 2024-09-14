from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from app.application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.logic import Mediator, CreateChatCommand, init_container

router = APIRouter(
    tags=["Chat"],
)


@router.post("/",
             response_model=CreateChatResponseSchema,
             status_code=status.HTTP_201_CREATED,
             description="Endpoint to create new chat, if chat with the same title already exists return 400 error",
             responses={
                 status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
                 status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
             },
)
async def create_chat_handler(schema: CreateChatRequestSchema, container=Depends(init_container)):
    """Create new chat."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.message})

    return CreateChatResponseSchema.from_entity(chat)
