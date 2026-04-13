# housecanary-mcp

A FastMCP server generated from the HouseCanary OpenAPI spec.

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

## Usage

```bash
housecanary-mcp
```

or:

```bash
housecanary-mcp --username "$HOUSECANARY_API_USERNAME" --password "$HOUSECANARY_API_PASSWORD"
```

## Run with uv (no project download)

`housecanary-mcp` is also published to PyPI, you can run it directly with `uv` without cloning this repository.

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

## OpenAPI spec location

The canonical OpenAPI spec file is:

- `src/housecanary_mcp/openapi.yaml`

## Development checks

```bash
pytest
python -m build
```
