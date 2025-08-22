# API Reference

## Health
`GET /healthz`

## Tools
`GET /tools`: list available tools

`POST /tools/invoke`
```json
{
  "tool_name": "get_devices_by_location",
  "args": { "location_name": "NY Data Center" }
}
```
