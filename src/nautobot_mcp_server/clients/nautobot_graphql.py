"""Nautobot GraphQL client for making queries."""

from importlib import resources
from typing import Any

import requests
import structlog

from ..settings import get_settings

logger = structlog.get_logger(__name__)

_settings = get_settings()
BASE_URL = _settings.nautobot_url
GRAPHQL_PATH = _settings.graphql_path
TOKEN = _settings.nautobot_token

HEADERS = {"Authorization": f"Token {TOKEN}"} if TOKEN else {}


def _load_query(filename: str) -> str:
    with resources.files("nautobot_mcp_server.graphql").joinpath(filename).open(
        "r", encoding="utf-8"
    ) as f:
        return f.read()


PREFIXES_QUERY = _load_query("prefixes_by_location.graphql")
DEVICES_QUERY = _load_query("devices_by_location.graphql")
DEVICES_BY_LOCATION_AND_ROLE_QUERY = _load_query("devices_by_location_and_role.graphql")


class NautobotGraphQLClient:
    """Client for making GraphQL queries to Nautobot."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        """Initialize the client."""
        self.base_url = base_url or BASE_URL
        self.token = token or TOKEN
        self.headers = {"Authorization": f"Token {self.token}"} if self.token else {}
        self.graphql_url = f"{self.base_url}{GRAPHQL_PATH}"

    def query(
        self, query: str, variables: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Execute a GraphQL query."""
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables

        logger.info(
            "Executing GraphQL query",
            query=query[:100] + "..." if len(query) > 100 else query,
        )

        try:
            response = requests.post(
                self.graphql_url, json=payload, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                logger.error("GraphQL errors", errors=data["errors"])
                raise RuntimeError(f"GraphQL errors: {data['errors']}")

            return data
        except requests.exceptions.RequestException as e:
            logger.error("GraphQL request failed", error=str(e))
            raise RuntimeError(f"GraphQL request failed: {e}") from e

    def get_all_prefixes(self) -> list[dict[str, Any]]:
        """Get all prefixes."""
        try:
            data = self.query(
                "query { prefixes { prefix status { name } role { name } description } }"
            )
            prefixes_data = data["data"]["prefixes"]

            prefixes = []
            for prefix in prefixes_data:
                prefix_data = {
                    "prefix": prefix["prefix"],
                    "status": (prefix["status"] or {}).get("name"),
                    "role": (prefix["role"] or {}).get("name"),
                    "description": prefix.get("description"),
                }
                prefixes.append(prefix_data)

            logger.info("Retrieved all prefixes", count=len(prefixes))
            return prefixes
        except Exception as e:
            logger.error("Failed to get all prefixes", error=str(e))
            raise RuntimeError(f"GraphQL request failed: {e}") from e

    def get_prefixes_by_location(self, location_name: str) -> list[dict[str, Any]]:
        """Get all prefixes for a given location name."""
        try:
            data = self.query(PREFIXES_QUERY, {"name": location_name})
            prefixes_data = data["data"]["prefixes"]

            prefixes = []
            for prefix in prefixes_data:
                # Get location names from the locations array
                location_names = [
                    loc["name"] for loc in (prefix.get("locations") or [])
                ]

                prefix_data = {
                    "prefix": prefix["prefix"],
                    "status": (prefix["status"] or {}).get("name"),
                    "role": (prefix["role"] or {}).get("name"),
                    "description": prefix.get("description"),
                    "locations": location_names,
                }
                prefixes.append(prefix_data)

            logger.info(
                "Retrieved prefixes by location",
                location=location_name,
                count=len(prefixes),
            )
            return prefixes
        except Exception as e:
            logger.error(
                "Failed to get prefixes by location",
                location=location_name,
                error=str(e),
            )
            raise RuntimeError(f"GraphQL request failed: {e}") from e

    def get_devices_by_location(self, location_name: str) -> list[dict[str, Any]]:
        """Get all devices for a given location name."""
        try:
            data = self.query(DEVICES_QUERY, {"name": location_name})
            devices_data = data["data"]["devices"]

            devices = []
            for device in devices_data:
                device_data = {
                    "name": device["name"],
                    "status": (device["status"] or {}).get("name"),
                    "role": (device["role"] or {}).get("name"),
                    "device_type": {
                        "model": (device["device_type"] or {}).get("model"),
                        "manufacturer": (device["device_type"] or {})
                        .get("manufacturer", {})
                        .get("name"),
                    },
                    "platform": (device["platform"] or {}).get("name"),
                    "primary_ip4": (device["primary_ip4"] or {}).get("address"),
                    "location": (device["location"] or {}).get("name"),
                }
                devices.append(device_data)

            logger.info(
                "Retrieved devices by location",
                location=location_name,
                count=len(devices),
            )
            return devices
        except Exception as e:
            logger.error(
                "Failed to get devices by location",
                location=location_name,
                error=str(e),
            )
            raise RuntimeError(f"GraphQL request failed: {e}") from e

    def get_devices_by_location_and_role(
        self, location_name: str, role_name: str
    ) -> list[dict[str, Any]]:
        """Get devices for a given location and role."""
        try:
            data = self.query(
                DEVICES_BY_LOCATION_AND_ROLE_QUERY,
                {"location": location_name, "role": role_name},
            )
            devices_data = data["data"]["devices"]

            devices = []
            for device in devices_data:
                device_data = {
                    "name": device["name"],
                    "status": (device["status"] or {}).get("name"),
                    "role": (device["role"] or {}).get("name"),
                    "device_type": {
                        "model": (device["device_type"] or {}).get("model"),
                        "manufacturer": (device["device_type"] or {})
                        .get("manufacturer", {})
                        .get("name"),
                    },
                    "platform": (device["platform"] or {}).get("name"),
                    "primary_ip4": (device["primary_ip4"] or {}).get("address"),
                    "location": (device["location"] or {}).get("name"),
                }
                devices.append(device_data)

            logger.info(
                "Retrieved devices by location and role",
                location=location_name,
                role=role_name,
                count=len(devices),
            )
            return devices
        except Exception as e:
            logger.error(
                "Failed to get devices by location and role",
                location=location_name,
                role=role_name,
                error=str(e),
            )
            raise RuntimeError(f"GraphQL request failed: {e}") from e


# Global client instance
client = NautobotGraphQLClient()
