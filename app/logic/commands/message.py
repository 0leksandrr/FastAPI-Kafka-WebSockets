from dataclasses import dataclass

from app.domain.entities.messages import Chat, Message
from app.domain.values.messages import Title, Text
from app.infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from app.logic.commands.base import BaseCommand, CommandHandler
from app.logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException, ChatNotFoundException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        # TODO: read events

        new_chat = Chat(title=title)
        await self.chat_repository.add_chat(new_chat)

        return new_chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    message_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        if not (await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)):
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        message = Message(text=Text(value=command.text))
        await self.message_repository.add_message(chat_oid=command.chat_oid, message=message)

        return message
