from functools import lru_cache

from punq import Container, Scope
from motor.motor_asyncio import AsyncIOMotorClient

from app.infra.repositories.messages.base import BaseChatsRepository
from app.infra.repositories.messages.mongo import MongoDBChatsRepositories
from app.logic.commands.message import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator
from app.settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(CreateChatCommandHandler, )
    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        return mediator

    def init_chat_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatsRepositories(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    container.register(BaseChatsRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(Mediator, factory=init_mediator)

    return container
