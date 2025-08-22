## Open Source Readiness Roadmap

This roadmap defines the work to make this project production‑ready and attractive for open‑source contributors. Each item is an actionable checkbox that Cursor can check off as work is completed. Keep checklists as the single source of truth for progress.

### How to use this file
- Check off items as they are completed in edits and pull requests.
- Prefer small PRs that each close one or a few checkboxes.
- If scope changes, add or refine items here first.

### Definitions of Done
- Code builds and runs locally and in CI.
- Linting, typing, and tests pass (coverage ≥ 85% for core modules).
- Docs updated for any user‑visible change.
- Security and auth implications considered and documented.

## Milestones (high level)
- [ ] M1: Core server stable (config/auth/health, API surface, Docker) 
- [ ] M2: Quality gates (tests, lint, type checks, coverage)
- [ ] M3: CI/CD (build, test, release, images)
- [ ] M4: Documentation site live (mkdocs + GitHub Pages)
- [ ] M5: Optional Chainlit UI pathway
- [ ] M6: Community readiness (CONTRIBUTING, templates, governance)
- [ ] M7: Demo mode + conference deliverables

## 1) Core packaging and runtime
- [x] Align module entrypoint and port defaults
  - [x] Update `src/Dockerfile` CMD to `python -m nautobot_mcp_server.server`
  - [x] Standardize default port to 7001 in `server.py` and Docker `EXPOSE`
  - [x] Update `README.md` examples to reflect correct port/module
- [ ] Single source of dependencies
  - [x] Use `src/pyproject.toml` as authoritative
  - [x] Ensure runtime deps (including `fastmcp`) are consistent across `pyproject.toml`/`requirements.txt`
  - [x] Document installation for dev and production
- [ ] Console entrypoint
  - [x] Add `[project.scripts] nautobot-mcp-server` in `pyproject.toml`
  - [x] Implement `main()` wrapper around `server.run()`

## 2) Configuration and customization (env + YAML)
- [x] Create `nautobot_mcp_server/settings.py` using `pydantic` (and optional YAML overlay)
- [x] Support precedence: env vars > YAML file > defaults
- [ ] Add `.env.example` with all keys and safe defaults
- [ ] Support org customization file (e.g., location aliases, naming schemas)
- [x] Wire settings into `clients/nautobot_graphql.py` and `server.py`

## 3) Authentication and security
- [ ] Pluggable auth via settings `AUTH_MODE`
  - [ ] `none` (for demo, with warning)
  - [x] `api_key` header (`X-API-Key`) with allow‑list
  - [ ] `basic` (optional simple protection)
  - [ ] `bearer`/`oidc` (JWT validation via issuer/JWKS) 
- [x] Apply auth dependency to `/tools` and `/tools/invoke`
- [x] Keep `/healthz` open (document rationale) or provide public/private modes
- [ ] Security docs: threat model and guidance for safe deployment

## 4) Tools API surface
- [ ] Reconcile tool references in `tools/llm_chat.py`
  - [ ] Implement `export_prefixes_to_csv`
  - [ ] Implement `analyze_prefixes_dataframe`
  - [ ] Or remove unused references and simplify help text
- [ ] OpenAPI/schema docs reflect tools and custom routes
- [ ] Examples for `GET /tools`, `POST /tools/invoke` (with auth where applicable)
 - [ ] Externalize GraphQL queries to versioned files for easy customization
  - [ ] Create `nautobot_mcp_server/graphql/` directory
  - [ ] Move queries into separate files:
    - [ ] `prefixes_by_location.graphql`
    - [ ] `devices_by_location.graphql`
    - [ ] `devices_by_location_and_role.graphql`
  - [ ] Load query text at runtime via `importlib.resources` (or equivalent)
  - [ ] Include `.graphql` files in package data (configure in `pyproject.toml`)
  - [ ] Document how users can modify queries to add attributes for their context
  - [ ] Add tests for query file loading and clear error messages when missing

