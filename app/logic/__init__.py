from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from app.infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from app.infra.repositories.messages.mongo import MongoDBChatsRepositories, MongoDBMessagesRepositories
from app.logic.commands.message import (
    CreateChatCommand,
    CreateChatCommandHandler, CreateMessageCommand, CreateMessageCommandHandler,
)
from app.logic.mediator import Mediator
from app.logic.queries.messages import GetChatMessageQueryHandler, GetChatDetailQuery
from app.settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config = container.resolve(Config)

    def init_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)

    container.register(AsyncIOMotorClient, factory=init_client)
    client = container.resolve(AsyncIOMotorClient)

    # Repositories
    def init_chat_mongodb_repository() -> MongoDBChatsRepositories:
        return MongoDBChatsRepositories(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_message_mongodb_repository() -> MongoDBMessagesRepositories:
        return MongoDBMessagesRepositories(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    container.register(BaseChatsRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessagesRepository, factory=init_message_mongodb_repository, scope=Scope.singleton)

    # Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    container.register(GetChatMessageQueryHandler)

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)],
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatMessageQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
