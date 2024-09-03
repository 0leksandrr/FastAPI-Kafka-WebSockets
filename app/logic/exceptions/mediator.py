from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self) -> str:
        return f"Event type {self.event_type} not registered"


@dataclass(frozen=True, eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f"Command type {self.command_type} not registered"
