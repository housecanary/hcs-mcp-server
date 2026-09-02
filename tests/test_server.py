from unittest.mock import patch

import httpx
import pytest

from housecanary_mcp import __version__, server


def test_build_client_requires_server_url() -> None:
    with pytest.raises(ValueError, match="No server URL"):
        server.build_client({}, None, None)


def test_build_client_requires_auth_pair() -> None:
    with pytest.raises(ValueError, match="Both username and password"):
        server.build_client({"servers": [{"url": "https://example.com"}]}, "u", None)


@patch("housecanary_mcp.server.FastMCP.from_openapi")
@patch("housecanary_mcp.server.build_client")
@patch("housecanary_mcp.server.load_openapi_spec")
def test_create_server_smoke(
    load_openapi_spec_mock,
    build_client_mock,
    from_openapi_mock,
) -> None:
    load_openapi_spec_mock.return_value = {"servers": [{"url": "https://example.com"}]}
    fake_client = object()
    fake_server = object()
    build_client_mock.return_value = fake_client
    from_openapi_mock.return_value = fake_server

    result = server.create_server("user", "pass")

    assert result is fake_server
    build_client_mock.assert_called_once_with(load_openapi_spec_mock.return_value, "user", "pass")


def test_build_client_sends_x_caller() -> None:
    client = server.build_client({"servers": [{"url": "https://example.com"}]}, None, None)

    assert client.headers["X-Caller"] == "housecanary-mcp"


def test_x_caller_is_unversioned() -> None:
    # x_caller is varchar(100) and usage reporting groups by it, so the value must stay
    # stable across releases. Version detail belongs in User-Agent.
    assert server.X_CALLER == "housecanary-mcp"

    client = server.build_client({"servers": [{"url": "https://example.com"}]}, None, None)

    assert client.headers["User-Agent"] == f"housecanary-mcp/{__version__}"


def test_build_client_sends_x_caller_with_auth() -> None:
    client = server.build_client(
        {"servers": [{"url": "https://example.com"}]}, "user", "pass"
    )

    assert client.headers["X-Caller"] == "housecanary-mcp"
    assert isinstance(client.auth, httpx.BasicAuth)
