import json
from datetime import date

import pytest

from pyapisports.exceptions import APISportsError


class TestGetCountries:
    def test_no_params_by_default(
        self, football, mock_client, countries_payload
    ):
        mock_client._get.return_value = countries_payload
        football.get_countries()
        mock_client._get.assert_called_once_with("/countries", params={})

    def test_passes_name(self, football, mock_client, countries_payload):
        mock_client._get.return_value = countries_payload
        football.get_countries(name="England")
        mock_client._get.assert_called_once_with(
            "/countries", params={"name": "England"}
        )

    def test_passes_code(self, football, mock_client, countries_payload):
        mock_client._get.return_value = countries_payload
        football.get_countries(code="GB")
        mock_client._get.assert_called_once_with(
            "/countries", params={"code": "GB"}
        )

    def test_passes_search(self, football, mock_client, countries_payload):
        mock_client._get.return_value = countries_payload
        football.get_countries(search="engl")
        mock_client._get.assert_called_once_with(
            "/countries", params={"search": "engl"}
        )


class TestGetSeasons:
    def test_calls_correct_endpoint(
        self, football, mock_client, seasons_payload
    ):
        mock_client._get.return_value = seasons_payload
        football.get_seasons()
        mock_client._get.assert_called_once_with("/leagues/seasons")

    def test_returns_seasons_list(
        self, football, mock_client, seasons_payload
    ):
        mock_client._get.return_value = seasons_payload
        result = football.get_seasons()
        assert result is not None

    def test_length(self, football, mock_client, seasons_payload):
        mock_client._get.return_value = seasons_payload
        result = football.get_seasons()
        assert len(result) == 5

    def test_contains_year(self, football, mock_client, seasons_payload):
        mock_client._get.return_value = seasons_payload
        result = football.get_seasons()
        assert 2018 in result
        assert 1900 not in result

    def test_iterable(self, football, mock_client, seasons_payload):
        mock_client._get.return_value = seasons_payload
        result = football.get_seasons()
        assert list(result) == [2015, 2016, 2017, 2018, 2019]

    def test_to_list(self, football, mock_client, seasons_payload):
        mock_client._get.return_value = seasons_payload
        result = football.get_seasons()
        assert result.to_list() == [2015, 2016, 2017, 2018, 2019]

    def test_to_json(self, football, mock_client, seasons_payload):
        mock_client._get.return_value = seasons_payload
        result = football.get_seasons()
        assert json.loads(result.to_json()) == [2015, 2016, 2017, 2018, 2019]


