from functools import lru_cache

from punq import Container, Scope
from motor.motor_asyncio import AsyncIOMotorClient

from app.infra.repositories.messages.base import BaseChatRepository
from app.infra.repositories.messages.mongo import MongoDBChatRepositories
from app.logic.commands.message import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator
from app.settings.config import BaseConfig

@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(CreateChatCommandHandler,)
    container.register(BaseConfig, scope=Scope.singleton)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        return mediator

    def iniit_chat_mongodb_repositories():
        config: BaseConfig = container.resolve(BaseConfig)
        client = AsyncIOMotorClient(uri=config.mongodb_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatRepositories(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )


    container.register(BaseChatRepository, MongoDBChatRepositories, scope=Scope.singleton)
    container.register(Mediator, factory=init_mediator)

    return container

