from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from pydantic import BaseSettings, BaseConfig
from pydantic import validator
from pydantic.env_settings import SettingsSourceCallable

logger = logging.getLogger(__name__)


class JsonConfig(BaseConfig):
    env_file = 'Subclasses of JsonConfig must redefine "env_file" field'
    env_file_encoding = 'utf-8'

    @classmethod
    def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
    ) -> tuple[SettingsSourceCallable, ...]:
        def json_config_settings_source(base: BaseSettings) -> dict[str, Any]:
            """
            Settings source that loads variables from a JSON file.
            """
            my_path = Path(__file__).parent.parent
            file_path = os.path.join(my_path, base.__config__.env_file)
            encoding = base.__config__.env_file_encoding
            return json.loads(Path(file_path).read_text(encoding))

        return (
            init_settings,
            json_config_settings_source,
            env_settings,
            file_secret_settings,
        )


class Settings(BaseSettings):
    PROJECT_NAME: str
    LOG_LEVEL: str
    LOG_FORMAT: str
    VERSION: str
    BOT_TOKEN: str
    BOT_REPLY: bool
    MONGO_URL: str
    MONGO_DB_NAME: str

    class Config(JsonConfig):
        env_file = 'config.json'

    @validator('LOG_LEVEL')
    def log_level_validator(cls, log_level):  # noqa
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'LOG_LEVEL value is invalid: {log_level}')
        return log_level


settings = Settings()
