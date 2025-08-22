import os
from contextlib import contextmanager

from starlette.testclient import TestClient

from nautobot_mcp_server.server import server
from nautobot_mcp_server.settings import get_settings


@contextmanager
def set_env(**env):
    old = {k: os.environ.get(k) for k in env}
    try:
        os.environ.update({k: str(v) for k, v in env.items()})
        # bust settings cache if needed
        get_settings.cache_clear()  # type: ignore[attr-defined]
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        get_settings.cache_clear()  # type: ignore[attr-defined]


def test_tools_requires_api_key_when_enabled() -> None:
    with set_env(AUTH_MODE="api_key", API_KEYS="abc123"):
        client = TestClient(server.app)
        r = client.get("/tools")
        assert r.status_code == 401
        r2 = client.get("/tools", headers={"X-API-Key": "abc123"})
        assert r2.status_code == 200

