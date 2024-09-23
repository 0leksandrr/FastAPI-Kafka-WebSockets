from fastapi import FastAPI

from .messages.handlers import router as messages_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kafka Websockets Chat",
        docs_url="/api/docs",
        description='A simple Kafka + DDD example',
        debug=True,
    )
    app.include_router(messages_router, prefix="/chat")

    return app


app = create_app()
