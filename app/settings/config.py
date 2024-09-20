from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias='MONGODB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='chat', alias='MONGODB_CHAT_DATABASE')
    mongodb_chat_collection: str = Field(default='chat', alias='MONGODB_CHAT_COLLECTION')

    model_config = SettingsConfigDict(env_file='../../.env', extra='ignore')
