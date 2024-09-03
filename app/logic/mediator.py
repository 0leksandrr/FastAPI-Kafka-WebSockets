from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from app.domain.events.base import BaseEvent
from app.logic.commands.base import CommandHandler, CT, CR, BaseCommand
from app.logic.events.base import EventHandler, ER, ET
from app.logic.exceptions.mediator import EventHandlersNotRegisteredException, CommandHandlersNotRegisteredException


@dataclass(frozen=True)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )
    commands_map: dict[ER, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    def register_event(self, event: ET, event_handler: EventHandler[ET, ER]):
        self.events_map[event.__class__].append(event_handler)

    def register_command(self, command: CT, command_handler: CommandHandler[CT, CR]):
        self.commands_map[command.__class__].append(command_handler)

    def handle_event(self, event: BaseEvent) -> Iterable[ER]:
        event_type = event.__class__
        handlers = self.events_map[event_type]

        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)

        return [handle.handle(event) for handle in handlers]

    def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        commands = self.events_map[command_type]

        if not commands:
            raise CommandHandlersNotRegisteredException(command_type)

        return [handler.handle(handler) for handler in commands]