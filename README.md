# housecanary-mcp

An MCP wrapper for the HouseCanary Analytics and Portfolio Monitoring APIs. Access HouseCanary's proprietary analytics and public records data across multiple geographic levels—from individual properties to states—with support for v2 and v3 endpoints. Includes endpoints for property valuation, rental estimates, market analysis, disaster risk assessment, school information, and portfolio management.

## Install

```bash
pip install housecanary-mcp
```

For local development in this repository:

```bash
pip install -e .
```

## Authentication

You can provide credentials with CLI options or environment variables.

- `--username` or `HOUSECANARY_API_USERNAME` (fallback: `HOUSECANARY_API_KEY`)
- `--password` or `HOUSECANARY_API_PASSWORD` (fallback: `HOUSECANARY_API_SECRET`)

Both username and password must be provided together if either is set.

## Usage (stdio default)

All commands in this section use the default MCP stdio transport.

```bash
housecanary-mcp
```

or:

```bash
housecanary-mcp --username "$HOUSECANARY_API_USERNAME" --password "$HOUSECANARY_API_PASSWORD"
```

## Run with uv (no project download)

`housecanary-mcp` is also published to PyPI, you can run it directly with `uv` without cloning this repository.

These examples also use stdio transport by default.

One-off execution:

```bash
uvx housecanary-mcp
```

Equivalent command using `uv run`:

```bash
uv run --with housecanary-mcp housecanary-mcp
```

With credentials:

```bash
HOUSECANARY_API_USERNAME="$HOUSECANARY_API_USERNAME" HOUSECANARY_API_PASSWORD="$HOUSECANARY_API_PASSWORD" uvx housecanary-mcp
```

With credentials passed as CLI args:

```bash
uvx housecanary-mcp --username "$HOUSECANARY_API_USERNAME" --password "$HOUSECANARY_API_PASSWORD"
```

Equivalent `uv run` form with credential args:

```bash
uv run --with housecanary-mcp housecanary-mcp --username "$HOUSECANARY_API_USERNAME" --password "$HOUSECANARY_API_PASSWORD"
```

## HTTP transport

To run the MCP server over HTTP instead of stdio, set FastMCP transport env vars.

Published package:

```bash
FASTMCP_TRANSPORT=http FASTMCP_HOST=127.0.0.1 FASTMCP_PORT=8000 FASTMCP_STREAMABLE_HTTP_PATH=/mcp uvx housecanary-mcp
```

Local project source:

```bash
FASTMCP_TRANSPORT=http FASTMCP_HOST=127.0.0.1 FASTMCP_PORT=8000 FASTMCP_STREAMABLE_HTTP_PATH=/mcp uv run --project /path/to/hcs-mcp housecanary-mcp
```

With credentials:

```bash
HOUSECANARY_API_USERNAME="$HOUSECANARY_API_USERNAME" HOUSECANARY_API_PASSWORD="$HOUSECANARY_API_PASSWORD" FASTMCP_TRANSPORT=http FASTMCP_HOST=127.0.0.1 FASTMCP_PORT=8000 FASTMCP_STREAMABLE_HTTP_PATH=/mcp uv run --project /path/to/hcs-mcp housecanary-mcp
```

Default HTTP endpoint URL:

- `http://127.0.0.1:8000/mcp`

## OpenAPI spec location

The canonical OpenAPI spec file is:

- `src/housecanary_mcp/openapi.yaml`

## Development checks

```bash
pytest
python -m build
```
