from contextlib import asynccontextmanager

from fastapi import FastAPI
from punq import Container

from .messages.handlers import router as messages_router
from ...infra.message_brokers.base import BaseMessageBroker
from ...logic import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()
    kafka_broker = container.resolve(BaseMessageBroker)

    await kafka_broker.producer.start()

    yield

    await kafka_broker.producer.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kafka Websockets Chat",
        docs_url="/api/docs",
        description='A simple Kafka + DDD example',
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(messages_router, prefix="/message")

    return app


app = create_app()
