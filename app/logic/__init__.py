from functools import lru_cache

from punq import Container

from app.infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from app.logic.commands.message import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator


@lru_cache(1)
def init_container():
    container = Container()

    container.register(BaseChatRepository, MemoryChatRepository)
    container.register(CreateChatCommandHandler,)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

