"""Centralized settings with env and optional YAML overlay."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    host: str = Field(default="127.0.0.1", description="Bind address")
    port: int = Field(default=7001, description="HTTP port")
    log_level: str = Field(default="info", description="Log level")

    # Nautobot
    nautobot_url: AnyHttpUrl = Field(default="http://nautobot:8080", description="Nautobot base URL")
    graphql_path: str = Field(default="/graphql/", description="GraphQL path")
    nautobot_token: Optional[str] = Field(default=None, description="Nautobot token")

    # Auth
    auth_mode: str = Field(default="none", description="Auth mode: none|api_key|basic|bearer|oidc")
    api_keys: List[str] = Field(default_factory=list, description="Allowed API keys for api_key mode")

    # Chainlit/LLM
    enable_chainlit: bool = Field(default=False)
    openai_api_key: Optional[str] = None
    openai_model: str = Field(default=os.environ.get("OPENAI_MODEL", os.environ.get("DEFAULT_MODEL", "gpt-4o-mini")))

    # Customization
    config_yaml: Optional[Path] = Field(default=None, description="Path to YAML with org customizations")
    demo_mode: bool = Field(default=False)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("api_keys", mode="before")
    @classmethod
    def _split_api_keys(cls, v):  # type: ignore[override]
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # split comma/semicolon/whitespace separated
            raw = [p.strip() for p in v.replace(";", ",").split(",")]
            return [x for x in raw if x]
        return []


def _load_yaml(path: Path | None) -> dict:
    if not path:
        return {}
    try:
        with path.expanduser().open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
            if not isinstance(data, dict):
                return {}
            return data
    except FileNotFoundError:
        return {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    # initial from env/.env
    base = Settings()

    # overlay from YAML if provided
    yaml_data = _load_yaml(base.config_yaml)
    if yaml_data:
        # construct another Settings from yaml values but allow env to win
        overlay = Settings(**{**yaml_data, **base.model_dump()})
        return overlay
    return base


