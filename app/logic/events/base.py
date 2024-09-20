from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from app.domain.events.base import BaseEvent


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class EventHandler(ABC, Generic[ET, ER]):
    @abstractmethod
    def handle(self, event: ET) -> ER:
        ...
