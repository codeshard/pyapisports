import json
from datetime import datetime

import pytest

from pyapisports.football.models.odds.odds import (
    Bet,
    Bookmaker,
    FixtureOdds,
    OddsList,
    OddValue,
)


@pytest.fixture
def odd_value_data():
    return {"value": "Home", "odd": "2.10", "handicap": None, "main": True, "suspended": False}


@pytest.fixture
def odd_value(odd_value_data) -> OddValue:
    return OddValue.from_api(odd_value_data)


@pytest.fixture
def suspended_odd_value() -> OddValue:
    return OddValue.from_api(
        {"value": "Away", "odd": "3.40", "handicap": "+1", "main": False, "suspended": True}
    )


@pytest.fixture
def bet_data():
    return {
        "id": 1,
        "name": "Match Winner",
        "values": [
            {"value": "Home", "odd": "2.10", "handicap": None, "main": True, "suspended": False},
            {"value": "Draw", "odd": "3.40", "handicap": None, "main": True, "suspended": False},
            {"value": "Away", "odd": "3.80", "handicap": None, "main": True, "suspended": False},
        ],
    }


@pytest.fixture
def bet(bet_data) -> Bet:
    return Bet.from_api(bet_data)


@pytest.fixture
def bookmaker_data():
    return {
        "id": 8,
        "name": "Bet365",
        "bets": [
            {
                "id": 1,
                "name": "Match Winner",
                "values": [
                    {"value": "Home", "odd": "2.10", "handicap": None, "main": True, "suspended": False},
                    {"value": "Draw", "odd": "3.40", "handicap": None, "main": True, "suspended": False},
                    {"value": "Away", "odd": "3.80", "handicap": None, "main": True, "suspended": False},
                ],
            },
            {
                "id": 2,
                "name": "Both Teams Score",
                "values": [
                    {"value": "Yes", "odd": "1.80", "handicap": None, "main": True, "suspended": False},
                    {"value": "No", "odd": "2.05", "handicap": None, "main": True, "suspended": False},
                ],
            },
        ],
    }


@pytest.fixture
def bookmaker(bookmaker_data) -> Bookmaker:
    return Bookmaker.from_api(bookmaker_data)


@pytest.fixture
def fixture_odds_data():
    return {
        "fixture": {"id": 215662},
        "league": {"id": 39, "name": "Premier League", "season": 2024},
        "update": "2024-12-01T10:00:00+00:00",
        "bookmakers": [
            {
                "id": 8,
                "name": "Bet365",
                "bets": [
                    {
                        "id": 1,
                        "name": "Match Winner",
                        "values": [
                            {"value": "Home", "odd": "2.10", "handicap": None, "main": True, "suspended": False},
                            {"value": "Draw", "odd": "3.40", "handicap": None, "main": True, "suspended": False},
                            {"value": "Away", "odd": "3.80", "handicap": None, "main": True, "suspended": False},
                        ],
                    },
                ],
            },
            {
                "id": 5,
                "name": "Betway",
                "bets": [
                    {
                        "id": 1,
                        "name": "Match Winner",
                        "values": [
                            {"value": "Home", "odd": "2.05", "handicap": None, "main": True, "suspended": False},
                            {"value": "Draw", "odd": "3.50", "handicap": None, "main": True, "suspended": False},
                            {"value": "Away", "odd": "3.90", "handicap": None, "main": True, "suspended": False},
                        ],
                    },
                ],
            },
            {
                "id": 3,
                "name": "WillHill",
                "bets": [
                    {
                        "id": 1,
                        "name": "Match Winner",
                        "values": [
                            {"value": "Home", "odd": "2.00", "handicap": None, "main": True, "suspended": True},
                            {"value": "Draw", "odd": "3.50", "handicap": None, "main": True, "suspended": False},
                            {"value": "Away", "odd": "4.00", "handicap": None, "main": True, "suspended": False},
                        ],
                    },
                ],
            },
        ],
    }


@pytest.fixture
def fixture_odds(fixture_odds_data) -> FixtureOdds:
    return FixtureOdds.from_api(fixture_odds_data)


@pytest.fixture
def odds_list_data(fixture_odds_data):
    return {"response": [fixture_odds_data]}


@pytest.fixture
def odds_list(odds_list_data) -> OddsList:
    return OddsList.from_api(odds_list_data)


# ── OddValue ───────────────────────────────────────────────


