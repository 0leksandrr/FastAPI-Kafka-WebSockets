from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from app.domain.events.base import BaseEvent
from app.logic import GetChatMessageQueryHandler
from app.logic.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)
from app.logic.events.base import (
    ER,
    ET,
    EventHandler,
)
from app.logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
    EventHandlersNotRegisteredException,
)
from app.logic.queries.base import QT, QR, QueryHandler, BaseQuery


@dataclass(frozen=True)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QT, GetChatMessageQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_query(self, query: QT, query_handler: QueryHandler[QT]) -> QR:
        self.queries_map[query] = query_handler

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].append(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        event_type = events.__class__
        handlers = self.events_map[event_type]

        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)

        result = []

        for event in events:
            result.extend([await handle.handle(event) for handle in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map[command_type]

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query=query)