## 5) Optional Chainlit UI pathway
- [ ] Create `chainlit_app/app.py` that calls API `/tools` and `/tools/invoke`
- [ ] Add `Dockerfile.chainlit` for Chainlit image
- [ ] Add `docker-compose.yml` with `api` and optional `chainlit` service
- [ ] Docs: using Chainlit vs API‑only, environment variables, example flows

## 6) Testing and quality gates
- [ ] Add dev dependencies: `pytest`, `pytest-asyncio`, `pytest-cov`, `requests-mock`/`responses`
- [ ] Unit tests
  - [ ] `clients/nautobot_graphql.py` (success/errors, timeouts)
  - [ ] `tools/prefixes.py` and `tools/devices.py` (mock client)
  - [ ] `settings` precedence (env vs YAML)
- [ ] Integration tests
  - [ ] Starlette/FastAPI TestClient for `/healthz`, `/tools`, `/tools/invoke`
  - [x] Auth modes (`none`, `api_key`) request coverage
- [ ] Coverage gate ≥ 85% for `nautobot_mcp_server/*`

## 7) CI/CD automation (GitHub Actions)
- [x] Add `.github/workflows/ci.yml`
  - [x] Lint: ruff, black, isort
  - [x] Type check: mypy
  - [x] Tests + coverage report
  - [ ] Build Docker
- [ ] Add CodeQL/security scan (optional)
  - [x] CodeQL workflow added
- [ ] On tags `v*`, build and push Docker image (GHCR)

## 8) Documentation site (MkDocs + Pages)
- [x] Add `mkdocs.yml` (Material theme)
- [x] Author docs pages in `docs/`
  - [x] Overview and Architecture
  - [x] Quickstart (Docker, local, compose)
  - [x] Configuration (env + YAML), examples
  - [x] Authentication modes
  - [x] API reference (tools and routes)
  - [x] Optional Chainlit UI (placeholder)
  - [x] Development Guide (install, run, test) (covered in contributing/quickstart)
  - [x] Contributing + Code of Conduct
  - [x] Security and responsible disclosure
- [x] Add `.github/workflows/docs.yml` for Pages deploy (manual only)

## 9) Community readiness
- [x] Add `CONTRIBUTING.md`
- [x] Add `CODE_OF_CONDUCT.md`
- [x] Add `SECURITY.md` (vuln reporting)
- [x] Add issue templates and PR template under `.github/`
- [x] Optional `CODEOWNERS`
- [ ] Enable Dependabot for `pip` and `actions`

## 10) Makefile, pre‑commit, and repo hygiene
- [x] Add `Makefile` targets: `install`, `fmt`, `lint`, `typecheck`, `test`, `coverage`, `build`, `run`, `docs-serve`
- [x] Add `.pre-commit-config.yaml` (black, isort, ruff, whitespace, EOF)
- [ ] Ensure consistent formatting and imports across project

## 11) Release and distribution
- [ ] Versioning policy and changelog
- [ ] Tag + GitHub Releases workflow
- [ ] Publish Docker image to GHCR
- [ ] (Optional) Publish Python package to PyPI

## 12) Demo mode and conference prep
- [ ] `DEMO_MODE` setting; static fixtures when Nautobot unavailable
- [ ] Sample `.env.demo` and example curl sequences
- [ ] Short demo script for Chainlit and API‑only paths
- [ ] Record fallback behavior in docs

## Current blockers/risks (track as needed)
- [ ] Clarify preferred auth modes for initial release
- [ ] Decide on YAML structure for environment customizations
- [ ] Confirm if Chainlit should call API or embed MCP client

## Backlog / Nice‑to‑have (post‑launch)
- [ ] OIDC/JWT validation with JWKS caching and clock skew handling
- [ ] Structured audit logs and request IDs
- [ ] Prometheus metrics endpoints and dashboards
- [ ] More Nautobot tools (sites, racks, circuits, VLANs)
- [ ] E2E tests with docker‑compose in CI


