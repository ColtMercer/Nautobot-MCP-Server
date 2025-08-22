# Deploy

## API-only
- Container image: build with `-f src/Dockerfile`.
- Expose port `7001`.
- Provide environment variables for Nautobot and auth.

## Optional Chainlit UI (local machine)

Use Chainlit to chat with the API from your browser.

1) Start the API in one terminal:
```
pip install -e ./src[dev]
nautobot-mcp-server
```
Defaults: HOST `127.0.0.1`, PORT `7001`.

2) Start Chainlit in another terminal:
```
export API_BASE_URL=http://localhost:7001
# If you turned on API key auth in the API:
# export API_KEY=your-api-key
chainlit run chainlit_app/app.py -w
```

3) Open the UI:
`http://localhost:8000`

4) Example tool call (type into Chainlit):
```
tool:get_devices_by_location {"location_name":"NY Data Center"}
```

## Optional Chainlit UI (Docker Compose)
- Use `docker-compose.yml` to run API + Chainlit together.
- Chainlit connects to API `/tools` and `/tools/invoke`.
- Environment variables before `docker compose up`:
  - `NAUTOBOT_URL` (e.g., `http://nautobot:8080`)
  - `NAUTOBOT_TOKEN`
  - `AUTH_MODE` and `API_KEYS` (optional)
  - `API_KEY` (optional, to pass from Chainlit to API)
