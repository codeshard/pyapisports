import json
from datetime import date

import pytest


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
