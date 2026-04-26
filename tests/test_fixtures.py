import json

import pytest

from pyapisports.football.models.fixtures.fixtures import (
    FixtureLeague,
    FixtureList,
    FixtureScore,
    FixtureStatus,
    FixtureTeam,
    PeriodScore,
)


class TestFixtureStatus:
    @pytest.fixture
    def status(self):
        return FixtureStatus.from_api(
            {
                "long": "Match Finished",
                "short": "FT",
                "elapsed": 90,
                "extra": None,
            }
        )

    def test_from_api(self, status):
        assert status.long == "Match Finished"
        assert status.short == "FT"
        assert status.elapsed == 90

    def test_from_api_without_elapsed(self):
        status = FixtureStatus.from_api(
            {"long": "Not Started", "short": "NS", "elapsed": None}
        )
        assert status.elapsed is None

    def test_is_live(self, status):
        assert not status.is_live

    def test_is_finished(self, status):
        assert status.is_finished is True

    def test_is_scheduled(self, status):
        assert status.is_scheduled is False

    def test_is_cancelled(self, status):
        assert status.is_cancelled is False

    @pytest.mark.parametrize(
        "short_code,expected",
        [
            ("1H", True),
            ("HT", True),
            ("2H", True),
            ("ET", True),
            ("BT", True),
            ("P", True),
            ("INT", True),
            ("LIVE", True),
        ],
    )
    def test_is_live_various_codes(self, short_code, expected):
        status = FixtureStatus.from_api(
            {"long": "Live", "short": short_code, "elapsed": 45}
        )
        assert status.is_live is expected

    def test_not_finished(self):
        status = FixtureStatus.from_api(
            {"long": "Not Started", "short": "NS", "elapsed": None}
        )
        assert status.is_finished is False

    def test_aet_finished(self):
        status = FixtureStatus.from_api(
            {
                "long": "Finished After Extra Time",
                "short": "AET",
                "elapsed": 120,
            }
        )
        assert status.is_finished is True

    def test_pen_finished(self):
        status = FixtureStatus.from_api(
            {
                "long": "Finished After Penalties",
                "short": "PEN",
                "elapsed": 120,
            }
        )
        assert status.is_finished is True

    def test_is_scheduled_ns(self):
        status = FixtureStatus.from_api(
            {"long": "Not Started", "short": "NS", "elapsed": None}
        )
        assert status.is_scheduled is True

    def test_is_cancelled_various_codes(self):
        for code in ["CANC", "ABD", "PST"]:
            status = FixtureStatus.from_api(
                {"long": "Cancelled", "short": code, "elapsed": None}
            )
            assert status.is_cancelled is True

    def test_to_dict(self, status):
        d = status.to_dict()
        assert d["long"] == "Match Finished"
        assert d["short"] == "FT"
        assert d["elapsed"] == 90


class TestFixtureLeague:
    @pytest.fixture
    def league(self):
        return FixtureLeague.from_api(
            {
                "id": 39,
                "name": "Premier League",
                "country": "England",
                "logo": "https://media.api-sports.io/football/leagues/39.png",
                "flag": "https://media.api-sports.io/flags/gb.svg",
                "season": 2024,
                "round": "Regular Season - 14",
            }
        )

    def test_from_api(self, league):
        assert league.id == 39
        assert league.name == "Premier League"

    def test_from_api_without_flag(self):
        league = FixtureLeague.from_api(
            {
                "id": 39,
                "name": "Premier League",
                "country": "England",
                "logo": "https://x.png",
                "flag": None,
                "season": 2024,
                "round": "1",
            }
        )
        assert league.flag is None

    def test_to_dict(self, league):
        d = league.to_dict()
        assert d["id"] == 39
        assert d["name"] == "Premier League"


class TestFixtureTeam:
    @pytest.fixture
    def team(self):
        return FixtureTeam.from_api(
            {
                "id": 33,
                "name": "Manchester United",
                "logo": "https://media.api-sports.io/football/teams/33.png",
                "winner": True,
            }
        )

    def test_from_api(self, team):
        assert team.id == 33
        assert team.winner is True

    def test_from_api_without_winner(self):
        team = FixtureTeam.from_api(
            {"id": 33, "name": "Man Utd", "logo": "https://x.png"}
        )
        assert team.winner is None

    def test_to_dict(self, team):
        d = team.to_dict()
        assert d["id"] == 33
        assert d["winner"] is True


class TestPeriodScore:
    def test_from_api_with_data(self):
        score = PeriodScore.from_api({"home": 2, "away": 1})
        assert score.home == 2
        assert score.away == 1

    def test_from_api_none(self):
        score = PeriodScore.from_api(None)
        assert score.home is None
        assert score.away is None

    def test_to_dict(self):
        score = PeriodScore.from_api({"home": 2, "away": 1})
        d = score.to_dict()
        assert d == {"home": 2, "away": 1}

    def test_from_api_partial(self):
        score = PeriodScore.from_api({"home": 1})
        assert score.home == 1
        assert score.away is None


