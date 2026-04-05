import json

import pytest

from pyapisports.football.models import (
    Biggest,
    BiggestScoreline,
    CardStats,
    CleanSheet,
    FixturesStats,
    GoalMinuteBreakdown,
    GoalMinuteSlot,
    GoalsStats,
    HomeAwayTotal,
    HomeAwayTotalStr,
    LineupEntry,
    PenaltyStat,
    PenaltyStats,
    TeamStatistics,
)


@pytest.fixture
def stats(teams_statistics_payload) -> TeamStatistics:
    return TeamStatistics.from_api(teams_statistics_payload)


class TestHomeAwayTotal:
    def test_from_api(self):
        obj = HomeAwayTotal.from_api({"home": 10, "away": 7, "total": 17})
        assert obj.home == 10
        assert obj.away == 7
        assert obj.total == 17

    def test_from_api_none_input(self):
        obj = HomeAwayTotal.from_api(None)
        assert obj.home is None
        assert obj.away is None
        assert obj.total is None

    def test_from_api_partial_nulls(self):
        obj = HomeAwayTotal.from_api({"home": 4, "away": None, "total": None})
        assert obj.home == 4
        assert obj.away is None

    def test_to_dict(self):
        obj = HomeAwayTotal.from_api({"home": 10, "away": 7, "total": 17})
        assert obj.to_dict() == {"home": 10, "away": 7, "total": 17}


class TestHomeAwayTotalStr:
    def test_from_api(self):
        obj = HomeAwayTotalStr.from_api(
            {"home": "1.6", "away": "1.2", "total": "1.4"}
        )
        assert obj.home == "1.6"
        assert obj.away == "1.2"
        assert obj.total == "1.4"

    def test_from_api_none_input(self):
        obj = HomeAwayTotalStr.from_api(None)
        assert obj.home is None
        assert obj.away is None
        assert obj.total is None

    def test_to_dict(self):
        obj = HomeAwayTotalStr.from_api(
            {"home": "1.6", "away": "1.2", "total": "1.4"}
        )
        assert obj.to_dict() == {"home": "1.6", "away": "1.2", "total": "1.4"}


class TestGoalMinuteSlot:
    def test_from_api(self):
        slot = GoalMinuteSlot.from_api({"total": 5, "percentage": "9.6%"})
        assert slot.total == 5
        assert slot.percentage == "9.6%"

    def test_from_api_none(self):
        slot = GoalMinuteSlot.from_api(None)
        assert slot.total is None
        assert slot.percentage is None

    def test_to_dict(self):
        slot = GoalMinuteSlot.from_api({"total": 5, "percentage": "9.6%"})
        assert slot.to_dict() == {"total": 5, "percentage": "9.6%"}


class TestGoalMinuteBreakdown:
    @pytest.fixture
    def breakdown(self, teams_statistics_payload):
        return GoalMinuteBreakdown.from_api(
            teams_statistics_payload["response"]["goals"]["for"]["minute"]
        )

    def test_all_slots_present(self, breakdown):
        assert breakdown.slot_0_15.total == 5
        assert breakdown.slot_16_30.total == 8
        assert breakdown.slot_31_45.total == 7
        assert breakdown.slot_46_60.total == 10
        assert breakdown.slot_61_75.total == 9
        assert breakdown.slot_76_90.total == 8
        assert breakdown.slot_91_105.total == 4
        assert breakdown.slot_106_120.total == 1

    def test_percentage_values(self, breakdown):
        assert breakdown.slot_0_15.percentage == "9.6%"
        assert breakdown.slot_106_120.percentage == "1.9%"

    def test_to_dict_keys(self, breakdown):
        d = breakdown.to_dict()
        assert set(d.keys()) == {
            "0-15",
            "16-30",
            "31-45",
            "46-60",
            "61-75",
            "76-90",
            "91-105",
            "106-120",
        }

    def test_to_dict_values(self, breakdown):
        d = breakdown.to_dict()
        assert d["0-15"] == {"total": 5, "percentage": "9.6%"}


