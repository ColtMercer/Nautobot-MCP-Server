import httpx
import pytest

from nautobot_mcp_server.server import server


@pytest.mark.anyio("asyncio")
async def test_healthz() -> None:
    app = server.streamable_http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/healthz")
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("status") == "ok"
        assert data.get("service") == "nautobot-mcp-server"


@pytest.mark.anyio("asyncio")
async def test_tools_endpoint_lists_tools() -> None:
    app = server.streamable_http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/tools")
        assert resp.status_code == 200
        payload = resp.json()
        assert "tools" in payload
        assert isinstance(payload["tools"], list)
