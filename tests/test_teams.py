import json

import pytest

from pyapisports.football.models import TeamInfo, TeamInfoList, Venue


@pytest.fixture
def team_list(teams_payload) -> TeamInfoList:
    return TeamInfoList.from_api(teams_payload)


@pytest.fixture
def man_utd(teams_payload) -> TeamInfo:
    return TeamInfo.from_api(teams_payload["response"][0])


@pytest.fixture
def az(teams_payload) -> TeamInfo:
    return TeamInfo.from_api(teams_payload["response"][2])


class TestTeamFromApi:
    def test_id(self, man_utd):
        assert man_utd.id == 33

    def test_name(self, man_utd):
        assert man_utd.name == "Manchester United"

    def test_code(self, man_utd):
        assert man_utd.code == "MUN"

    def test_country(self, man_utd):
        assert man_utd.country == "England"

    def test_founded(self, man_utd):
        assert man_utd.founded == 1878

    def test_founded_is_int(self, man_utd):
        assert isinstance(man_utd.founded, int)

    def test_national_false(self, man_utd):
        assert man_utd.national is False

    def test_national_true(self, az):
        assert az.national is True

    def test_logo(self, man_utd):
        assert (
            man_utd.logo == "https://media.api-sports.io/football/teams/33.png"
        )

    def test_venue_is_parsed(self, man_utd):
        assert isinstance(man_utd.venue, Venue)
        assert man_utd.venue.id == 556
        assert man_utd.venue.name == "Old Trafford"

    def test_nullable_code(self, az):
        assert az.code is None

    def test_nullable_country(self, az):
        assert az.country is None

    def test_nullable_founded(self, az):
        assert az.founded is None

    def test_nullable_venue(self, az):
        assert az.venue is None


class TestTeamToDict:
    def test_top_level_keys(self, man_utd):
        assert set(man_utd.to_dict().keys()) == {"team", "venue"}

    def test_team_block_keys(self, man_utd):
        assert set(man_utd.to_dict()["team"].keys()) == {
            "id",
            "name",
            "code",
            "country",
            "founded",
            "national",
            "logo",
        }

    def test_team_block_values(self, man_utd):
        t = man_utd.to_dict()["team"]
        assert t["id"] == 33
        assert t["name"] == "Manchester United"
        assert t["code"] == "MUN"
        assert t["country"] == "England"
        assert t["founded"] == 1878
        assert t["national"] is False

    def test_venue_block_present(self, man_utd):
        assert man_utd.to_dict()["venue"] is not None

    def test_venue_block_none_when_missing(self, az):
        assert az.to_dict()["venue"] is None

    def test_no_duplicate_team_key(self, man_utd):
        t = man_utd.to_dict()["team"]
        assert "team" not in t


class TestTeamToJson:
    def test_valid_json(self, man_utd):
        parsed = json.loads(man_utd.to_json())
        assert isinstance(parsed, dict)

    def test_json_values(self, man_utd):
        parsed = json.loads(man_utd.to_json())
        assert parsed["team"]["id"] == 33
        assert parsed["team"]["country"] == "England"

    def test_json_null_venue(self, az):
        parsed = json.loads(az.to_json())
        assert parsed["venue"] is None

    def test_json_indent_kwarg(self, man_utd):
        result = man_utd.to_json(indent=2)
        assert "\n" in result


class TestTeamListFromApi:
    def test_length(self, team_list):
        assert len(team_list) == 3

    def test_items_are_team_instances(self, team_list):
        for team in team_list:
            assert isinstance(team, TeamInfo)

    def test_empty_response(self):
        result = TeamInfoList.from_api({"response": []})
        assert len(result) == 0


class TestTeamListAccess:
    def test_iterable(self, team_list):
        names = [t.name for t in team_list]
        assert "Manchester United" in names
        assert "Liverpool" in names

    def test_getitem(self, team_list):
        assert team_list[0].id == 33

    def test_getitem_negative(self, team_list):
        assert team_list[-1].id == 99


class TestTeamListFinders:
    def test_find_by_id(self, team_list):
        team = team_list.find_by_id(33)
        assert team is not None
        assert team.name == "Manchester United"

    def test_find_by_id_not_found(self, team_list):
        assert team_list.find_by_id(9999) is None

    def test_find_by_name(self, team_list):
        team = team_list.find_by_name("Liverpool")
        assert team is not None
        assert team.id == 40

    def test_find_by_name_case_insensitive(self, team_list):
        assert team_list.find_by_name("liverpool") == team_list.find_by_name(
            "Liverpool"
        )

    def test_find_by_name_not_found(self, team_list):
        assert team_list.find_by_name("Real Madrid") is None