class TestFixturesStats:
    @pytest.fixture
    def fixtures(self, teams_statistics_payload):
        return FixturesStats.from_api(
            teams_statistics_payload["response"]["fixtures"]
        )

    def test_played(self, fixtures):
        assert fixtures.played.home == 19
        assert fixtures.played.away == 19
        assert fixtures.played.total == 38

    def test_wins(self, fixtures):
        assert fixtures.wins.home == 10
        assert fixtures.wins.away == 7
        assert fixtures.wins.total == 17

    def test_draws(self, fixtures):
        assert fixtures.draws.total == 9

    def test_loses(self, fixtures):
        assert fixtures.loses.total == 12

    def test_to_dict_structure(self, fixtures):
        d = fixtures.to_dict()
        assert set(d.keys()) == {"played", "wins", "draws", "loses"}
        assert d["played"] == {"home": 19, "away": 19, "total": 38}


class TestGoalsStats:
    @pytest.fixture
    def goals(self, teams_statistics_payload):
        r = teams_statistics_payload["response"]
        return GoalsStats.from_api(r["goals"], r.get("average", {}))

    def test_scored_totals(self, goals):
        assert goals.scored.home == 30
        assert goals.scored.away == 22
        assert goals.scored.total == 52

    def test_conceded_totals(self, goals):
        assert goals.conceded.home == 20
        assert goals.conceded.away == 28
        assert goals.conceded.total == 48

    def test_average_scored(self, goals):
        assert goals.average_scored.home == "1.6"
        assert goals.average_scored.total == "1.4"

    def test_average_conceded(self, goals):
        assert goals.average_conceded.away == "1.5"

    def test_minute_breakdown_type(self, goals):
        assert isinstance(goals.minute_breakdown, GoalMinuteBreakdown)

    def test_minute_breakdown_values(self, goals):
        assert goals.minute_breakdown.slot_46_60.total == 10

    def test_to_dict_keys(self, goals):
        d = goals.to_dict()
        assert set(d.keys()) == {
            "scored",
            "conceded",
            "average_scored",
            "average_conceded",
            "minute_breakdown",
        }


class TestBiggestScoreline:
    def test_from_api(self):
        s = BiggestScoreline.from_api({"home": "4-0", "away": "3-0"})
        assert s.home == "4-0"
        assert s.away == "3-0"

    def test_from_api_none(self):
        s = BiggestScoreline.from_api(None)
        assert s.home is None
        assert s.away is None

    def test_to_dict(self):
        s = BiggestScoreline.from_api({"home": "4-0", "away": "3-0"})
        assert s.to_dict() == {"home": "4-0", "away": "3-0"}


class TestBiggest:
    @pytest.fixture
    def biggest(self, teams_statistics_payload):
        return Biggest.from_api(
            teams_statistics_payload["response"]["biggest"]
        )

    def test_streaks(self, biggest):
        assert biggest.streak_wins == 4
        assert biggest.streak_draws == 2
        assert biggest.streak_loses == 3

    def test_wins_scoreline(self, biggest):
        assert biggest.wins.home == "4-0"
        assert biggest.wins.away == "3-0"

    def test_loses_scoreline(self, biggest):
        assert biggest.loses.home == "1-3"
        assert biggest.loses.away == "0-4"

    def test_goals_scored(self, biggest):
        assert biggest.goals_scored.home == 4
        assert biggest.goals_scored.away == 3
        assert biggest.goals_scored.total is None

    def test_goals_conceded(self, biggest):
        assert biggest.goals_conceded.home == 3
        assert biggest.goals_conceded.away == 4

    def test_to_dict_structure(self, biggest):
        d = biggest.to_dict()
        assert d["streak"] == {"wins": 4, "draws": 2, "loses": 3}
        assert d["wins"] == {"home": "4-0", "away": "3-0"}
        assert d["loses"] == {"home": "1-3", "away": "0-4"}


