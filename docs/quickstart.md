# Quickstart

## Local
```bash
pip install -e ./src[dev]
nautobot-mcp-server
```

Defaults:
- HOST: 127.0.0.1
- PORT: 7001

Optional environment variables:
```bash
export NAUTOBOT_URL=http://nautobot:8080
export NAUTOBOT_TOKEN=replace-me
```

## Docker
```bash
docker build -t nautobot-mcp:dev -f src/Dockerfile .
docker run --rm -p 7001:7001 \
  -e NAUTOBOT_URL=http://nautobot:8080 \
  -e NAUTOBOT_TOKEN=replace-me \
  nautobot-mcp:dev
```
