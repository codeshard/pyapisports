from typing import Any

import httpx

from pyapisports.resources import FootballResource


class ApiSportsClient:
    BASE_URL = "https://v3.football.api-sports.io"

    def __init__(self, api_key: str, timeout: int = 10):
        self._http = httpx.Client(
            base_url=self.BASE_URL,
            headers={"x-apisports-key": api_key},
            timeout=timeout,
        )
        self.football = FootballResource(self)

    def _get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | Any:
        response = self._http.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def __enter__(self) -> "ApiSportsClient":
        return self

    def __exit__(self, *args: tuple[str, Any]) -> None:
        self._http.close()