class TestCleanSheet:
    def test_clean_sheet_values(self, stats):
        assert stats.clean_sheet.home == 8
        assert stats.clean_sheet.away == 5
        assert stats.clean_sheet.total == 13

    def test_failed_to_score_values(self, stats):
        assert stats.failed_to_score.home == 3
        assert stats.failed_to_score.away == 6
        assert stats.failed_to_score.total == 9

    def test_from_api_none(self):
        obj = CleanSheet.from_api(None)
        assert obj.home is None
        assert obj.away is None
        assert obj.total is None

    def test_to_dict(self, stats):
        assert stats.clean_sheet.to_dict() == {
            "home": 8,
            "away": 5,
            "total": 13,
        }


class TestPenaltyStats:
    @pytest.fixture
    def penalty(self, teams_statistics_payload):
        return PenaltyStats.from_api(
            teams_statistics_payload["response"]["penalty"]
        )

    def test_total(self, penalty):
        assert penalty.total == 8

    def test_scored(self, penalty):
        assert penalty.scored.total == 7
        assert penalty.scored.percentage == "87.5%"

    def test_missed(self, penalty):
        assert penalty.missed.total == 1
        assert penalty.missed.percentage == "12.5%"

    def test_penalty_stat_none_input(self):
        stat = PenaltyStat.from_api(None)
        assert stat.total is None
        assert stat.percentage is None

    def test_to_dict(self, penalty):
        d = penalty.to_dict()
        assert d["total"] == 8
        assert d["scored"] == {"total": 7, "percentage": "87.5%"}
        assert d["missed"] == {"total": 1, "percentage": "12.5%"}


class TestLineupEntry:
    def test_from_api(self):
        entry = LineupEntry.from_api({"formation": "4-2-3-1", "played": 22})
        assert entry.formation == "4-2-3-1"
        assert entry.played == 22

    def test_to_dict(self):
        entry = LineupEntry.from_api({"formation": "4-3-3", "played": 10})
        assert entry.to_dict() == {"formation": "4-3-3", "played": 10}


class TestCardStats:
    @pytest.fixture
    def cards(self, teams_statistics_payload):
        return CardStats.from_api(
            teams_statistics_payload["response"]["cards"]
        )

    def test_yellow_breakdown_type(self, cards):
        assert isinstance(cards.yellow, GoalMinuteBreakdown)

    def test_red_breakdown_type(self, cards):
        assert isinstance(cards.red, GoalMinuteBreakdown)

    def test_yellow_peak_slot(self, cards):
        assert cards.yellow.slot_76_90.total == 10
        assert cards.yellow.slot_76_90.percentage == "22.7%"

    def test_yellow_zero_slot(self, cards):
        assert cards.yellow.slot_106_120.total == 0

    def test_red_cards(self, cards):
        assert cards.red.slot_31_45.total == 1
        assert cards.red.slot_61_75.total == 1
        assert cards.red.slot_76_90.total == 1
        assert cards.red.slot_0_15.total == 0

    def test_to_dict_keys(self, cards):
        d = cards.to_dict()
        assert set(d.keys()) == {"yellow", "red"}


class TestTeamStatisticsConstruction:
    def test_league_fields(self, stats):
        assert stats.league_id == 39
        assert stats.league_name == "Premier League"
        assert stats.league_country == "England"
        assert (
            stats.league_logo
            == "https://media.api-sports.io/football/leagues/39.png"
        )
        assert stats.league_flag == "https://media.api-sports.io/flags/gb.svg"
        assert stats.league_season == 2024

    def test_team_fields(self, stats):
        assert stats.team_id == 33
        assert stats.team_name == "Manchester United"
        assert (
            stats.team_logo
            == "https://media.api-sports.io/football/teams/33.png"
        )

    def test_form_string(self, stats):
        assert stats.form == "WDLWW"

    def test_nullable_flag(self, teams_statistics_payload):
        payload = json.loads(json.dumps(teams_statistics_payload))  # deep copy
        del payload["response"]["league"]["flag"]
        s = TeamStatistics.from_api(payload)
        assert s.league_flag is None

    def test_nested_types(self, stats):
        assert isinstance(stats.fixtures, FixturesStats)
        assert isinstance(stats.goals, GoalsStats)
        assert isinstance(stats.biggest, Biggest)
        assert isinstance(stats.clean_sheet, CleanSheet)
        assert isinstance(stats.failed_to_score, CleanSheet)
        assert isinstance(stats.penalty, PenaltyStats)
        assert isinstance(stats.cards, CardStats)

    def test_lineups_count(self, stats):
        assert len(stats.lineups) == 3

    def test_lineups_types(self, stats):
        for entry in stats.lineups:
            assert isinstance(entry, LineupEntry)

    def test_empty_lineups(self, teams_statistics_payload):
        payload = json.loads(json.dumps(teams_statistics_payload))
        payload["response"]["lineups"] = []
        s = TeamStatistics.from_api(payload)
        assert s.lineups == []


