from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="core/.env", env_file_encoding="utf-8", extra="ignore"
    )


class TelegramConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="tg_")

    token: SecretStr


class Config(BaseSettings):
    tg: TelegramConfig = Field(default_factory=TelegramConfig)
    

config = Config()