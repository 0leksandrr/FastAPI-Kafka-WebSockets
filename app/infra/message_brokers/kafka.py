from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from app.infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(key=key, topic=topic, value=value)

    async def receive_message(self, topic: str):
        ...