class TestTeamStatisticsComputedProperties:
    def test_win_rate(self, stats):
        assert stats.win_rate == 44.7

    def test_win_rate_zero_played(self, teams_statistics_payload):
        payload = json.loads(json.dumps(teams_statistics_payload))
        payload["response"]["fixtures"]["played"] = {
            "home": 0,
            "away": 0,
            "total": 0,
        }
        s = TeamStatistics.from_api(payload)
        assert s.win_rate is None

    def test_win_rate_none_played(self, teams_statistics_payload):
        payload = json.loads(json.dumps(teams_statistics_payload))
        payload["response"]["fixtures"]["played"] = {
            "home": None,
            "away": None,
            "total": None,
        }
        s = TeamStatistics.from_api(payload)
        assert s.win_rate is None

    def test_most_used_formation(self, stats):
        assert stats.most_used_formation == "4-2-3-1"

    def test_most_used_formation_empty_lineups(self, teams_statistics_payload):
        payload = json.loads(json.dumps(teams_statistics_payload))
        payload["response"]["lineups"] = []
        s = TeamStatistics.from_api(payload)
        assert s.most_used_formation is None

    def test_current_form_list(self, stats):
        assert stats.current_form == ["W", "D", "L", "W", "W"]

    def test_current_form_none(self, teams_statistics_payload):
        payload = json.loads(json.dumps(teams_statistics_payload))
        payload["response"]["form"] = None
        s = TeamStatistics.from_api(payload)
        assert s.current_form == []

    def test_current_form_length(self, stats):
        assert len(stats.current_form) == 5


class TestTeamStatisticsSerialization:
    def test_to_dict_top_level_keys(self, stats):
        d = stats.to_dict()
        assert set(d.keys()) == {
            "league",
            "team",
            "form",
            "fixtures",
            "goals",
            "biggest",
            "clean_sheet",
            "failed_to_score",
            "penalty",
            "lineups",
            "cards",
        }

    def test_to_dict_league_block(self, stats):
        d = stats.to_dict()
        assert d["league"]["id"] == 39
        assert d["league"]["name"] == "Premier League"
        assert d["league"]["season"] == 2024

    def test_to_dict_team_block(self, stats):
        d = stats.to_dict()
        assert d["team"]["id"] == 33
        assert d["team"]["name"] == "Manchester United"

    def test_to_dict_form(self, stats):
        assert stats.to_dict()["form"] == "WDLWW"

    def test_to_dict_lineups(self, stats):
        lineups = stats.to_dict()["lineups"]
        assert len(lineups) == 3
        assert lineups[0] == {"formation": "4-2-3-1", "played": 22}

    def test_to_json_is_valid(self, stats):
        result = json.loads(stats.to_json())
        assert isinstance(result, dict)

    def test_to_json_indent(self, stats):
        result = stats.to_json(indent=2)
        assert "\n" in result

    def test_to_json_round_trips(self, stats):
        parsed = json.loads(stats.to_json())
        assert parsed["team"]["id"] == 33
        assert parsed["fixtures"]["played"]["total"] == 38
        assert parsed["penalty"]["scored"]["percentage"] == "87.5%"
        assert parsed["lineups"][0]["formation"] == "4-2-3-1"
