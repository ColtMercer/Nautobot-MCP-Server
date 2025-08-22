"""Centralized settings with env and optional YAML overlay."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    host: str = Field(default="127.0.0.1", description="Bind address")
    port: int = Field(default=7001, description="HTTP port")
    log_level: str = Field(default="info", description="Log level")

    # Nautobot
    nautobot_url: str = Field(
        default="http://nautobot:8080", description="Nautobot base URL"
    )
    graphql_path: str = Field(default="/graphql/", description="GraphQL path")
    nautobot_token: str | None = Field(default=None, description="Nautobot token")

    # Auth
    auth_mode: str = Field(
        default="none", description="Auth mode: none|api_key|basic|bearer|oidc"
    )
    api_keys: list[str] = Field(
        default_factory=list, description="Allowed API keys for api_key mode"
    )

    # Chainlit/LLM
    enable_chainlit: bool = Field(default=False)
    openai_api_key: str | None = None
    openai_model: str = Field(
        default=os.environ.get(
            "OPENAI_MODEL", os.environ.get("DEFAULT_MODEL", "gpt-4o-mini")
        )
    )

    # Customization
    config_yaml: Path | None = Field(
        default=None, description="Path to YAML with org customizations"
    )
    demo_mode: bool = Field(default=False)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", json_schema_extra={}
    )

    @field_validator("api_keys", mode="before")
    @classmethod
    def _split_api_keys(cls, v):  # type: ignore[override]
        # Accept list (already parsed), JSON array string, or simple comma/semicolon-separated string
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                try:
                    import json

                    parsed = json.loads(s)
                    if isinstance(parsed, list):
                        return [str(x).strip() for x in parsed if str(x).strip()]
                except Exception:
                    pass
            raw = [p.strip() for p in s.replace(";", ",").split(",")]
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

    # overlay from YAML if provided, but do not override explicit env vars
    yaml_data = _load_yaml(base.config_yaml)
    if yaml_data:
        env_map = {
            "host": "HOST",
            "port": "PORT",
            "log_level": "LOG_LEVEL",
            "nautobot_url": "NAUTOBOT_URL",
            "graphql_path": "GRAPHQL_PATH",
            "nautobot_token": "NAUTOBOT_TOKEN",
            "auth_mode": "AUTH_MODE",
            "api_keys": "API_KEYS",
            "enable_chainlit": "ENABLE_CHAINLIT",
            "openai_api_key": "OPENAI_API_KEY",
            "openai_model": "OPENAI_MODEL",
            "config_yaml": "CONFIG_YAML",
            "demo_mode": "DEMO_MODE",
        }
        merged = base.model_dump()
        for key, value in yaml_data.items():
            env_var = env_map.get(key)
            if env_var and env_var in os.environ:
                # env wins; keep existing value from base
                continue
            merged[key] = value
        return Settings(**merged)
    return base
