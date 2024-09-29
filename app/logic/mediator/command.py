from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from app.logic.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)


@dataclass(frozen=True)
class CommandMediator(ABC):
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        ...

    @abstractmethod
    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        ...