class TestFixtureScore:
    @pytest.fixture
    def score(self):
        return FixtureScore.from_api(
            {
                "halftime": {"home": 1, "away": 0},
                "fulltime": {"home": 2, "away": 1},
                "extratime": {"home": None, "away": None},
                "penalty": {"home": None, "away": None},
            }
        )

    def test_from_api(self, score):
        assert score.halftime.home == 1
        assert score.fulltime.away == 1

    def test_to_dict(self, score):
        d = score.to_dict()
        assert d["halftime"]["home"] == 1
        assert d["fulltime"]["away"] == 1


class TestFixture:
    @pytest.fixture
    def fixture(self, fixture_payload):
        return FixtureList.from_api(fixture_payload)[0]

    @pytest.fixture
    def live_fixture(self, live_fixture_payload):
        return FixtureList.from_api(live_fixture_payload)[0]

    @pytest.fixture
    def scheduled_fixture(self, scheduled_fixture_payload):
        return FixtureList.from_api(scheduled_fixture_payload)[0]

    @pytest.fixture
    def cancelled_fixture(self, cancelled_fixture_payload):
        return FixtureList.from_api(cancelled_fixture_payload)[0]

    def test_from_api(self, fixture):
        assert fixture.id == 868078
        assert fixture.referee == "Anthony Taylor"

    def test_referee_none(self, scheduled_fixture):
        assert scheduled_fixture.referee is None

    def test_is_live(self, fixture, live_fixture):
        assert not fixture.is_live
        assert live_fixture.is_live is True

    def test_is_finished(self, fixture):
        assert fixture.is_finished is True

    def test_is_scheduled(self, fixture, scheduled_fixture):
        assert not fixture.is_scheduled
        assert scheduled_fixture.is_scheduled is True

    def test_is_cancelled(self, fixture, cancelled_fixture):
        assert not fixture.is_cancelled
        assert cancelled_fixture.is_cancelled is True

    def test_score_str(self, fixture):
        assert fixture.score_str == "2 - 1"

    def test_score_str_with_none(self, scheduled_fixture):
        assert scheduled_fixture.score_str == "? - ?"

    def test_winner_home(self, fixture):
        assert fixture.winner is not None
        assert fixture.winner.id == 33

    def test_winner_away(self, fixture_payload):
        payload = {
            "response": [
                {
                    "fixture": {
                        "id": 1,
                        "referee": None,
                        "timezone": "UTC",
                        "date": "2024-12-01T15:00:00+00:00",
                        "timestamp": 1,
                        "venue": {"id": 1, "name": "X", "city": "Y"},
                        "status": {"long": "FT", "short": "FT", "elapsed": 90},
                    },
                    "league": {
                        "id": 1,
                        "name": "L",
                        "country": "X",
                        "logo": "x",
                        "season": 2024,
                        "round": "1",
                    },
                    "teams": {
                        "home": {
                            "id": 1,
                            "name": "A",
                            "logo": "x",
                            "winner": False,
                        },
                        "away": {
                            "id": 2,
                            "name": "B",
                            "logo": "y",
                            "winner": True,
                        },
                    },
                    "goals": {"home": 1, "away": 2},
                    "score": {},
                }
            ]
        }
        f = FixtureList.from_api(payload)[0]
        assert f.winner is not None
        assert f.winner.id == 2

    def test_winner_none(self, scheduled_fixture):
        assert scheduled_fixture.winner is None

    def test_to_dict(self, fixture):
        d = fixture.to_dict()
        assert d["fixture"]["id"] == 868078
        assert d["goals"]["home"] == 2

    def test_to_json(self, fixture):
        j = fixture.to_json()
        parsed = json.loads(j)
        assert parsed["fixture"]["id"] == 868078


class TestFixtureList:
    @pytest.fixture
    def fixture_list(
        self, fixture_payload, live_fixture_payload, scheduled_fixture_payload
    ):
        all_fixtures = {
            "response": [
                *fixture_payload["response"],
                *live_fixture_payload["response"],
                *scheduled_fixture_payload["response"],
            ]
        }
        return FixtureList.from_api(all_fixtures)

    def test_from_api(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        assert len(fl) == 1

    def test_iter(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        count = 0
        for f in fl:
            count += 1
        assert count == 1

    def test_getitem(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        assert fl[0].id == 868078

    def test_find_by_id(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        f = fl.find_by_id(868078)
        assert f is not None
        assert f.id == 868078

    def test_find_by_id_not_found(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        f = fl.find_by_id(999999)
        assert f is None

    def test_live(self, fixture_list):
        live = fixture_list.live()
        assert len(live) == 1

    def test_finished(self, fixture_list):
        finished = fixture_list.finished()
        assert len(finished) == 1

    def test_scheduled(self, fixture_list):
        scheduled = fixture_list.scheduled()
        assert len(scheduled) == 1

    def test_by_team(self, fixture_list):
        by_team = fixture_list.by_team(33)
        assert len(by_team) == 3

    def test_by_round(self, fixture_list):
        by_round = fixture_list.by_round("Regular Season - 14")
        assert len(by_round) == 2

    def test_to_list(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        lst = fl.to_list()
        assert len(lst) == 1
        assert lst[0]["fixture"]["id"] == 868078

    def test_to_json(self, fixture_payload):
        fl = FixtureList.from_api(fixture_payload)
        j = fl.to_json()
        parsed = json.loads(j)
        assert len(parsed) == 1
