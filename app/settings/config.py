from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    api_port: int
    mongodb_connection_uri: str
    mongodb_chat_collection: str
    mongodb_chat_database: str

    class Config:
        env_file = '../../.env'
