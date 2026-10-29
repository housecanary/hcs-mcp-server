import argparse
import os
import sys
from contextlib import asynccontextmanager
from importlib.resources import files
from pathlib import Path

import httpx
import yaml
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import RouteMap, MCPType

from housecanary_mcp import __version__

DEFAULT_TIMEOUT = 30.0

# SPLAT-1770: tags MCP-originated traffic so it can be told apart from other API clients.
# The gateway forwards X-Caller untouched, and it is meant to reach
# reporting.billing_usage.x_caller. Keep it a stable, unversioned literal -- x_caller is
# varchar(100) and usage reporting groups by it, so a version suffix would fragment every
# report. Version detail goes in User-Agent instead.
X_CALLER = "housecanary-mcp"


def resolve_spec_path() -> Path:
    bundled_dir = getattr(sys, "_MEIPASS", None)
    if bundled_dir:
        bundled_spec = Path(bundled_dir) / "openapi.yaml"
        if bundled_spec.exists():
            return bundled_spec

    return Path(str(files("housecanary_mcp").joinpath("openapi.yaml")))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the HouseCanary MCP server.")
    parser.add_argument(
        "--username",
        default=(
            os.getenv("HOUSECANARY_API_USERNAME")
            or os.getenv("HOUSECANARY_API_KEY")
        ),
        help="API username or key. Defaults to HOUSECANARY_API_USERNAME, or HOUSECANARY_API_KEY.",
    )
    parser.add_argument(
        "--password",
        default=(
            os.getenv("HOUSECANARY_API_PASSWORD")
            or os.getenv("HOUSECANARY_API_SECRET")
        ),
        help="API password or secret. Defaults to HOUSECANARY_API_PASSWORD, or HOUSECANARY_API_SECRET.",
    )
    return parser.parse_args(argv)


def load_openapi_spec() -> dict:
    spec_path = resolve_spec_path()
    return yaml.safe_load(spec_path.read_text())


def build_client(
    openapi_spec: dict,
    username: str | None,
    password: str | None,
) -> httpx.AsyncClient:
    servers = openapi_spec.get("servers", [])
    if not servers or not servers[0].get("url"):
        raise ValueError("No server URL found in openapi.yaml")

    if bool(username) != bool(password):
        raise ValueError("Both username and password must be provided together")

    client_kwargs = {
        "base_url": servers[0]["url"],
        "timeout": DEFAULT_TIMEOUT,
        "headers": {
            "X-Caller": X_CALLER,
            "User-Agent": f"{X_CALLER}/{__version__}",
        },
    }
    if username and password:
        client_kwargs["auth"] = httpx.BasicAuth(username, password)

    return httpx.AsyncClient(**client_kwargs)


def create_server(username: str | None, password: str | None) -> FastMCP:
    openapi_spec = load_openapi_spec()
    client = build_client(openapi_spec, username, password)

    @asynccontextmanager
    async def server_lifespan(_: FastMCP):
        async with client:
            yield

    return FastMCP.from_openapi(
        openapi_spec,
        client=client,
        name="HouseCanary",
        lifespan=server_lifespan,
        route_maps=[
            RouteMap(methods=['POST'], mcp_type=MCPType.EXCLUDE),
            RouteMap(pattern=r'component_mget$', mcp_type=MCPType.EXCLUDE),
        ]
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    mcp = create_server(args.username, args.password)
    mcp.run()


if __name__ == "__main__":
    main()
