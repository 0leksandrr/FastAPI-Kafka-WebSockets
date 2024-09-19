from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self) -> str:
        return f'Chat with this title ({self.title}) already exists.'


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    chat_oid: str

    @property
    def message(self) -> str:
        return f'Chat with this oid ({self.chat_oid}) not found.'
