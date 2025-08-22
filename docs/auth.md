# Authentication

Configure via `AUTH_MODE` and related settings.

## Modes
- `none`: No authentication (for demos only).
- `api_key`: Require `X-API-Key` header. Keys from `API_KEYS`.
- `basic`, `bearer`, `oidc`: Planned.

## Example
```bash
export AUTH_MODE=api_key
export API_KEYS=supersecret1,supersecret2
curl -H "X-API-Key: supersecret1" http://localhost:7001/tools
```
