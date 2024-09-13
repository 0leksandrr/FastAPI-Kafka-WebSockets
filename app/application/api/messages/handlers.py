from fastapi.routing import APIRouter

from app.application.api.dependencies.containers import container
from app.application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from app.logic import Mediator, CreateChatCommand

router = APIRouter(
    tags=["Chat"],
)


@router.post("/", response_model=CreateChatResponseSchema)
async def create_chat_handler(schema: CreateChatRequestSchema):
    mediator: Mediator = container.resolve(Mediator)

    await mediator.handle_command(CreateChatCommand(title=schema.title))
