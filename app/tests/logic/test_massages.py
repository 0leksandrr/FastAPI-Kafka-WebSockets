import pytest

from app.domain.entities.messages import Chat
from app.infra.repositories.messages import BaseChatRepository
from app.logic import Mediator, CreateChatCommand


@pytest.mark.asyncio
async def test_create_chat_command_success(
        chat_repository: BaseChatRepository,
        mediator: Mediator
):
    # TODO: ADD FAKER FOR REGISTERIN RANDOM TEXT
    chat: Chat = (await mediator.handle_command(CreateChatCommand(title='something')))[0]

    assert await chat_repository.check_chat_exists_by_title(chat.title.as_generic_type())
