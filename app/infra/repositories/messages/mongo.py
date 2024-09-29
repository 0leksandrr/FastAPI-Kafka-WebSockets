from dataclasses import dataclass
from typing import Iterable

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)

from app.domain.entities.messages import (
    Chat,
    Message,
)
from app.infra.repositories.filters.messages import GetMessagesFilters
from app.infra.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.infra.repositories.messages.converters import (
    convert_chat_document_to_entity,
    convert_chat_to_document,
    convert_message_document_to_entity,
    convert_messages_to_document,
)


@dataclass
class BaseMongoDBRepository:
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self) -> AsyncIOMotorCollection:
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatsRepositories(BaseChatsRepository, BaseMongoDBRepository):
    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one({"title": title}))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one({"oid": oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_to_document(chat))


@dataclass
class MongoDBMessagesRepositories(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(convert_messages_to_document(message))

    async def get_messages(self, chat_oid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        find = {'chat_oid': chat_oid}

        cursor = self._collection.find(find).skip(filters.offset).limit(filters.limit)
        count = await self._collection.count_documents(find)
        messages = [
            convert_message_document_to_entity(message_document=message_document)
            async for message_document in cursor
        ]

        return messages, count
