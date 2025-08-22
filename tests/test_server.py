from starlette.testclient import TestClient

from nautobot_mcp_server.server import server


def test_healthz() -> None:
    client = TestClient(server.app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert data.get("service") == "nautobot-mcp-server"


def test_tools_endpoint_lists_tools() -> None:
    client = TestClient(server.app)
    resp = client.get("/tools")
    assert resp.status_code == 200
    payload = resp.json()
    assert "tools" in payload
    assert isinstance(payload["tools"], list)

