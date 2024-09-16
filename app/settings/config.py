from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    api_port: int
    mongodb_connection_uri: str

    class Config:
        env_file = '../../.env'
