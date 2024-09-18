from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.domain.entities.messages import Chat, Message
from app.infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from app.infra.repositories.messages.converters import convert_entity_to_document, convert_messages_to_document


@dataclass
class BaseMongoDBRepository:
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_collection(self) -> AsyncIOMotorCollection:
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatsRepositories(BaseChatsRepository, BaseMongoDBRepository):
    async def check_chat_exists_by_title(self, title: str) -> bool:
        collection = self._get_collection()

        return await collection.find_one({"title": title})

    async def add_chat(self, chat: Chat) -> None:
        collection = self._get_collection()

        await collection.insert_one(
            convert_entity_to_document(chat),
        )


@dataclass
class MongoDBMessageRepositories(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, chat_oid: str, message: Message) -> None:
        collection = self._get_collection()
        await collection.update_one(
            filter={'oid': chat_oid},
            update={
                '$push': {
                    'message': convert_messages_to_document(message)
                },
            },
        )


