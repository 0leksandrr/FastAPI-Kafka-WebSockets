from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.domain.entities.messages import Chat
from app.infra.repositories.messages.base import BaseChatRepository


@dataclass
class MongoDBChatRepositories(BaseChatRepository):
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_chat_collection(self) -> AsyncIOMotorCollection:
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    async def add_chat(self, chat: Chat) -> None:
        collection = self._get_chat_collection()

        await collection.insert_one(
            convert_entity_to_document(chat),
        )
