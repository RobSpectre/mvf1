# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `mvf1` - a Python package, command line interface, and MCP (Model Context Protocol) server for controlling MultiViewer video players. MultiViewer is a desktop application for watching Formula 1 and other motorsports with multiple synchronized video streams.

## Key Architecture

### Core Components

- **`mvf1/mvf1.py`**: Main library with `MultiViewerForF1` class and `Player` class
  - `MultiViewerForF1`: Primary interface for controlling MultiViewer via GraphQL API (localhost:10101)
  - `Player`: Represents individual video players with methods for control (pause, mute, seek, etc.)
  - Communicates with MultiViewer desktop app via GraphQL at `http://localhost:10101/api/graphql`

- **`mvf1/mcp.py`**: FastMCP server implementation exposing MultiViewer controls as MCP tools
  - Provides AI agents with tools to control video players
  - Tools include: `f1_live_timing_state()`, `players()`, `player_create()`, `player_delete()`, etc.

- **`mvf1/cmdline.py`**: Click-based CLI with two main command groups
  - `players`: Control all players (list, close, mute, pause, sync)
  - `player`: Control specific player by ID or title

- **`mvf1/mvf1_schema.py`**: Auto-generated GraphQL schema definitions using sgqlc

### Key Features

- **Player Management**: Create, delete, control individual video players
- **Live Timing Integration**: Access F1 and WEC live timing data
- **Synchronization**: Sync all players to commentary or specific player timestamp
- **MCP Integration**: Expose functionality to AI agents via Model Context Protocol

## Development Commands

### Testing
```bash
# Run all tests across Python versions
tox

# Run tests with coverage
pytest --cov=./
```

### Installation
```bash
# Install in development mode
pip install -e ./
```

### CLI Usage
```bash
# List all active players
mvf1-cli players ls

# Run MCP server with default URL
mvf1-cli mcp

# Run MCP server with custom URL
mvf1-cli mcp --url http://192.168.1.100:10101/api/graphql
```

## Dependencies

- **sgqlc**: GraphQL client for communicating with MultiViewer
- **click**: Command line interface framework
- **fastmcp**: MCP server implementation

## Testing Notes

- Tests are in `tests/` directory
- Uses pytest with asyncio support
- Tox configuration tests Python 3.10-3.13
- Test data includes `players.json` fixture