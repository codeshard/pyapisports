from unittest.mock import MagicMock

import httpx
import pytest

from pyapisports.client import ApiSportsClient
from pyapisports.football.resources import FootballResource

API_KEY = "test_api_key_123"


@pytest.fixture
def client():
    return ApiSportsClient(api_key=API_KEY)


class TestClientConstruction:
    def test_football_resource_is_attached(self, client):
        assert isinstance(client.football, FootballResource)

    def test_football_resource_references_client(self, client):
        assert client.football._client is client

    def test_base_url_is_set(self, client):
        assert str(client._http.base_url) == f"{ApiSportsClient.BASE_URL}"

    def test_api_key_header_is_set(self, client):
        assert client._http.headers["x-apisports-key"] == API_KEY

    def test_default_timeout(self, client):
        assert client._http.timeout.read == 10

    def test_custom_timeout(self):
        c = ApiSportsClient(api_key=API_KEY, timeout=30)
        assert c._http.timeout.read == 30

    def test_different_api_keys_are_independent(self):
        c1 = ApiSportsClient(api_key="key_one")
        c2 = ApiSportsClient(api_key="key_two")
        assert c1._http.headers["x-apisports-key"] == "key_one"
        assert c2._http.headers["x-apisports-key"] == "key_two"


class TestClientGet:
    def test_returns_parsed_json(self, client):
        payload = {"get": "status", "response": {"account": {}}}
        mock_response = MagicMock()
        mock_response.json.return_value = payload
        mock_response.raise_for_status = MagicMock()
        client._http.get = MagicMock(return_value=mock_response)

        result = client._get("/status")

        assert result == payload

    def test_calls_correct_endpoint(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        client._http.get = MagicMock(return_value=mock_response)

        client._get("/status")

        client._http.get.assert_called_once_with("/status", params=None)

    def test_passes_params(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        client._http.get = MagicMock(return_value=mock_response)

        client._get("/leagues", params={"season": 2024, "country": "England"})

        client._http.get.assert_called_once_with(
            "/leagues", params={"season": 2024, "country": "England"}
        )

    def test_no_params_by_default(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        client._http.get = MagicMock(return_value=mock_response)

        client._get("/timezone")

        client._http.get.assert_called_once_with("/timezone", params=None)

    def test_calls_raise_for_status(self, client):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        client._http.get = MagicMock(return_value=mock_response)

        client._get("/status")

        mock_response.raise_for_status.assert_called_once()

    def test_returns_list_response(self, client):
        payload = {"response": ["Africa/Abidjan", "Africa/Accra"]}
        mock_response = MagicMock()
        mock_response.json.return_value = payload
        mock_response.raise_for_status = MagicMock()
        client._http.get = MagicMock(return_value=mock_response)

        result = client._get("/timezone")

        assert result == payload


class TestClientGetErrors:
    def _make_http_error(self, status_code: int) -> httpx.HTTPStatusError:
        request = httpx.Request(
            "GET", "https://v3.football.api-sports.io/status"
        )
        response = httpx.Response(status_code, request=request)
        return httpx.HTTPStatusError(
            f"{status_code} error",
            request=request,
            response=response,
        )

    def test_raises_on_401(self, client):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = self._make_http_error(401)
        client._http.get = MagicMock(return_value=mock_response)

        with pytest.raises(httpx.HTTPStatusError):
            client._get("/status")

    def test_raises_on_429(self, client):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = self._make_http_error(429)
        client._http.get = MagicMock(return_value=mock_response)

        with pytest.raises(httpx.HTTPStatusError):
            client._get("/status")

    def test_raises_on_500(self, client):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = self._make_http_error(500)
        client._http.get = MagicMock(return_value=mock_response)

        with pytest.raises(httpx.HTTPStatusError):
            client._get("/status")

    def test_raises_on_network_error(self, client):
        client._http.get = MagicMock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(httpx.ConnectError):
            client._get("/status")


class TestClientContextManager:
    def test_enter_returns_client(self):
        client = ApiSportsClient(api_key=API_KEY)
        result = client.__enter__()
        assert result is client
        client._http.close()

    def test_exit_closes_http_client(self):
        client = ApiSportsClient(api_key=API_KEY)
        client._http.close = MagicMock()

        client.__exit__(None, None, None)

        client._http.close.assert_called_once()

    def test_with_block_closes_on_exit(self):
        client = ApiSportsClient(api_key=API_KEY)
        client._http.close = MagicMock()

        with client:
            pass

        client._http.close.assert_called_once()

    def test_with_block_closes_on_exception(self):
        client = ApiSportsClient(api_key=API_KEY)
        client._http.close = MagicMock()

        with pytest.raises(ValueError):
            with client:
                raise ValueError("something went wrong")

        client._http.close.assert_called_once()

    def test_with_block_returns_client_instance(self):
        with ApiSportsClient(api_key=API_KEY) as c:
            assert isinstance(c, ApiSportsClient)
