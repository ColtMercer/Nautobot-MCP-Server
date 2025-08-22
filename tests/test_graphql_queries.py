from nautobot_mcp_server.clients.nautobot_graphql import (
    DEVICES_BY_LOCATION_AND_ROLE_QUERY,
    DEVICES_QUERY,
    PREFIXES_QUERY,
)


def test_queries_loaded() -> None:
    assert "query PrefixesByLocation" in PREFIXES_QUERY
    assert "query DevicesByLocation" in DEVICES_QUERY
    assert "query DevicesByLocationAndRole" in DEVICES_BY_LOCATION_AND_ROLE_QUERY
