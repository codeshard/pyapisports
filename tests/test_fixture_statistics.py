import json
import pytest

from pyapisports.football.models.fixtures.statistics import (
    FixtureStatistics,
    StatEntry,
    StatType,
    TeamFixtureStatistics,
)


@pytest.fixture
def home_stats():
    return TeamFixtureStatistics.from_api({
        "team": {
            "id": 33,
            "name": "Manchester United",
            "logo": "https://media.api-sports.io/football/teams/33.png",
        },
        "statistics": [
            {"type": "Shots on Goal", "value": 8},
            {"type": "Shots off Goal", "value": 3},
            {"type": "Total Shots", "value": 11},
            {"type": "Blocked Shots", "value": 2},
            {"type": "Shots insidebox", "value": 9},
            {"type": "Shots outsidebox", "value": 2},
            {"type": "Fouls", "value": 12},
            {"type": "Corner Kicks", "value": 7},
            {"type": "Offsides", "value": 3},
            {"type": "Ball Possession", "value": "56%"},
            {"type": "Yellow Cards", "value": 2},
            {"type": "Red Cards", "value": 0},
            {"type": "Goalkeeper Saves", "value": 3},
            {"type": "Total passes", "value": 450},
            {"type": "Passes accurate", "value": 380},
            {"type": "Passes %", "value": "84%"},
            {"type": "expected_goals", "value": "1.89"},
        ],
    })


@pytest.fixture
def away_stats():
    return TeamFixtureStatistics.from_api({
        "team": {
            "id": 34,
            "name": "Tottenham Hotspur",
            "logo": "https://media.api-sports.io/football/teams/34.png",
        },
        "statistics": [
            {"type": "Shots on Goal", "value": 5},
            {"type": "Shots off Goal", "value": 2},
            {"type": "Total Shots", "value": 7},
            {"type": "Blocked Shots", "value": 1},
            {"type": "Shots insidebox", "value": 5},
            {"type": "Shots outsidebox", "value": 2},
            {"type": "Fouls", "value": 14},
            {"type": "Corner Kicks", "value": 3},
            {"type": "Offsides", "value": 1},
            {"type": "Ball Possession", "value": "44%"},
            {"type": "Yellow Cards", "value": 3},
            {"type": "Red Cards", "value": 0},
            {"type": "Goalkeeper Saves", "value": 2},
            {"type": "Total passes", "value": 352},
            {"type": "Passes accurate", "value": 291},
            {"type": "Passes %", "value": "83%"},
            {"type": "expected_goals", "value": "1.12"},
        ],
    })


@pytest.fixture
def fixture_stats(home_stats, away_stats):
    return FixtureStatistics(
        fixture_id=215662,
        home=home_stats,
        away=away_stats,
    )


class TestStatEntry:
    def test_from_api(self):
        entry = StatEntry.from_api({"type": "Shots on Goal", "value": 8})
        assert entry.type == "Shots on Goal"
        assert entry.value == 8

    def test_from_api_none_value(self):
        entry = StatEntry.from_api({"type": "Shots on Goal", "value": None})
        assert entry.value is None

    def test_int_value_int(self):
        entry = StatEntry(type="Shots", value=8)
        assert entry.int_value == 8

    def test_int_value_string(self):
        entry = StatEntry(type="Shots", value="8")
        assert entry.int_value == 8

    def test_int_value_percentage_string(self):
        entry = StatEntry(type="Possession", value="56%")
        assert entry.int_value == 56

    def test_int_value_invalid_string(self):
        entry = StatEntry(type="Name", value="abc")
        assert entry.int_value is None

    def test_int_value_unsupported_type(self):
        entry = StatEntry(type="Unknown", value=[1, 2])
        assert entry.int_value is None

    def test_int_value_none(self):
        entry = StatEntry(type="Shots", value=None)
        assert entry.int_value is None

    def test_float_value_float(self):
        entry = StatEntry(type="xG", value=1.5)
        assert entry.float_value == 1.5

    def test_float_value_string(self):
        entry = StatEntry(type="xG", value="1.89")
        assert entry.float_value == 1.89

    def test_float_value_percentage_string(self):
        entry = StatEntry(type="Possession", value="56%")
        assert entry.float_value == 56.0

    def test_float_value_invalid_string(self):
        entry = StatEntry(type="Name", value="abc")
        assert entry.float_value is None

    def test_float_value_unsupported_type(self):
        entry = StatEntry(type="Unknown", value=[1, 2])
        assert entry.float_value is None

    def test_float_value_none(self):
        entry = StatEntry(type="xG", value=None)
        assert entry.float_value is None

    def test_float_value_int(self):
        entry = StatEntry(type="xG", value=2)
        assert entry.float_value == 2.0

    def test_is_percentage_true(self):
        entry = StatEntry(type="Possession", value="56%")
        assert entry.is_percentage is True

    def test_is_percentage_false_int(self):
        entry = StatEntry(type="Shots", value=8)
        assert entry.is_percentage is False

    def test_is_percentage_false_string_no_percent(self):
        entry = StatEntry(type="Name", value="test")
        assert entry.is_percentage is False

    def test_is_percentage_none(self):
        entry = StatEntry(type="Shots", value=None)
        assert entry.is_percentage is False

    def test_to_dict(self):
        entry = StatEntry(type="Shots on Goal", value=8)
        assert entry.to_dict() == {"type": "Shots on Goal", "value": 8}


