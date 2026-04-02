from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyapisports.exceptions import APISportsError
from pyapisports.models import (
    CountryList,
    LeagueList,
    SeasonsList,
    TeamList,
    VenueList,
)
from pyapisports.resources import BaseResource

if TYPE_CHECKING:
    from pyapisports.client import ApiSportsClient


class FootballResource(BaseResource):
    def __init__(self, client: ApiSportsClient):
        self._client = client

    def get_countries(
        self,
        name: str | None = None,
        code: str | None = None,
        search: str | None = None,
    ) -> CountryList:
        """Retrieve a  list of available countries for the leagues endpoint.

        Args:
            name (str, optional): The name of the country
            code (str, optional): The Alpha code of the country
            search: (str, optional): The name of the country (+ 3 characters).

        Returns:
            CountryList: Collection of countries matching the query.

        Example:
            >>> countries = client.resource.get_countries()
            >>> countries.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Countries"""
        params = {}
        if name:
            params["name"] = name
        if code:
            params["code"] = code
        if search:
            params["search"] = search

        raw = self._client._get("/countries", params=params)
        return CountryList.from_api(raw)

    def get_seasons(self) -> SeasonsList:
        """Retrieve a  list of available seasons, that can be used in other
        endpoints as filters.

        Returns:
            SeasonsList: List of available seasons.

        Example:
            >>> seasons = client.resource.get_seasons()
            >>> seasons.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Leagues/operation/get-seasons"""
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
        """Retrieve a  list of available leagues and cups.
        The league id are unique in the API and leagues keep it across all
        seasons

        Returns:
            LeaguesList: List of available leagues and cups.

        Example:
            >>> leagues = client.resource.get_leagues()
            >>> leagues.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Leagues/operation/get-leagues"""
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

    def get_venues(
        self,
        id: int | None = None,
        name: str | None = None,
        city: str | None = None,
        country: str | None = None,
        search: str | None = None,
    ) -> VenueList:
        """Retrieve a  list of available venues.
        The venue id are unique in the API.
        At least one parameter is required.

        Returns:
            VenueList: List of available venues.

        Example:
            >>> venues = client.resource.get_venues(id=556)
            >>> venues.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Venues/operation/get-venues"""
        if not any([id, name, city, country, search]):
            raise APISportsError("At least one parameter must be provided")
        params: dict[str, Any] = {}
        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if city:
            params["city"] = city
        if country:
            params["country"] = country
        if search:
            params["search"] = search
        raw = self._client._get("/venues", params=params)
        return VenueList.from_api(raw)

    def get_teams_info(
        self,
        id: int | None = None,
        name: str | None = None,
        league: str | None = None,
        season: int | None = None,
        country: str | None = None,
        code: str | None = None,
        venue_id: int | None = None,
        search: str | None = None,
    ) -> TeamList:
        """Retrieve a  list of available teams.
        The team id are unique in the API.
        At least one parameter is required.

        Returns:
            TeamList: List of available teams.

        Example:
            >>> teams = client.resource.get_teams(id=33)
            >>> teams.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Teams/operation/get-teams"""
        if not any(
            [id, name, league, season, country, code, venue_id, search]
        ):
            raise APISportsError("At least one parameter must be provided")
        params: dict[str, Any] = {}
        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        raw = self._client._get("/teams", params=params)
        return TeamList.from_api(raw)
