from functools import lru_cache

from aiokafka import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from app.domain.events.messages import NewChatCreatedEvent
from app.infra.message_brokers.base import BaseMessageBroker
from app.infra.message_brokers.kafka import KafkaMessageBroker
from app.infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.infra.repositories.messages.mongo import (
    MongoDBChatsRepositories,
    MongoDBMessagesRepositories,
)
from app.logic.commands.message import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from app.logic.events.messages import CreateChatEventHandler
from app.logic.mediator.base import Mediator
from app.logic.mediator.event import EventMediator
from app.logic.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
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
            mongo_db_collection_name=config.mongodb_message_collection,
        )

    container.register(BaseChatsRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessagesRepository, factory=init_message_mongodb_repository, scope=Scope.singleton)

    # Command handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Query handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    # Brokers
    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
        )

    container.register(BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton)

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessagesRepository),
            chats_repository=container.resolve(BaseChatsRepository),
        )
        create_chat_event_handler = CreateChatEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
        )

        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        mediator.register_event(
            NewChatCreatedEvent,
            [create_chat_event_handler],
        )

        return mediator

    container.register(EventMediator, factory=init_mediator)
    container.register(Mediator, factory=init_mediator)

    return container
