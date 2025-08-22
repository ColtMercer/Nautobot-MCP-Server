from nautobot_mcp_server.tools.devices import (
    get_devices_by_location,
    get_devices_by_location_and_role,
)
from nautobot_mcp_server.tools.prefixes import get_prefixes_by_location


class DummyClient:
    def get_prefixes_by_location(self, name: str):
        return [{"prefix": "10.0.0.0/24", "status": "Active", "locations": [name]}]

    def get_devices_by_location(self, name: str):
        return [{"name": "r1", "location": name}]

    def get_devices_by_location_and_role(self, name: str, role: str):
        return [{"name": "r1", "location": name, "role": role}]


def test_prefixes_tool(monkeypatch):
    from nautobot_mcp_server.clients import nautobot_graphql

    monkeypatch.setattr(nautobot_graphql, "client", DummyClient())
    res = get_prefixes_by_location("HQ")
    assert res["success"] is True
    assert res["count"] == 1


def test_devices_tools(monkeypatch):
    from nautobot_mcp_server.clients import nautobot_graphql

    monkeypatch.setattr(nautobot_graphql, "client", DummyClient())
    r1 = get_devices_by_location("DC1")
    assert r1["count"] == 1
    r2 = get_devices_by_location_and_role("DC1", "Core")
    assert r2["count"] == 1
