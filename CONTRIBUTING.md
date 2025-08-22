# Contributing

## Dev setup
```bash
python -m pip install --upgrade pip
pip install -e ./src[dev]
```

## Checks
```bash
ruff check .
black --check .
isort --check-only .
mypy src/nautobot_mcp_server
pytest -q
```

## Pull requests
- Small, focused PRs.
- Update docs and roadmap checkboxes.
- Follow Conventional Commits if possible.
