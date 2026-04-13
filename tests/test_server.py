from unittest.mock import patch

import pytest

from housecanary_mcp import server


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
