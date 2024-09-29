from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias='MONGODB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='message', alias='MONGODB_CHAT_DATABASE')
    mongodb_chat_collection: str = Field(default='message', alias='MONGODB_CHAT_COLLECTION')
    mongodb_message_collection: str = Field(alias='MONGODB_MESSAGE_COLLECTION')
    new_chats_event_topic: str = Field(default='new_chats', alias='NEW_CHAT_EVENTS_TOPIC')
    kafka_url: str = Field(default='kafka:29092', alias='KAFKA_SERVERS')

    model_config = SettingsConfigDict(env_file='../../.env', extra='ignore')
