PY_SRC=src/nautobot_mcp_server

.PHONY: install fmt lint typecheck test coverage run docs-serve

install:
	pip install -e ./src[dev]

fmt:
	black $(PY_SRC) tests
	isort $(PY_SRC) tests

lint:
	ruff check $(PY_SRC) tests
	black --check $(PY_SRC) tests
	isort --check-only $(PY_SRC) tests
	test -z "$(shell mypy $(PY_SRC) | tee /dev/stderr)"

typecheck:
	mypy $(PY_SRC)

test:
	pytest -q --maxfail=1 --disable-warnings

coverage:
	pytest --cov=nautobot_mcp_server --cov-report=term-missing

run:
	nautobot-mcp-server

docs-serve:
	mkdocs serve
