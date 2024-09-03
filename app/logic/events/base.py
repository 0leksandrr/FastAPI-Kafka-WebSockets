from dataclasses import dataclass
from abc import ABC
from typing import TypeVar, Any

from app.domain.events.base import BaseEvent

ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class EventHandler(ABC):
    def handle(self, event: ET) -> ER:
        ...
