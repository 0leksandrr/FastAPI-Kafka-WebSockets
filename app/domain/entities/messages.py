from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.base import BaseEntity
from app.domain.values.messages import Text, Title


@dataclass
class Message(BaseEntity):
    text: Text
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'Chat') -> bool:
        return self.oid == __value.oid


@dataclass
class Chat(BaseEntity):
    title: Title
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'Chat') -> bool:
        return self.oid == __value.oid

    def add_message(self, message: Message):
        self.messages.add(message)
