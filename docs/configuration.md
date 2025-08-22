# Configuration

Settings are centralized in `nautobot_mcp_server/settings.py` using pydantic settings.

Precedence: environment variables > YAML file > defaults.

Key variables:
- `HOST`, `PORT`, `LOG_LEVEL`
- `NAUTOBOT_URL`, `GRAPHQL_PATH`, `NAUTOBOT_TOKEN`
- `AUTH_MODE` (none|api_key|basic|bearer|oidc)
- `API_KEYS` (comma-separated)
- `CONFIG_YAML` (path to additional YAML overrides)

Example YAML:
```yaml
nautobot_url: http://nautobot:8080
graphql_path: /graphql/
```
