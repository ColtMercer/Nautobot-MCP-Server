import os
from contextlib import contextmanager
from pathlib import Path

from nautobot_mcp_server.settings import get_settings


@contextmanager
def set_env(**env):
    old = {k: os.environ.get(k) for k in env}
    try:
        os.environ.update({k: str(v) for k, v in env.items()})
        get_settings.cache_clear()  # type: ignore[attr-defined]
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        get_settings.cache_clear()  # type: ignore[attr-defined]


def test_yaml_overlay(tmp_path: Path):
    yaml_file = tmp_path / "settings.yaml"
    yaml_file.write_text(
        "nautobot_url: http://yaml:8080\nport: 9000\n", encoding="utf-8"
    )
    with set_env(CONFIG_YAML=str(yaml_file)):
        s = get_settings()
        assert str(s.nautobot_url) == "http://yaml:8080"
        assert s.port == 9000


def test_env_overrides_yaml(tmp_path: Path):
    yaml_file = tmp_path / "settings.yaml"
    yaml_file.write_text("port: 9000\n", encoding="utf-8")
    with set_env(CONFIG_YAML=str(yaml_file), PORT="8001"):
        s = get_settings()
        assert s.port == 8001


def test_api_keys_parsing():
    # Provide JSON array to avoid platform-specific env parsing quirks
    with set_env(API_KEYS='["a","b","c"]'):
        s = get_settings()
        assert s.api_keys == ["a", "b", "c"]
