from dataclasses import dataclass
from typing import Generic

from app.domain.entities.messages import Chat
from app.infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from app.logic.exceptions.messages import ChatNotFoundException
from app.logic.queries.base import BaseQuery, QueryHandler, QT


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_id: str


@dataclass(frozen=True)
class GetChatMessageQueryHandler(QueryHandler, Generic[QT, QR]):
    chats_repository = BaseChatsRepository
    messeges_repository = BaseMessagesRepository

    async def handle(self, command: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_id)

        if not chat:
            raise ChatNotFoundException(command.chat_id)

        return chat
