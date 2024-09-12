from punq import Container

from app.infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from app.logic.commands.message import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator


def init_mediator(
        container: Container,
        mediator: Mediator,
    ):
    mediator.register_command(
        CreateChatCommand,
        [container.resolve(CreateChatCommandHandler)],
    )

def init_container(
        container: Container,
):
    container.register(BaseChatRepository, MemoryChatRepository)
    container.register(CreateChatCommandHandler,)
