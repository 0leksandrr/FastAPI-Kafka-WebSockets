from dataclasses import dataclass

from app.domain.events.messages import NewChatCreatedEvent, NewMessageReceivedEvent
from app.infra.message_brokers.converters import convert_event_to_broker_message
from app.logic.events.base import EventHandler


@dataclass
class CreateChatEventHandler(EventHandler[NewChatCreatedEvent, None]):

    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            key=event.event_id.encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )


@dataclass
class CreateMessageEventHandler(EventHandler[NewMessageReceivedEvent, None]):

    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            key=event.event_id.encode(),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )
