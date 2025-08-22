# Nautobot MCP Server

FastMCP server exposing Nautobot GraphQL data as Machine-Callable Tools (MCP) and simple REST endpoints.

## Quickstart

### Run locally (API only)
```bash
pip install -e ./src
nautobot-mcp-server
```

Environment variables:
```bash
export HOST=0.0.0.0
export PORT=7001
export NAUTOBOT_URL=http://nautobot:8080
export NAUTOBOT_TOKEN=replace-me
```

### Use Chainlit as the UI (local)
Open a second terminal:
```bash
export API_BASE_URL=http://localhost:7001
# If API key auth is enabled:
# export API_KEY=supersecret
chainlit run chainlit_app/app.py -w
```
Open `http://localhost:8000` and type:
```
tool:get_devices_by_location {"location_name":"NY Data Center"}
```

### Docker
```bash
docker build -t nautobot-mcp:dev -f src/Dockerfile .
docker run --rm -p 7001:7001 \
  -e NAUTOBOT_URL=http://nautobot:8080 \
  -e NAUTOBOT_TOKEN=replace-me \
  nautobot-mcp:dev
```

Health check:
```bash
curl -s http://localhost:7001/healthz
```

List tools:
```bash
curl -s http://localhost:7001/tools | jq
```

Invoke a tool:
```bash
curl -s -X POST http://localhost:7001/tools/invoke \
  -H 'Content-Type: application/json' \
  -d '{"tool_name": "get_devices_by_location", "args": {"location_name": "NY Data Center"}}'
```