class TestOddValueFromApi:
    def test_value(self, odd_value):
        assert odd_value.value == "Home"

    def test_odd(self, odd_value):
        assert odd_value.odd == "2.10"

    def test_handicap_none(self, odd_value):
        assert odd_value.handicap is None

    def test_handicap_present(self, suspended_odd_value):
        assert suspended_odd_value.handicap == "+1"

    def test_main(self, odd_value):
        assert odd_value.main is True

    def test_suspended_false(self, odd_value):
        assert odd_value.suspended is False

    def test_suspended_true(self, suspended_odd_value):
        assert suspended_odd_value.suspended is True


class TestOddValueProperties:
    def test_odd_float(self, odd_value):
        assert odd_value.odd_float == 2.10

    def test_odd_float_invalid(self):
        ov = OddValue.from_api(
            {"value": "X", "odd": "N/A", "handicap": None, "main": None, "suspended": None}
        )
        assert ov.odd_float is None

    def test_odd_float_none_odd(self):
        ov = OddValue.from_api(
            {"value": "X", "odd": None, "handicap": None, "main": None, "suspended": None}
        )
        assert ov.odd_float is None

    def test_implied_probability(self, odd_value):
        assert odd_value.implied_probability == 47.62

    def test_implied_probability_zero_odd(self):
        ov = OddValue.from_api(
            {"value": "X", "odd": "0", "handicap": None, "main": None, "suspended": None}
        )
        assert ov.implied_probability is None

    def test_implied_probability_invalid_odd(self):
        ov = OddValue.from_api(
            {"value": "X", "odd": "N/A", "handicap": None, "main": None, "suspended": None}
        )
        assert ov.implied_probability is None

    def test_implied_probability_rounding(self):
        ov = OddValue.from_api(
            {"value": "X", "odd": "1.3333", "handicap": None, "main": None, "suspended": None}
        )
        assert ov.implied_probability == 75.0

    def test_is_suspended_true(self, suspended_odd_value):
        assert suspended_odd_value.is_suspended is True

    def test_is_suspended_false(self, odd_value):
        assert odd_value.is_suspended is False

    def test_is_suspended_none(self):
        ov = OddValue.from_api(
            {"value": "X", "odd": "2.0", "handicap": None, "main": None, "suspended": None}
        )
        assert ov.is_suspended is False


class TestOddValueToDict:
    def test_keys(self, odd_value):
        assert set(odd_value.to_dict().keys()) == {"value", "odd", "handicap", "main", "suspended"}

    def test_values(self, odd_value):
        d = odd_value.to_dict()
        assert d["value"] == "Home"
        assert d["odd"] == "2.10"
        assert d["handicap"] is None
        assert d["main"] is True
        assert d["suspended"] is False


# ── Bet ────────────────────────────────────────────────────


class TestBetFromApi:
    def test_id(self, bet):
        assert bet.id == 1

    def test_name(self, bet):
        assert bet.name == "Match Winner"

    def test_values_length(self, bet):
        assert len(bet.values) == 3

    def test_values_are_odd_value(self, bet):
        assert all(isinstance(v, OddValue) for v in bet.values)


class TestBetGet:
    def test_get_found(self, bet):
        ov = bet.get("Home")
        assert ov is not None
        assert ov.value == "Home"

    def test_get_case_insensitive(self, bet):
        assert bet.get("home") is not None

    def test_get_not_found(self, bet):
        assert bet.get("NonExistent") is None


class TestBetAvailable:
    def test_available_excludes_suspended(self, bet):
        bet.values.append(
            OddValue.from_api(
                {"value": "X", "odd": "5.0", "handicap": None, "main": False, "suspended": True}
            )
        )
        avail = bet.available
        assert all(not v.is_suspended for v in avail)

    def test_available_length(self, bet):
        assert len(bet.available) == 3


class TestBetBestValue:
    def test_best_value_highest_odd(self, bet):
        best = bet.best_value
        assert best is not None
        assert best.value == "Away"

    def test_best_value_all_suspended(self):
        b = Bet.from_api(
            {
                "id": 1,
                "name": "Test",
                "values": [
                    {"value": "A", "odd": "2.0", "handicap": None, "main": True, "suspended": True},
                    {"value": "B", "odd": "3.0", "handicap": None, "main": True, "suspended": True},
                ],
            }
        )
        assert b.best_value is None

    def test_best_value_empty(self):
        b = Bet(id=1, name="Empty")
        assert b.best_value is None


class TestBetToDict:
    def test_keys(self, bet):
        assert set(bet.to_dict().keys()) == {"id", "name", "values"}

    def test_values_serialized(self, bet):
        d = bet.to_dict()
        assert all(isinstance(v, dict) for v in d["values"])