class TestTeamFixtureStatistics:
    def test_from_api(self, home_stats):
        assert home_stats.team_id == 33
        assert home_stats.team_name == "Manchester United"
        assert home_stats.team_logo == "https://media.api-sports.io/football/teams/33.png"
        assert len(home_stats.stats) == 17

    def test_get_returns_entry(self, home_stats):
        entry = home_stats.get(StatType.SHOTS_ON_GOAL)
        assert entry is not None
        assert entry.value == 8

    def test_get_returns_none_for_missing(self, home_stats):
        entry = home_stats.get("Unknown Stat")
        assert entry is None

    def test_value_of(self, home_stats):
        assert home_stats.value_of(StatType.SHOTS_ON_GOAL) == 8

    def test_value_of_none_for_missing(self, home_stats):
        assert home_stats.value_of("Unknown") is None

    def test_int_value_of(self, home_stats):
        assert home_stats.int_value_of(StatType.SHOTS_ON_GOAL) == 8

    def test_int_value_of_percentage(self, home_stats):
        assert home_stats.int_value_of(StatType.BALL_POSSESSION) == 56

    def test_int_value_of_none_for_missing(self, home_stats):
        assert home_stats.int_value_of("Unknown") is None

    def test_float_value_of(self, home_stats):
        assert home_stats.float_value_of(StatType.EXPECTED_GOALS) == 1.89

    def test_float_value_of_percentage(self, home_stats):
        assert home_stats.float_value_of(StatType.BALL_POSSESSION) == 56.0

    def test_float_value_of_none_for_missing(self, home_stats):
        assert home_stats.float_value_of("Unknown") is None

    def test_shots_on_goal_property(self, home_stats):
        assert home_stats.shots_on_goal == 8

    def test_shots_off_goal_property(self, home_stats):
        assert home_stats.shots_off_goal == 3

    def test_total_shots_property(self, home_stats):
        assert home_stats.total_shots == 11

    def test_blocked_shots_property(self, home_stats):
        assert home_stats.blocked_shots == 2

    def test_shots_inside_box_property(self, home_stats):
        assert home_stats.shots_inside_box == 9

    def test_shots_outside_box_property(self, home_stats):
        assert home_stats.shots_outside_box == 2

    def test_fouls_property(self, home_stats):
        assert home_stats.fouls == 12

    def test_corners_property(self, home_stats):
        assert home_stats.corners == 7

    def test_offsides_property(self, home_stats):
        assert home_stats.offsides == 3

    def test_ball_possession_property(self, home_stats):
        assert home_stats.ball_possession == 56

    def test_yellow_cards_property(self, home_stats):
        assert home_stats.yellow_cards == 2

    def test_red_cards_property(self, home_stats):
        assert home_stats.red_cards == 0

    def test_goalkeeper_saves_property(self, home_stats):
        assert home_stats.goalkeeper_saves == 3

    def test_total_passes_property(self, home_stats):
        assert home_stats.total_passes == 450

    def test_accurate_passes_property(self, home_stats):
        assert home_stats.accurate_passes == 380

    def test_pass_accuracy_property(self, home_stats):
        assert home_stats.pass_accuracy == 84

    def test_expected_goals_property(self, home_stats):
        assert home_stats.expected_goals == 1.89

    def test_to_dict_structure(self, home_stats):
        d = home_stats.to_dict()
        assert "team" in d
        assert "statistics" in d
        assert d["team"]["id"] == 33

    def test_to_json(self, home_stats):
        result = home_stats.to_json()
        parsed = json.loads(result)
        assert parsed["team"]["name"] == "Manchester United"


class TestFixtureStatistics:
    def test_from_api(self, fixture_stats):
        assert fixture_stats.fixture_id == 215662
        assert fixture_stats.home.team_id == 33
        assert fixture_stats.away.team_id == 34

    def test_compare(self, fixture_stats):
        result = fixture_stats.compare(StatType.SHOTS_ON_GOAL)
        assert result == {"type": "Shots on Goal", "home": 8, "away": 5}

    def test_summary(self, fixture_stats):
        result = fixture_stats.summary()
        assert result["fixture_id"] == 215662
        assert result["home_team"] == "Manchester United"
        assert result["away_team"] == "Tottenham Hotspur"
        assert "stats" in result

    def test_for_team_home(self, fixture_stats):
        result = fixture_stats.for_team(33)
        assert result is not None
        assert result.team_id == 33

    def test_for_team_away(self, fixture_stats):
        result = fixture_stats.for_team(34)
        assert result is not None
        assert result.team_id == 34

    def test_for_team_not_found(self, fixture_stats):
        result = fixture_stats.for_team(999)
        assert result is None

    def test_to_dict(self, fixture_stats):
        d = fixture_stats.to_dict()
        assert d["fixture_id"] == 215662
        assert "home" in d
        assert "away" in d

    def test_to_json(self, fixture_stats):
        result = fixture_stats.to_json()
        parsed = json.loads(result)
        assert parsed["fixture_id"] == 215662


class TestFixtureStatisticsFromApi:
    def test_from_api(self):
        data = {
            "response": [
                {
                    "team": {
                        "id": 33,
                        "name": "Manchester United",
                        "logo": "https://x.png",
                    },
                    "statistics": [{"type": "Shots on Goal", "value": 8}],
                },
                {
                    "team": {
                        "id": 34,
                        "name": "Tottenham",
                        "logo": "https://y.png",
                    },
                    "statistics": [{"type": "Shots on Goal", "value": 5}],
                },
            ],
        }
        result = FixtureStatistics.from_api(data, fixture_id=215662)
        assert result.fixture_id == 215662
        assert result.home.team_id == 33
        assert result.away.team_id == 34