class TestGetLeaguesParams:
    def test_no_params_by_default(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        football.get_leagues()
        mock_client._get.assert_called_once_with("/leagues", params={})

    def test_passes_id(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(id=39)
        mock_client._get.assert_called_once_with("/leagues", params={"id": 39})

    def test_passes_name(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(name="Premier League")
        mock_client._get.assert_called_once_with(
            "/leagues", params={"name": "Premier League"}
        )

    def test_passes_country(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(country="England")
        mock_client._get.assert_called_once_with(
            "/leagues", params={"country": "England"}
        )

    def test_passes_code(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(code="GB")
        mock_client._get.assert_called_once_with(
            "/leagues", params={"code": "GB"}
        )

    def test_passes_season(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(season=2019)
        mock_client._get.assert_called_once_with(
            "/leagues", params={"season": 2019}
        )

    def test_passes_current_true(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(current=True)
        mock_client._get.assert_called_once_with(
            "/leagues", params={"current": "true"}
        )

    def test_passes_current_false(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(current=False)
        mock_client._get.assert_called_once_with(
            "/leagues", params={"current": "false"}
        )

    def test_passes_search(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(search="prem")
        mock_client._get.assert_called_once_with(
            "/leagues", params={"search": "prem"}
        )

    def test_passes_multiple_params(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        football.get_leagues(country="England", season=2019, current=True)
        mock_client._get.assert_called_once_with(
            "/leagues",
            params={"country": "England", "season": 2019, "current": "true"},
        )


class TestGetLeaguesList:
    def test_returns_league_list(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert result is not None

    def test_length(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert len(result) == 1

    def test_iterable(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        leagues = list(result)
        assert len(leagues) == 1

    def test_find_by_id(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert result.find_by_id(39).name == "Premier League"

    def test_find_by_id_not_found(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert result.find_by_id(999) is None

    def test_find_by_name(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert result.find_by_name("Premier League").id == 39

    def test_find_by_name_case_insensitive(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert result.find_by_name("premier league") == result.find_by_name(
            "Premier League"
        )

    def test_find_by_name_not_found(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert result.find_by_name("Nonexistent") is None

    def test_filter_by_country(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        filtered = result.filter_by_country("GB")
        assert len(filtered) == 1
        assert filtered[0].name == "Premier League"

    def test_filter_by_country_no_match(
        self, football, mock_client, leagues_payload
    ):
        mock_client._get.return_value = leagues_payload
        result = football.get_leagues()
        assert len(result.filter_by_country("ZZ")) == 0


class TestLeagueModel:
    @pytest.fixture
    def pl(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        return football.get_leagues()[0]

    def test_league_fields(self, pl):
        assert pl.id == 39
        assert pl.name == "Premier League"
        assert pl.type == "League"
        assert pl.logo == "https://media.api-sports.io/football/leagues/2.png"

    def test_country_fields(self, pl):
        assert pl.country.name == "England"
        assert pl.country.code == "GB"
        assert pl.country.flag == "https://media.api-sports.io/flags/gb.svg"

    def test_seasons_count(self, pl):
        assert len(pl.seasons) == 2

    def test_current_season(self, pl):
        assert pl.current_season.year == 2019

    def test_current_season_none_when_missing(
        self, football, mock_client, leagues_payload
    ):
        for s in leagues_payload["response"][0]["seasons"]:
            s["current"] = False
        mock_client._get.return_value = leagues_payload
        pl = football.get_leagues()[0]
        assert pl.current_season is None

    def test_season_lookup_by_year(self, pl):
        s = pl.season(2018)
        assert s is not None
        assert s.year == 2018

    def test_season_lookup_not_found(self, pl):
        assert pl.season(1800) is None

    def test_league_to_dict(self, pl):
        d = pl.to_dict()
        assert d["league"]["id"] == 39
        assert d["country"]["code"] == "GB"
        assert len(d["seasons"]) == 2

    def test_league_to_json(self, pl):
        parsed = json.loads(pl.to_json())
        assert parsed["league"]["name"] == "Premier League"


class TestSeasonModel:
    @pytest.fixture
    def seasons(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        return football.get_leagues()[0].seasons

    def test_start_is_date(self, seasons):
        assert isinstance(seasons[0].start, date)

    def test_end_is_date(self, seasons):
        assert isinstance(seasons[0].end, date)

    def test_start_value(self, seasons):
        assert seasons[0].start == date(2018, 8, 10)

    def test_end_value(self, seasons):
        assert seasons[0].end == date(2019, 5, 12)

    def test_current_false(self, seasons):
        assert seasons[0].current is False
        assert seasons[0].is_active is False

    def test_current_true(self, seasons):
        assert seasons[1].current is True
        assert seasons[1].is_active is True

    def test_season_to_dict(self, seasons):
        d = seasons[0].to_dict()
        assert d["year"] == 2018
        assert d["start"] == "2018-08-10"
        assert d["end"] == "2019-05-12"
        assert d["current"] is False

    def test_season_to_json(self, seasons):
        parsed = json.loads(seasons[0].to_json())
        assert parsed["year"] == 2018


class TestCoverageModel:
    @pytest.fixture
    def coverage(self, football, mock_client, leagues_payload):
        mock_client._get.return_value = leagues_payload
        return football.get_leagues()[0].seasons[0].coverage

    def test_standings(self, coverage):
        assert coverage.standings is True

    def test_players(self, coverage):
        assert coverage.players is True

    def test_injuries_false(self, coverage):
        assert coverage.injuries is False

    def test_odds_false(self, coverage):
        assert coverage.odds is False

    def test_fixture_coverage_events(self, coverage):
        assert coverage.fixtures.events is True

    def test_fixture_coverage_lineups(self, coverage):
        assert coverage.fixtures.lineups is True

    def test_fixture_coverage_statistics(self, coverage):
        assert coverage.fixtures.statistics_fixtures is True
        assert coverage.fixtures.statistics_players is True

    def test_coverage_to_dict(self, coverage):
        d = coverage.to_dict()
        assert d["standings"] is True
        assert d["fixtures"]["events"] is True
        assert d["odds"] is False


class TestVenueModel:
    @pytest.fixture
    def pl(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        return football.get_venues(search="manches")[0]

    def test_venue_fields(self, pl):
        assert pl.id == 556
        assert pl.name == "Old Trafford"
        assert pl.city == "Manchester"

    def test_league_to_dict(self, pl):
        d = pl.to_dict()
        assert d["id"] == 556
        assert d["name"] == "Old Trafford"

    def test_league_to_json(self, pl):
        parsed = json.loads(pl.to_json())
        assert parsed["name"] == "Old Trafford"


class TestGetVenuesList:
    def test_returns_venues_list(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(search="manches")
        assert result is not None

    def test_length(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(search="manches")
        assert len(result) == 1

    def test_iterable(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(search="manches")
        leagues = list(result)
        assert len(leagues) == 1

    def test_find_by_name(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(name="Old Trafford")
        assert result.find_by_name("Old Trafford").id == 556

    def test_find_by_name_case_insensitive(
        self, football, mock_client, venues_payload
    ):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(search="manches")
        assert result.find_by_name("old trafford") == result.find_by_name(
            "Old Trafford"
        )

    def test_find_by_name_not_found(
        self, football, mock_client, venues_payload
    ):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(search="manches")
        assert result.find_by_name("Nonexistent") is None

    def test_filter_by_country(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        result = football.get_venues(id=556)
        filtered = result.find_by_country("england")
        assert filtered.name == "Old Trafford"


class TestGetVenuesValidation:
    def test_raises_when_no_params(self, football):
        with pytest.raises(
            APISportsError, match="At least one parameter must be provided"
        ):
            football.get_venues()


class TestGetTeamsInfo:
    def test_raises_when_no_params(self, football):
        with pytest.raises(
            APISportsError, match="At least one parameter must be provided"
        ):
            football.get_teams_info()

    def test_passes_id(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        football.get_teams_info(id=33)
        mock_client._get.assert_called_once_with("/teams", params={"id": 33})

    def test_passes_name(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        football.get_teams_info(name="Manchester United")
        mock_client._get.assert_called_once_with(
            "/teams", params={"name": "Manchester United"}
        )

    def test_passes_league(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        football.get_teams_info(league="39")
        mock_client._get.assert_called_once_with(
            "/teams", params={"league": "39"}
        )

    def test_passes_season(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        football.get_teams_info(season=2019)
        mock_client._get.assert_called_once_with(
            "/teams", params={"season": 2019}
        )

    def test_passes_multiple_params(
        self, football, mock_client, teams_payload
    ):
        mock_client._get.return_value = teams_payload
        football.get_teams_info(id=33, season=2019)
        mock_client._get.assert_called_once_with(
            "/teams", params={"id": 33, "season": 2019}
        )

    def test_returns_team_list(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        result = football.get_teams_info(id=33)
        assert result is not None

    def test_length(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        result = football.get_teams_info(id=33)
        assert len(result) == 3

    def test_iterable(self, football, mock_client, teams_payload):
        mock_client._get.return_value = teams_payload
        result = football.get_teams_info(id=33)
        assert len(list(result)) == 3


class TestGetTeamStatistics:
    def test_passes_required_params(
        self, football, mock_client, teams_statistics_payload
    ):
        mock_client._get.return_value = teams_statistics_payload
        football.get_team_statistics(team=33, league=39, season=2019)
        mock_client._get.assert_called_once_with(
            "/teams/statistics",
            params={"team": 33, "league": 39, "season": 2019},
        )

    def test_passes_date(
        self, football, mock_client, teams_statistics_payload
    ):
        mock_client._get.return_value = teams_statistics_payload
        football.get_team_statistics(
            team=33, league=39, season=2019, date="2019-12-01"
        )
        mock_client._get.assert_called_once_with(
            "/teams/statistics",
            params={
                "team": 33,
                "league": 39,
                "season": 2019,
                "date": "2019-12-01",
            },
        )

    def test_returns_team_statistics(
        self, football, mock_client, teams_statistics_payload
    ):
        mock_client._get.return_value = teams_statistics_payload
        result = football.get_team_statistics(team=33, league=39, season=2019)
        assert result is not None

    def test_no_date_by_default(
        self, football, mock_client, teams_statistics_payload
    ):
        mock_client._get.return_value = teams_statistics_payload
        football.get_team_statistics(team=33, league=39, season=2019)
        call_params = mock_client._get.call_args[1]["params"]
        assert "date" not in call_params


class TestGetVenuesParams:
    def test_passes_city(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        football.get_venues(city="Manchester")
        mock_client._get.assert_called_once_with(
            "/venues", params={"city": "Manchester"}
        )

    def test_passes_country(self, football, mock_client, venues_payload):
        mock_client._get.return_value = venues_payload
        football.get_venues(country="England")
        mock_client._get.assert_called_once_with(
            "/venues", params={"country": "England"}
        )


class TestGetTeamSeasons:
    def test_passes_team(self, football, mock_client, seasons_list_data):
        mock_client._get.return_value = seasons_list_data
        football.get_team_seasons(team=33)
        mock_client._get.assert_called_once_with(
            "/teams/seasons", params={"team": 33}
        )

    def test_returns_team_seasons_list(
        self, football, mock_client, seasons_list_data
    ):
        mock_client._get.return_value = seasons_list_data
        result = football.get_team_seasons(team=33)
        assert result is not None
        assert 2020 in result


class TestGetTeamCountries:
    def test_calls_correct_endpoint(self, football, mock_client):
        mock_client._get.return_value = {"response": []}
        football.get_team_countries()
        mock_client._get.assert_called_once_with("/teams/countries")

    def test_returns_team_country_list(self, football, mock_client):
        mock_client._get.return_value = {
            "response": [
                {
                    "name": "England",
                    "code": "GB",
                    "flag": "https://example.com/gb.svg",
                },
                {
                    "name": "France",
                    "code": "FR",
                    "flag": "https://example.com/fr.svg",
                },
            ]
        }
        result = football.get_team_countries()
        assert result is not None
        assert len(result) == 2


class TestGetStandings:
    def test_passes_league_and_season(
        self, football, mock_client, standings_payload
    ):
        mock_client._get.return_value = standings_payload
        football.get_standings(league=39, season=2024)
        mock_client._get.assert_called_once_with(
            "/standings", params={"league": 39, "season": 2024}
        )

    def test_passes_team_param(self, football, mock_client, standings_payload):
        mock_client._get.return_value = standings_payload
        football.get_standings(league=39, season=2024, team=50)
        mock_client._get.assert_called_once_with(
            "/standings", params={"league": 39, "season": 2024, "team": 50}
        )

    def test_returns_standings(self, football, mock_client, standings_payload):
        mock_client._get.return_value = standings_payload
        result = football.get_standings(league=39, season=2024)
        assert result is not None
