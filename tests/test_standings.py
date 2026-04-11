import json
from datetime import datetime

import pytest

from pyapisports.football.models import (
    StandingEntry,
    StandingRecord,
    Standings,
    StandingsTable,
)


@pytest.fixture
def standings(standings_payload) -> Standings:
    return Standings.from_api(standings_payload)


@pytest.fixture
def multi(standings_multi_payload) -> Standings:
    return Standings.from_api(standings_multi_payload)


@pytest.fixture
def table(standings) -> StandingsTable:
    return standings.table


@pytest.fixture
def city(table) -> StandingEntry:
    return table.find_by_rank(1)


@pytest.fixture
def sheffield(table) -> StandingEntry:
    return table.find_by_rank(20)


class TestStandingRecord:
    def test_from_api_fields(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        record = StandingRecord.from_api(raw_record["all"])
        assert record.played == 38
        assert record.win == 28
        assert record.draw == 7
        assert record.lose == 3
        assert record.goals_for == 96
        assert record.goals_against == 34

    def test_goal_difference(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        record = StandingRecord.from_api(raw_record["all"])
        assert record.goal_difference == 62

    def test_goal_difference_negative(self):
        record = StandingRecord.from_api(
            {
                "played": 38,
                "win": 3,
                "draw": 7,
                "lose": 28,
                "goals": {"for": 35, "against": 104},
            }
        )
        assert record.goal_difference == -69

    def test_to_dict(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        record = StandingRecord.from_api(raw_record["all"])
        d = record.to_dict()
        assert d["played"] == 38
        assert d["win"] == 28
        assert d["goals"]["for"] == 96
        assert d["goals"]["against"] == 34

    def test_to_dict_keys(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        record = StandingRecord.from_api(raw_record["all"])
        assert set(record.to_dict().keys()) == {
            "played",
            "win",
            "draw",
            "lose",
            "goals",
        }


class TestStandingEntryConstruction:
    def test_rank(self, city):
        assert city.rank == 1

    def test_team_id(self, city):
        assert city.team_id == 50

    def test_team_name(self, city):
        assert city.team_name == "Manchester City"

    def test_team_logo(self, city):
        assert (
            city.team_logo
            == "https://media.api-sports.io/football/teams/50.png"
        )

    def test_points(self, city):
        assert city.points == 91

    def test_goals_diff(self, city):
        assert city.goals_diff == 62

    def test_group(self, city):
        assert city.group == "Premier League"

    def test_form(self, city):
        assert city.form == "WWDWW"

    def test_status(self, city):
        assert city.status == "same"

    def test_description(self, city):
        assert city.description == "Promotion - Champions League (Group Stage)"

    def test_nullable_description(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        raw = json.loads(json.dumps(raw_record))
        raw["description"] = None
        entry = StandingEntry.from_api(raw)
        assert entry.description is None

    def test_nullable_form(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        raw = json.loads(json.dumps(raw_record))
        raw["form"] = None
        entry = StandingEntry.from_api(raw)
        assert entry.form is None

    def test_updated_is_datetime(self, city):
        assert isinstance(city.updated, datetime)

    def test_updated_value(self, city):
        assert city.updated.year == 2024
        assert city.updated.month == 5
        assert city.updated.day == 19

    def test_all_record_type(self, city):
        assert isinstance(city.all, StandingRecord)

    def test_home_record_type(self, city):
        assert isinstance(city.home, StandingRecord)

    def test_away_record_type(self, city):
        assert isinstance(city.away, StandingRecord)


class TestStandingEntryRecords:
    def test_all_record(self, city):
        assert city.all.played == 38
        assert city.all.win == 28
        assert city.all.goals_for == 96

    def test_home_record(self, city):
        assert city.home.played == 19
        assert city.home.win == 15
        assert city.home.goals_for == 56

    def test_away_record(self, city):
        assert city.away.played == 19
        assert city.away.win == 13
        assert city.away.goals_for == 40


class TestStandingEntryComputed:
    def test_played_shortcut(self, city):
        assert city.played == city.all.played

    def test_form_list(self, city):
        assert city.form_list == ["W", "W", "D", "W", "W"]

    def test_form_list_empty_when_none(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        raw = json.loads(json.dumps(raw_record))
        raw["form"] = None
        entry = StandingEntry.from_api(raw)
        assert entry.form_list == []

    def test_form_list_length(self, city):
        assert len(city.form_list) == 5

    def test_is_promoted_true(self, city):
        assert city.is_promoted is True

    def test_is_promoted_false(self, sheffield):
        assert sheffield.is_promoted is False

    def test_is_relegated_true(self, sheffield):
        assert sheffield.is_relegated is True

    def test_is_relegated_false(self, city):
        assert city.is_relegated is False

    def test_is_promoted_false_when_description_none(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][0]
        raw = json.loads(json.dumps(raw_record))
        raw["description"] = None
        entry = StandingEntry.from_api(raw)
        assert entry.is_promoted is False

    def test_is_relegated_false_when_description_none(self, standings_payload):
        raw_record = standings_payload["response"][0]["league"]["standings"][
            0
        ][5]
        raw = json.loads(json.dumps(raw_record))
        raw["description"] = None
        entry = StandingEntry.from_api(raw)
        assert entry.is_relegated is False

    def test_status_up(self, table):
        arsenal = table.find_by_team_name("Arsenal")
        assert arsenal.status == "up"

    def test_status_down(self, sheffield):
        assert sheffield.status == "down"


class TestStandingEntrySerialization:
    def test_to_dict_top_level_keys(self, city):
        assert set(city.to_dict().keys()) == {
            "rank",
            "team",
            "points",
            "goalsDiff",
            "group",
            "form",
            "status",
            "description",
            "all",
            "home",
            "away",
            "update",
        }

    def test_to_dict_team_block(self, city):
        t = city.to_dict()["team"]
        assert t["id"] == 50
        assert t["name"] == "Manchester City"

    def test_to_dict_values(self, city):
        d = city.to_dict()
        assert d["rank"] == 1
        assert d["points"] == 91
        assert d["goalsDiff"] == 62

    def test_to_dict_all_record(self, city):
        assert city.to_dict()["all"]["played"] == 38

    def test_to_json_valid(self, city):
        parsed = json.loads(city.to_json())
        assert isinstance(parsed, dict)
        assert parsed["rank"] == 1

    def test_to_json_indent(self, city):
        assert "\n" in city.to_json(indent=2)


class TestStandingsTableConstruction:
    def test_length(self, table):
        assert len(table) == 6

    def test_entries_are_standing_entry_instances(self, table):
        for entry in table:
            assert isinstance(entry, StandingEntry)

    def test_iterable(self, table):
        ranks = [e.rank for e in table]
        assert ranks[0] == 1
        assert ranks[-1] == 20

    def test_getitem(self, table):
        assert table[0].rank == 1

    def test_getitem_negative(self, table):
        assert table[-1].rank == 20


class TestStandingsTableFinders:
    def test_find_by_rank(self, table):
        entry = table.find_by_rank(1)
        assert entry.team_name == "Manchester City"

    def test_find_by_rank_not_found(self, table):
        assert table.find_by_rank(99) is None

    def test_find_by_team_id(self, table):
        entry = table.find_by_team_id(42)
        assert entry.team_name == "Arsenal"

    def test_find_by_team_id_not_found(self, table):
        assert table.find_by_team_id(9999) is None

    def test_find_by_team_name(self, table):
        entry = table.find_by_team_name("Arsenal")
        assert entry.rank == 2

    def test_find_by_team_name_case_insensitive(self, table):
        assert table.find_by_team_name("arsenal") == table.find_by_team_name(
            "Arsenal"
        )

    def test_find_by_team_name_not_found(self, table):
        assert table.find_by_team_name("Real Madrid") is None


class TestStandingsTableZones:
    def test_promoted_count(self, table):
        result = table.promoted()
        assert len(result) == 3

    def test_promoted_returns_standings_table(self, table):
        assert isinstance(table.promoted(), StandingsTable)

    def test_promoted_entries_have_description(self, table):
        for entry in table.promoted():
            assert entry.is_promoted

    def test_relegated_count(self, table):
        result = table.relegated()
        assert len(result) == 3

    def test_relegated_returns_standings_table(self, table):
        assert isinstance(table.relegated(), StandingsTable)

    def test_relegated_entries_are_correct(self, table):
        names = [e.team_name for e in table.relegated()]
        assert "Leeds United" in names
        assert "Sheffield Utd" in names
        assert "Brentford" in names

    def test_top_n(self, table):
        result = table.top(4)
        assert len(result) == 4
        assert result[0].rank == 1

    def test_top_returns_standings_table(self, table):
        assert isinstance(table.top(4), StandingsTable)

    def test_top_preserves_order(self, table):
        top4 = table.top(4)
        ranks = [e.rank for e in top4]
        assert ranks == sorted(ranks)


class TestStandingsTableSerialization:
    def test_to_list_returns_list_of_dicts(self, table):
        result = table.to_list()
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    def test_to_list_length(self, table):
        assert len(table.to_list()) == 6

    def test_to_list_first_entry(self, table):
        assert table.to_list()[0]["rank"] == 1
        assert table.to_list()[0]["team"]["id"] == 50

    def test_to_json_valid(self, table):
        parsed = json.loads(table.to_json())
        assert isinstance(parsed, list)
        assert len(parsed) == 6

    def test_to_json_indent(self, table):
        assert "\n" in table.to_json(indent=2)


class TestStandingsConstruction:
    def test_league_id(self, standings):
        assert standings.league_id == 39

    def test_league_name(self, standings):
        assert standings.league_name == "Premier League"

    def test_league_country(self, standings):
        assert standings.league_country == "England"

    def test_league_logo(self, standings):
        assert (
            standings.league_logo
            == "https://media.api-sports.io/football/leagues/39.png"
        )

    def test_league_flag(self, standings):
        assert (
            standings.league_flag == "https://media.api-sports.io/flags/gb.svg"
        )

    def test_league_flag_nullable(self, multi):
        assert multi.league_flag is None

    def test_league_season(self, standings):
        assert standings.league_season == 2024

    def test_tables_count_single(self, standings):
        assert len(standings.tables) == 1

    def test_tables_count_multi(self, multi):
        assert len(multi.tables) == 2

    def test_tables_are_standings_table_instances(self, standings):
        for t in standings.tables:
            assert isinstance(t, StandingsTable)


class TestStandingsComputed:
    def test_table_shortcut(self, standings):
        assert standings.table is standings.tables[0]

    def test_table_shortcut_length(self, standings):
        assert len(standings.table) == 6

    def test_is_multi_group_false(self, standings):
        assert standings.is_multi_group is False

    def test_is_multi_group_true(self, multi):
        assert multi.is_multi_group is True

    def test_multi_group_leaders(self, multi):
        leaders = [t.find_by_rank(1) for t in multi.tables]
        names = [e.team_name for e in leaders]
        assert "Manchester City" in names
        assert "Arsenal" in names


class TestStandingsSerialization:
    def test_to_dict_top_level_keys(self, standings):
        assert set(standings.to_dict().keys()) == {"league"}

    def test_to_dict_league_block(self, standings):
        league = standings.to_dict()["league"]
        assert league["id"] == 39
        assert league["name"] == "Premier League"
        assert league["season"] == 2024

    def test_to_dict_standings_is_list_of_lists(self, standings):
        tables = standings.to_dict()["league"]["standings"]
        assert isinstance(tables, list)
        assert isinstance(tables[0], list)

    def test_to_dict_first_entry(self, standings):
        first = standings.to_dict()["league"]["standings"][0][0]
        assert first["rank"] == 1
        assert first["points"] == 91

    def test_to_json_valid(self, standings):
        parsed = json.loads(standings.to_json())
        assert isinstance(parsed, dict)
        assert "league" in parsed

    def test_to_json_round_trips(self, standings):
        parsed = json.loads(standings.to_json())
        assert parsed["league"]["id"] == 39
        assert parsed["league"]["standings"][0][0]["team"]["id"] == 50

    def test_to_json_indent(self, standings):
        assert "\n" in standings.to_json(indent=2)

    def test_to_json_null_flag(self, multi):
        parsed = json.loads(multi.to_json())
        assert parsed["league"]["flag"] is None
