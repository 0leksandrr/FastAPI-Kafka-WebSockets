from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    # TODO Create abstract producer

    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes):
        ...

    @abstractmethod
    async def receive_message(self, topic: str):
        ...