# ── Bookmaker ──────────────────────────────────────────────


class TestBookmakerFromApi:
    def test_id(self, bookmaker):
        assert bookmaker.id == 8

    def test_name(self, bookmaker):
        assert bookmaker.name == "Bet365"

    def test_bets_length(self, bookmaker):
        assert len(bookmaker.bets) == 2

    def test_bets_are_bet(self, bookmaker):
        assert all(isinstance(b, Bet) for b in bookmaker.bets)


class TestBookmakerGetBet:
    def test_get_bet_by_id(self, bookmaker):
        b = bookmaker.get_bet(1)
        assert b is not None
        assert b.name == "Match Winner"

    def test_get_bet_by_id_not_found(self, bookmaker):
        assert bookmaker.get_bet(999) is None

    def test_get_bet_by_name(self, bookmaker):
        b = bookmaker.get_bet_by_name("Both Teams Score")
        assert b is not None
        assert b.id == 2

    def test_get_bet_by_name_case_insensitive(self, bookmaker):
        assert bookmaker.get_bet_by_name("both teams score") is not None

    def test_get_bet_by_name_not_found(self, bookmaker):
        assert bookmaker.get_bet_by_name("Over/Under") is None


class TestBookmakerToDict:
    def test_keys(self, bookmaker):
        assert set(bookmaker.to_dict().keys()) == {"id", "name", "bets"}

    def test_bets_serialized(self, bookmaker):
        d = bookmaker.to_dict()
        assert all(isinstance(b, dict) for b in d["bets"])


# ── FixtureOdds ────────────────────────────────────────────


class TestFixtureOddsFromApi:
    def test_fixture_id(self, fixture_odds):
        assert fixture_odds.fixture_id == 215662

    def test_league_id(self, fixture_odds):
        assert fixture_odds.league_id == 39

    def test_league_name(self, fixture_odds):
        assert fixture_odds.league_name == "Premier League"

    def test_league_season(self, fixture_odds):
        assert fixture_odds.league_season == 2024

    def test_update_is_datetime(self, fixture_odds):
        assert isinstance(fixture_odds.update, datetime)

    def test_bookmakers_length(self, fixture_odds):
        assert len(fixture_odds.bookmakers) == 3

    def test_bookmakers_are_bookmaker(self, fixture_odds):
        assert all(isinstance(b, Bookmaker) for b in fixture_odds.bookmakers)


class TestFixtureOddsGetBookmaker:
    def test_by_id(self, fixture_odds):
        bm = fixture_odds.get_bookmaker(8)
        assert bm is not None
        assert bm.name == "Bet365"

    def test_by_id_not_found(self, fixture_odds):
        assert fixture_odds.get_bookmaker(999) is None

    def test_by_name(self, fixture_odds):
        bm = fixture_odds.get_bookmaker_by_name("Betway")
        assert bm is not None
        assert bm.id == 5

    def test_by_name_case_insensitive(self, fixture_odds):
        assert fixture_odds.get_bookmaker_by_name("betway") is not None

    def test_by_name_not_found(self, fixture_odds):
        assert fixture_odds.get_bookmaker_by_name("Unibet") is None


class TestFixtureOddsBestOddFor:
    def test_best_odd_found(self, fixture_odds):
        best = fixture_odds.best_odd_for("Match Winner", "Home")
        assert best is not None
        assert best.odd == "2.10"
        assert best.value == "Home"

    def test_best_odd_skips_suspended(self, fixture_odds):
        # WillHill has Home at 2.00 but suspended; Bet365 at 2.10 should win
        best = fixture_odds.best_odd_for("Match Winner", "Home")
        assert best is not None
        assert best.odd == "2.10"

    def test_best_odd_not_found(self, fixture_odds):
        assert fixture_odds.best_odd_for("NonExistent", "Home") is None

    def test_best_odd_value_not_found(self, fixture_odds):
        assert fixture_odds.best_odd_for("Match Winner", "Nonsense") is None


