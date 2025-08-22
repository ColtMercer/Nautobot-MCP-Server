import responses

from nautobot_mcp_server.clients.nautobot_graphql import NautobotGraphQLClient


@responses.activate
def test_get_prefixes_by_location_success() -> None:
    client = NautobotGraphQLClient(base_url="http://nautobot:8080", token=None)
    responses.add(
        responses.POST,
        "http://nautobot:8080/graphql/",
        json={
            "data": {
                "prefixes": [
                    {
                        "prefix": "10.0.0.0/24",
                        "status": {"name": "Active"},
                        "role": {"name": "User"},
                        "description": "Test",
                        "locations": [{"name": "HQ"}],
                    }
                ]
            }
        },
        status=200,
    )

    result = client.get_prefixes_by_location("HQ")
    assert isinstance(result, list)
    assert result[0]["prefix"] == "10.0.0.0/24"
    assert result[0]["locations"] == ["HQ"]


@responses.activate
def test_get_devices_by_location_graphql_error() -> None:
    client = NautobotGraphQLClient(base_url="http://nautobot:8080", token=None)
    responses.add(
        responses.POST,
        "http://nautobot:8080/graphql/",
        json={"errors": [{"message": "bad query"}]},
        status=200,
    )

    try:
        client.get_devices_by_location("DC1")
    except RuntimeError as e:
        assert "GraphQL errors" in str(e)
    else:
        assert False, "Expected RuntimeError"

