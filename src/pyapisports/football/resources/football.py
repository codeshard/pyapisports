from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyapisports.exceptions import APISportsError
from pyapisports.football.models import (
    CountryList,
    Fixture,
    FixtureList,
    LeagueList,
    RoundsList,
    SeasonsList,
    Standings,
    TeamCountryList,
    TeamInfoList,
    TeamSeasonsList,
    TeamStatistics,
    VenueList,
)
from pyapisports.football.resources import BaseResource

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
    ) -> TeamInfoList:
        """Retrieve a  list of available teams.
        The team id are unique in the API.
        At least one parameter is required.

        Returns:
            TeamInfoList: List of available teams.

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
        return TeamInfoList.from_api(raw)

    def get_team_statistics(
        self,
        team: int,
        league: int,
        season: int,
        date: str | None = None,
    ) -> TeamStatistics:
        """Retrieve aggregated season statistics for a team in a specific
        league.

        All three of `team`, `league`, and `season` are required by the API.
        Pass `date` to calculate stats up to a specific point in the season
        rather than up to today.

        Returns:
            TeamStatistics: Statistics of a team in relation to a given
            competition and season.

        Example:
            >>> stats = client.resource.get_team_statistics(
                    team=33, league=39, season=2024
                )
            >>> stats.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Teams/operation/get-teams-statistics"""
        params: dict[str, Any] = {
            "team": team,
            "league": league,
            "season": season,
        }
        if date:
            params["date"] = date
        raw = self._client._get("/teams/statistics", params=params)
        return TeamStatistics.from_api(raw)

    def get_team_seasons(self, team: int) -> TeamSeasonsList:
        """Retrieve the list of seasons available for a team.

        The team is is required by the API.

        Returns:
            TeamSeasonsList: List of seasons.

        Example:
            >>> seasons = client.resource.get_team_seasons(team=33)
            >>> seasons.to_json()

        API Reference:
            GET https://www.api-football.com/documentation-v3#tag/Teams/operation/get-teams-seasons"""
        params: dict[str, Any] = {"team": team}
        raw = self._client._get("/teams/seasons", params=params)
        return TeamSeasonsList.from_api(data=raw)

    def get_team_countries(self) -> TeamCountryList:
        """Retrieve the list of of countries available for the teams endpoint.

        Returns:
            TeamCountryList: List of countries.

        Example:
            >>> countries = client.resource.get_team_countries()
            >>> countries.to_json()

        API Reference:
            GET https://api-sports.io/documentation/football/v3#tag/Teams/operation/get-teams-countries"""
        raw = self._client._get("/teams/countries")
        return TeamCountryList.from_api(raw)

    def get_standings(
        self,
        league: int,
        season: int,
        team: int | None = None,
    ) -> Standings:
        """
        Retrieve the standings table(s) for a league and season.

        Args:
            league:  League ID (required).
            season:  Season year, e.g. 2024 (required).
            team:    Optional team ID to filter down to a single team's row.

        Returns:
            Standings: Contains one or more StandingsTable objects.
            Single-table leagues (Premier League, La Liga, etc.) expose a
            `.table` shortcut. Multi-group competitions (Champions League,
            World Cup) expose the full `.tables` list.

        Example:
            >>> stands = client.football.get_standings(league=39, season=2024)
            >>> stands.to_json()

        API reference:
            GET https://api-sports.io/documentation/football/v3#tag/Standings/operation/get-standings
        """
        params: dict[str, Any] = {"league": league, "season": season}
        if team:
            params["team"] = team
        raw = self._client._get("/standings", params=params)
        return Standings.from_api(raw)

    def get_rounds(
        self,
        league: int,
        season: int,
        current: bool = False,
        dates: bool = False,
        timezone: str | None = None,
    ) -> RoundsList:
        """
        Retrieve the rounds for a league or a cup.

        Args:
            league:  League ID (required).
            season:  Season year, e.g. 2024 (required).
            current: The current round only (optional).
            dates:   Add the dates of each round in the response (Optional).

        Returns:
            RoundsList: Contains one or more rounds for a league or a cup.

        Example:
            >>> rounds = client.football.get_rounds(league=39, season=2019)

            >>> rounds.to_json()

        API reference:
            https://api-sports.io/documentation/football/v3#tag/Fixtures/operation/get-fixtures-rounds
        """
        params: dict[str, Any] = {"league": league, "season": season}
        if current:
            params["current"] = current
        if dates:
            params["dates"] = dates
        if timezone:
            params["timezone"] = timezone
        raw = self._client._get("/fixtures/rounds", params=params)
        return RoundsList.from_api(raw)

    def get_fixtures(
        self,
        id: int | None = None,
        ids: list[int] | None = None,
        live: str | None = None,
        date: str | None = None,
        league: int | None = None,
        season: int | None = None,
        team: int | None = None,
        round: str | None = None,
        status: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        last: int | None = None,
        next: int | None = None,
        timezone: str | None = None,
    ) -> FixtureList:
        """
        Retrieve fixtures with flexible filtering.

        Common patterns:
            # Live fixtures across all leagues
            get_fixtures(live="all")

            # Full season schedule
            get_fixtures(league=39, season=2024)

            # Today's matches in a league
            get_fixtures(league=39, season=2024, date="2024-12-01")

            # Team's last 5 results
            get_fixtures(team=33, last=5)

            # Team's next 10 fixtures
            get_fixtures(team=33, next=10)

            # Date range
            get_fixtures(league=39, season=2024, from_date="2024-12-01",
                to_date="2024-12-31")

            # Batch by IDs (up to 20)
            get_fixtures(ids=[868078, 868079, 868080])

        Args:
            id: The id of the fixture
            ids: One or more fixture ids
            live: All or several leagues ids
            date: A valid date
            league: The id of the league
            season: The season of the league
            team: The id of the team
            last: For the X last fixtures
            next: For the X next fixtures
            from: A valid date
            to: A valid date
            round: The round of the fixture
            status: One or more fixture status short
            vanue: The venue id of the fixture
            timezone: A valid timezone from the endpoint get_timezones()

        Returns:
            FixtureList: Contains one or more fixtures.

        Example:
            >>> fixtures = client.football.get_fixtures(league=39, season=2019)

            >>> fixtures.to_json()

        API reference:
            https://api-sports.io/documentation/football/v3#tag/Fixtures/operation/get-fixtures
        """
        params: dict[str, Any] = {}

        if id is not None:
            params["id"] = id
        if ids is not None:
            params["ids"] = "-".join(str(i) for i in ids)
        if live is not None:
            params["live"] = live
        if date is not None:
            params["date"] = date
        if league is not None:
            params["league"] = league
        if season is not None:
            params["season"] = season
        if team is not None:
            params["team"] = team
        if round is not None:
            params["round"] = round
        if status is not None:
            params["status"] = status
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if last is not None:
            params["last"] = last
        if next is not None:
            params["next"] = next
        if timezone is not None:
            params["timezone"] = timezone

        raw = self._client._get("/fixtures", params=params)
        return FixtureList.from_api(raw)

    def get_fixture(self, id: int, timezone: str | None = None) -> Fixture:
        """
        Retrieve a single fixture by ID.

        Convenience wrapper around get_fixtures() that returns a Fixture
        directly rather than a FixtureList.

        Args:
            id:       Fixture ID (required).
            timezone: Optional timezone string for kickoff localisation.

        Returns:
            Fixture: The requested fixture.

        Raises:
            APISportsError: If the fixture ID is not found in the response.

        API reference:
            https://api-sports.io/documentation/football/v3#tag/Fixtures/operation/get-fixtures
        """
        result = self.get_fixtures(id=id, timezone=timezone)
        if not result:
            raise APISportsError(f"Fixture {id} not found.")
        return result[0]