class TestFixtureOddsCompareBookmakers:
    def test_returns_sorted_list(self, fixture_odds):
        result = fixture_odds.compare_bookmakers("Match Winner", "Home")
        # WillHill Home is suspended so it is excluded
        assert len(result) == 2
        assert float(result[0]["odd"]) >= float(result[1]["odd"])

    def test_excludes_suspended(self, fixture_odds):
        # WillHill Home is suspended, should not appear
        result = fixture_odds.compare_bookmakers("Match Winner", "Home")
        names = [r["bookmaker"] for r in result]
        assert "WillHill" not in names

    def test_includes_implied(self, fixture_odds):
        result = fixture_odds.compare_bookmakers("Match Winner", "Home")
        assert "implied" in result[0]

    def test_no_match(self, fixture_odds):
        assert fixture_odds.compare_bookmakers("NonExistent", "Home") == []


class TestFixtureOddsMarketSummary:
    def test_market_key(self, fixture_odds):
        summary = fixture_odds.market_summary("Match Winner")
        assert summary["market"] == "Match Winner"

    def test_outcomes_keys(self, fixture_odds):
        summary = fixture_odds.market_summary("Match Winner")
        assert "Home" in summary["outcomes"]
        assert "Draw" in summary["outcomes"]
        assert "Away" in summary["outcomes"]

    def test_best_odd_per_outcome(self, fixture_odds):
        summary = fixture_odds.market_summary("Match Winner")
        outcomes = summary["outcomes"]
        # Home: Bet365 2.10 vs Betway 2.05 vs WillHill 2.00(suspended) → 2.10
        assert outcomes["Home"]["best_odd"] == "2.10"
        assert outcomes["Home"]["bookmaker"] == "Bet365"
        # Away: Bet365 3.80 vs Betway 3.90 vs WillHill 4.00 → 4.00
        assert outcomes["Away"]["best_odd"] == "4.00"
        assert outcomes["Away"]["bookmaker"] == "WillHill"

    def test_outcome_implied(self, fixture_odds):
        summary = fixture_odds.market_summary("Match Winner")
        assert "implied" in summary["outcomes"]["Home"]


class TestFixtureOddsToDict:
    def test_keys(self, fixture_odds):
        d = fixture_odds.to_dict()
        assert "fixture" in d
        assert "league" in d
        assert "update" in d
        assert "bookmakers" in d

    def test_fixture_block(self, fixture_odds):
        assert fixture_odds.to_dict()["fixture"]["id"] == 215662

    def test_league_block(self, fixture_odds):
        d = fixture_odds.to_dict()["league"]
        assert d["id"] == 39
        assert d["name"] == "Premier League"
        assert d["season"] == 2024

    def test_update_is_iso_string(self, fixture_odds):
        assert isinstance(fixture_odds.to_dict()["update"], str)

    def test_bookmakers_serialized(self, fixture_odds):
        bms = fixture_odds.to_dict()["bookmakers"]
        assert all(isinstance(b, dict) for b in bms)


class TestFixtureOddsToJson:
    def test_valid_json(self, fixture_odds):
        parsed = json.loads(fixture_odds.to_json())
        assert isinstance(parsed, dict)

    def test_json_values(self, fixture_odds):
        parsed = json.loads(fixture_odds.to_json())
        assert parsed["fixture"]["id"] == 215662
        assert parsed["league"]["name"] == "Premier League"

    def test_json_indent(self, fixture_odds):
        result = fixture_odds.to_json(indent=2)
        assert "\n" in result


# ── OddsList ───────────────────────────────────────────────


class TestOddsListFromApi:
    def test_length(self, odds_list):
        assert len(odds_list) == 1

    def test_items_are_fixture_odds(self, odds_list):
        assert all(isinstance(o, FixtureOdds) for o in odds_list)

    def test_empty(self):
        ol = OddsList.from_api({"response": []})
        assert len(ol) == 0


class TestOddsListIteration:
    def test_iter(self, odds_list):
        items = list(odds_list)
        assert len(items) == 1

    def test_getitem(self, odds_list):
        assert odds_list[0].fixture_id == 215662


class TestOddsListFindByFixture:
    def test_found(self, odds_list):
        fo = odds_list.find_by_fixture(215662)
        assert fo is not None

    def test_not_found(self, odds_list):
        assert odds_list.find_by_fixture(9999) is None


class TestOddsListSerialization:
    def test_to_list(self, odds_list):
        result = odds_list.to_list()
        assert isinstance(result, list)
        assert all(isinstance(o, dict) for o in result)

    def test_to_list_length(self, odds_list):
        assert len(odds_list.to_list()) == 1

    def test_to_json_valid(self, odds_list):
        parsed = json.loads(odds_list.to_json())
        assert isinstance(parsed, list)
        assert len(parsed) == 1

    def test_to_json_indent(self, odds_list):
        assert "\n" in odds_list.to_json(indent=2)
