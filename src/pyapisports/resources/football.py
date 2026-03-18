from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyapisports.models import LeagueList, SeasonsList
from pyapisports.resources import BaseResource

if TYPE_CHECKING:
    from pyapisports.client import ApiSportsClient


class FootballResource(BaseResource):
    def __init__(self, client: ApiSportsClient):
        self._client = client

    def get_seasons(self) -> SeasonsList:
        raw = self._client._get("/leagues/seasons")
        return SeasonsList.from_api(raw)

    def get_leagues(
        self,
        id: int | None = None,
        name: str | None = None,
        country: str | None = None,
        code: str | None = None,
        season: int | None = None,
        current: bool | None = None,
        search: str | None = None,
    ) -> LeagueList:
        params: dict[str, Any] = {}
        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if country:
            params["country"] = country
        if code:
            params["code"] = code
        if season:
            params["season"] = season
        if current is not None:
            params["current"] = "true" if current else "false"
        if search:
            params["search"] = search

        raw = self._client._get("/leagues", params=params)
        return LeagueList.from_api(raw)
