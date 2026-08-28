# AGENTS.md

## Project

`mvf1` is a Python library, CLI, and MCP server for controlling MultiViewer video players. It talks to the MultiViewer desktop app's GraphQL API at `http://localhost:10101/api/graphql` using `sgqlc`. The package is published on PyPI and runs on Python 3.10+.

## Layout

- `mvf1/mvf1.py` — `MultiViewerForF1` client and `Player` model
- `mvf1/mcp.py` — FastMCP server exposing MultiViewer controls as MCP tools
- `mvf1/cmdline.py` — Click CLI (`players`, `player`, `mcp` commands)
- `mvf1/mvf1_schema.py` — auto-generated GraphQL schema (do not hand-edit)
- `tests/` — pytest tests using `unittest.TestCase` style with mocks
- `docs/` — Sphinx docs
- `tox.ini` — test matrix for Python 3.10–3.13

## Setup

```bash
pip install -e ./
```

Requires Python >= 3.10. Dependencies: `click`, `sgqlc`, `fastmcp`.

## Commands

| Task | Command |
|---|---|
| Run tests (all Pythons) | `tox` |
| Run tests (current env) | `pytest --cov=./` |
| Run a single test file | `pytest tests/test_mvf1.py` |
| CLI help | `mvf1-cli --help` |
| Start MCP server | `mvf1-cli mcp` |
| Start MCP with custom URL | `mvf1-cli mcp --url http://<host>/api/graphql` |

## Conventions

- Tests use `unittest.TestCase` with `@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')` to mock GraphQL responses.
- Test fixtures live in `tests/players.json`.
- CLI commands catch `URLError` (MultiViewer not running) and `MultiViewerForF1Error` (GraphQL errors) and raise `click.UsageError`.
- MCP tools in `mvf1/mcp.py` wrap `MultiViewerForF1` client methods and are decorated with `@mcp.tool()`.
- README mentions `black` but no formatter/linter config files exist in the repo.

## Pitfalls

- **Player creation lag**: `player_create` is non-blocking; new players take 200–800 ms to appear in the API. Callers must delay before querying the new player.
- **Tests require no live server**: all HTTP calls are mocked; do not hit `localhost:10101` in tests.
- `mvf1/mvf1_schema.py` is auto-generated; hand edits will be overwritten.
