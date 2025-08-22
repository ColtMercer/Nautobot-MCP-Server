import os
import requests
import chainlit as cl


API_BASE = os.environ.get("API_BASE_URL", "http://localhost:7001")
API_KEY = os.environ.get("API_KEY")


def _headers():
    if API_KEY:
        return {"X-API-Key": API_KEY}
    return {}


@cl.on_chat_start
async def start():
    tools = requests.get(f"{API_BASE}/tools", headers=_headers(), timeout=10).json().get("tools", [])
    names = ", ".join(t.get("name") for t in tools)
    await cl.Message(content=f"Connected to API. Available tools: {names}").send()


@cl.on_message
async def message(msg: cl.Message):
    text = msg.content.strip()
    # naive parse: expect 'tool:NAME {json args}'
    if text.startswith("tool:"):
        try:
            _, rest = text.split(":", 1)
            name, _, args_str = rest.partition(" ")
            args = {}
            if args_str:
                import json

                args = json.loads(args_str)
            r = requests.post(
                f"{API_BASE}/tools/invoke",
                json={"tool_name": name, "args": args},
                headers={"Content-Type": "application/json", **_headers()},
                timeout=20,
            )
            data = r.json()
            await cl.Message(content=f"Result: {data}").send()
        except Exception as e:
            await cl.Message(content=f"Error: {e}").send()
    else:
        await cl.Message(content="Use 'tool:TOOL_NAME {\"arg\": \"value\"}' to invoke.").send()