class TestTeamListFilters:
    def test_filter_by_country(self, team_list):
        result = team_list.filter_by_country("England")
        assert len(result) == 2
        assert all(t.country == "England" for t in result)

    def test_filter_by_country_case_insensitive(self, team_list):
        assert len(team_list.filter_by_country("england")) == 2
        assert len(team_list.filter_by_country("ENGLAND")) == 2

    def test_filter_by_country_no_match(self, team_list):
        assert len(team_list.filter_by_country("Brazil")) == 0

    def test_filter_by_country_skips_null_country(self, team_list):
        # AZ has country=None, should not raise
        result = team_list.filter_by_country("None")
        assert len(result) == 0

    def test_filter_by_code(self, team_list):
        result = team_list.filter_by_code("LIV")
        assert len(result) == 1
        assert result[0].name == "Liverpool"

    def test_filter_by_code_case_insensitive(self, team_list):
        assert len(team_list.filter_by_code("liv")) == 1

    def test_filter_by_code_no_match(self, team_list):
        assert len(team_list.filter_by_code("ZZZ")) == 0

    def test_filter_by_venue(self, team_list):
        result = team_list.filter_by_venue(556)
        assert len(result) == 1
        assert result[0].name == "Manchester United"

    def test_filter_by_venue_skips_null_venue(self, team_list):
        # AZ has venue=None, should not raise
        result = team_list.filter_by_venue(9999)
        assert len(result) == 0

    def test_filter_by_venue_no_match(self, team_list):
        assert len(team_list.filter_by_venue(1)) == 0

    def test_search_partial_match(self, team_list):
        result = team_list.search("united")
        assert len(result) == 1
        assert result[0].name == "Manchester United"

    def test_search_case_insensitive(self, team_list):
        assert len(team_list.search("UNITED")) == 1

    def test_search_no_match(self, team_list):
        assert len(team_list.search("barcelona")) == 0

    def test_search_returns_team_list(self, team_list):
        assert isinstance(team_list.search("liverpool"), TeamInfoList)

    def test_filter_returns_team_list(self, team_list):
        assert isinstance(team_list.filter_by_country("England"), TeamInfoList)


class TestTeamListSerialization:
    def test_to_list_returns_list_of_dicts(self, team_list):
        result = team_list.to_list()
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    def test_to_list_length(self, team_list):
        assert len(team_list.to_list()) == 3

    def test_to_list_values(self, team_list):
        first = team_list.to_list()[0]
        assert first["team"]["id"] == 33
        assert first["team"]["country"] == "England"

    def test_to_json_valid(self, team_list):
        parsed = json.loads(team_list.to_json())
        assert isinstance(parsed, list)
        assert len(parsed) == 3

    def test_to_json_indent(self, team_list):
        assert "\n" in team_list.to_json(indent=2)

    def test_to_json_null_venue_serializes(self, team_list):
        parsed = json.loads(team_list.to_json())
        az_entry = next(t for t in parsed if t["team"]["id"] == 99)
        assert az_entry["venue"] is None


class TestTeamSeasonsList:
    def test_from_api(self, seasons_list_data):
        from pyapisports.football.models import TeamSeasonsList

        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert sl.seasons == [
            2008,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
        ]

    def test_iter(self, seasons_list_data):
        from pyapisports.football.models import TeamSeasonsList

        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert list(sl) == [
            2008,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
        ]

    def test_len(self, seasons_list_data):
        from pyapisports.football.models import TeamSeasonsList

        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert len(sl) == 12

    def test_contains(self, seasons_list_data):
        from pyapisports.football.models import TeamSeasonsList

        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert 2018 in sl
        assert 1900 not in sl

    def test_to_list(self, seasons_list_data):
        from pyapisports.football.models import TeamSeasonsList

        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert isinstance(sl.to_list(), list)
        assert len(sl.to_list()) == 12

    def test_to_json(self, seasons_list_data):
        import json

        from pyapisports.football.models import TeamSeasonsList

        sl = TeamSeasonsList.from_api(seasons_list_data)
        parsed = json.loads(sl.to_json())
        assert 2020 in parsed


class TestTeamCountryList:
    def test_from_api(self, country_list_data):
        from pyapisports.football.models import TeamCountryList

        cl = TeamCountryList.from_api(country_list_data)
        assert len(cl.countries) == 3

    def test_iter(self, country_list_data):
        from pyapisports.football.models import Country, TeamCountryList

        cl = TeamCountryList.from_api(country_list_data)
        countries = list(cl)
        assert len(countries) == 3
        assert all(isinstance(c, Country) for c in countries)

    def test_len(self, country_list_data):
        from pyapisports.football.models import TeamCountryList

        cl = TeamCountryList.from_api(country_list_data)
        assert len(cl) == 3

    def test_contains(self, country_list_data):
        from pyapisports.football.models import Country, TeamCountryList

        cl = TeamCountryList.from_api(country_list_data)
        england = Country.from_api(country_list_data["response"][0])
        assert england in cl
        fake = Country.from_api({"name": "Fake", "code": "FK", "flag": None})
        assert fake not in cl

    def test_to_list(self, country_list_data):
        from pyapisports.football.models import TeamCountryList

        cl = TeamCountryList.from_api(country_list_data)
        result = cl.to_list()
        assert isinstance(result, list)
        assert len(result) == 3

    def test_to_json(self, country_list_data):
        import json

        from pyapisports.football.models import TeamCountryList

        cl = TeamCountryList.from_api(country_list_data)
        parsed = json.loads(cl.to_json())
        assert isinstance(parsed, list)
        assert len(parsed) == 3
