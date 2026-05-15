import json

import pytest

from pyapisports.football.models.fixtures.player_stats import (
    FixturePlayer,
    FixturePlayers,
    PlayerCards,
    PlayerDribbles,
    PlayerFouls,
    PlayerGames,
    PlayerGoals,
    PlayerMatchStats,
    PlayerPasses,
    PlayerPenalty,
    PlayerShots,
    PlayerTackles,
    TeamFixturePlayers,
)


# ---------------------------------------------------------------------------
#  Stat sub-objects
# ---------------------------------------------------------------------------

class TestPlayerGames:
    def test_from_api_none(self):
        g = PlayerGames.from_api(None)
        assert g.minutes is None
        assert g.number is None
        assert g.position is None
        assert g.rating is None
        assert g.captain is False
        assert g.substitute is False

    def test_from_api_missing_bool_fields(self):
        g = PlayerGames.from_api({"minutes": 90, "number": 9})
        assert g.minutes == 90
        assert g.captain is False
        assert g.substitute is False

    def test_from_api_full(self):
        g = PlayerGames.from_api({
            "minutes": 90, "number": 9, "position": "F",
            "rating": "9.2", "captain": True, "substitute": False,
        })
        assert g.minutes == 90
        assert g.number == 9
        assert g.position == "F"
        assert g.rating == "9.2"
        assert g.captain is True
        assert g.substitute is False

    def test_rating_float_valid(self):
        g = PlayerGames(minutes=90, number=9, position="F", rating="9.2", captain=False, substitute=False)
        assert g.rating_float == 9.2

    def test_rating_float_none(self):
        g = PlayerGames(minutes=0, number=0, position=None, rating=None, captain=False, substitute=False)
        assert g.rating_float is None

    def test_rating_float_invalid(self):
        g = PlayerGames(minutes=0, number=0, position=None, rating="N/A", captain=False, substitute=False)
        assert g.rating_float is None

    def test_to_dict(self):
        g = PlayerGames(minutes=90, number=9, position="F", rating="9.2", captain=True, substitute=False)
        assert g.to_dict() == {
            "minutes": 90, "number": 9, "position": "F",
            "rating": "9.2", "captain": True, "substitute": False,
        }


class TestPlayerShots:
    def test_from_api_none(self):
        s = PlayerShots.from_api(None)
        assert s.total is None
        assert s.on is None

    def test_from_api_full(self):
        s = PlayerShots.from_api({"total": 5, "on": 4})
        assert s.total == 5
        assert s.on == 4

    def test_to_dict(self):
        s = PlayerShots(total=5, on=4)
        assert s.to_dict() == {"total": 5, "on": 4}


class TestPlayerGoals:
    def test_from_api_none(self):
        g = PlayerGoals.from_api(None)
        assert g.total is None
        assert g.conceded is None
        assert g.assists is None
        assert g.saves is None

    def test_from_api_full(self):
        g = PlayerGoals.from_api({"total": 2, "conceded": 0, "assists": 1, "saves": 0})
        assert g.total == 2
        assert g.conceded == 0
        assert g.assists == 1
        assert g.saves == 0

    def test_to_dict(self):
        g = PlayerGoals(total=2, conceded=0, assists=1, saves=0)
        assert g.to_dict() == {"total": 2, "conceded": 0, "assists": 1, "saves": 0}


class TestPlayerPasses:
    def test_from_api_none(self):
        p = PlayerPasses.from_api(None)
        assert p.total is None
        assert p.key is None
        assert p.accuracy is None

    def test_from_api_full(self):
        p = PlayerPasses.from_api({"total": 42, "key": 1, "accuracy": "72%"})
        assert p.total == 42
        assert p.key == 1
        assert p.accuracy == "72%"

    def test_accuracy_int_valid(self):
        p = PlayerPasses(total=42, key=1, accuracy="72%")
        assert p.accuracy_int == 72

    def test_accuracy_int_none(self):
        p = PlayerPasses(total=0, key=0, accuracy=None)
        assert p.accuracy_int is None

    def test_accuracy_int_invalid(self):
        p = PlayerPasses(total=0, key=0, accuracy="abc")
        assert p.accuracy_int is None

    def test_to_dict(self):
        p = PlayerPasses(total=42, key=1, accuracy="72%")
        assert p.to_dict() == {"total": 42, "key": 1, "accuracy": "72%"}


class TestPlayerTackles:
    def test_from_api_none(self):
        t = PlayerTackles.from_api(None)
        assert t.total is None
        assert t.blocks is None
        assert t.interceptions is None

    def test_from_api_full(self):
        t = PlayerTackles.from_api({"total": 2, "blocks": 0, "interceptions": 1})
        assert t.total == 2
        assert t.blocks == 0
        assert t.interceptions == 1

    def test_to_dict(self):
        t = PlayerTackles(total=2, blocks=0, interceptions=1)
        assert t.to_dict() == {"total": 2, "blocks": 0, "interceptions": 1}


class TestPlayerDribbles:
    def test_from_api_none(self):
        d = PlayerDribbles.from_api(None)
        assert d.attempts is None
        assert d.success is None
        assert d.past is None

    def test_from_api_full(self):
        d = PlayerDribbles.from_api({"attempts": 6, "success": 3, "past": 0})
        assert d.attempts == 6
        assert d.success == 3
        assert d.past == 0

    def test_to_dict(self):
        d = PlayerDribbles(attempts=6, success=3, past=0)
        assert d.to_dict() == {"attempts": 6, "success": 3, "past": 0}


class TestPlayerFouls:
    def test_from_api_none(self):
        f = PlayerFouls.from_api(None)
        assert f.drawn is None
        assert f.committed is None

    def test_from_api_full(self):
        f = PlayerFouls.from_api({"drawn": 1, "committed": 0})
        assert f.drawn == 1
        assert f.committed == 0

    def test_to_dict(self):
        f = PlayerFouls(drawn=1, committed=0)
        assert f.to_dict() == {"drawn": 1, "committed": 0}


class TestPlayerCards:
    def test_from_api_none(self):
        c = PlayerCards.from_api(None)
        assert c.yellow is None
        assert c.red is None

    def test_from_api_full(self):
        c = PlayerCards.from_api({"yellow": 1, "red": 0})
        assert c.yellow == 1
        assert c.red == 0

    def test_to_dict(self):
        c = PlayerCards(yellow=1, red=0)
        assert c.to_dict() == {"yellow": 1, "red": 0}


class TestPlayerPenalty:
    def test_from_api_none(self):
        p = PlayerPenalty.from_api(None)
        assert p.won is None
        assert p.committed is None
        assert p.scored is None
        assert p.missed is None
        assert p.saved is None

    def test_from_api_full(self):
        p = PlayerPenalty.from_api({"won": 0, "commited": 0, "scored": 0, "missed": 0, "saved": 0})
        assert p.won == 0
        assert p.committed == 0
        assert p.scored == 0
        assert p.missed == 0
        assert p.saved == 0

    def test_to_dict(self):
        p = PlayerPenalty(won=0, committed=0, scored=0, missed=0, saved=0)
        assert p.to_dict() == {"won": 0, "commited": 0, "scored": 0, "missed": 0, "saved": 0}


# ---------------------------------------------------------------------------
#  PlayerMatchStats
# ---------------------------------------------------------------------------

class TestPlayerMatchStats:
    @pytest.fixture
    def stats_data(self):
        return [{
            "games": {"minutes": 90, "number": 9, "position": "F", "rating": "9.2", "captain": False, "substitute": False},
            "offsides": 1,
            "shots": {"total": 5, "on": 4},
            "goals": {"total": 2, "conceded": 0, "assists": 1, "saves": 0},
            "passes": {"total": 42, "key": 1, "accuracy": "72%"},
            "tackles": {"total": 0, "blocks": 0, "interceptions": 0},
            "dribbles": {"attempts": 6, "success": 3, "past": 0},
            "fouls": {"drawn": 1, "committed": 0},
            "cards": {"yellow": 0, "red": 0},
            "penalty": {"won": 0, "commited": 0, "scored": 0, "missed": 0, "saved": 0},
        }]

    def test_from_api_empty(self):
        stats = PlayerMatchStats.from_api([])
        assert stats.games.minutes is None
        assert stats.offsides is None
        assert stats.shots.total is None

    def test_from_api_full(self, stats_data):
        stats = PlayerMatchStats.from_api(stats_data)
        assert stats.games.minutes == 90
        assert stats.offsides == 1
        assert stats.shots.total == 5
        assert stats.goals.total == 2
        assert stats.passes.total == 42
        assert stats.tackles.total == 0
        assert stats.dribbles.attempts == 6

    @pytest.fixture
    def stats(self, stats_data):
        return PlayerMatchStats.from_api(stats_data)

    def test_rating(self, stats):
        assert stats.rating == 9.2

    def test_minutes_played(self, stats):
        assert stats.minutes_played == 90

    def test_is_captain(self, stats):
        assert stats.is_captain is False

    def test_is_substitute(self, stats):
        assert stats.is_substitute is False

    def test_to_dict(self, stats):
        d = stats.to_dict()
        assert d["games"]["minutes"] == 90
        assert d["offsides"] == 1
        assert d["shots"]["total"] == 5


# ---------------------------------------------------------------------------
#  FixturePlayer
# ---------------------------------------------------------------------------

class TestFixturePlayer:
    @pytest.fixture
    def haaland_data(self):
        return {
            "player": {"id": 35931, "name": "Erling Haaland", "photo": "https://x.com/photo.jpg"},
            "statistics": [{
                "games": {"minutes": 90, "number": 9, "position": "F", "rating": "9.2", "captain": False, "substitute": False},
                "offsides": 1,
                "shots": {"total": 5, "on": 4},
                "goals": {"total": 2, "conceded": 0, "assists": 1, "saves": 0},
                "passes": {"total": 42, "key": 1, "accuracy": "72%"},
                "tackles": {"total": 0, "blocks": 0, "interceptions": 0},
                "dribbles": {"attempts": 6, "success": 3, "past": 0},
                "fouls": {"drawn": 1, "committed": 0},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {"won": 0, "commited": 0, "scored": 0, "missed": 0, "saved": 0},
            }],
        }

    @pytest.fixture
    def player(self, haaland_data):
        return FixturePlayer.from_api(haaland_data)

    def test_from_api(self, player):
        assert player.id == 35931
        assert player.name == "Erling Haaland"
        assert player.photo == "https://x.com/photo.jpg"

    def test_rating(self, player):
        assert player.rating == 9.2

    def test_minutes_played(self, player):
        assert player.minutes_played == 90

    def test_position(self, player):
        assert player.position == "F"

    def test_is_captain(self, player):
        assert player.is_captain is False

    def test_is_substitute(self, player):
        assert player.is_substitute is False

    def test_goals(self, player):
        assert player.goals == 2

    def test_assists(self, player):
        assert player.assists == 1

    def test_to_dict(self, player):
        d = player.to_dict()
        assert d["player"]["id"] == 35931
        assert d["player"]["name"] == "Erling Haaland"
        assert len(d["statistics"]) == 1

    def test_to_json(self, player):
        parsed = json.loads(player.to_json())
        assert parsed["player"]["name"] == "Erling Haaland"
        assert parsed["statistics"][0]["goals"]["total"] == 2


# ---------------------------------------------------------------------------
#  TeamFixturePlayers
# ---------------------------------------------------------------------------

class TestTeamFixturePlayers:
    @pytest.fixture
    def team_data(self):
        return {
            "team": {"id": 2284, "name": "Manchester City", "logo": "https://x.com/logo.png"},
            "players": [
                {
                    "player": {"id": 35931, "name": "Erling Haaland", "photo": ""},
                    "statistics": [{
                        "games": {"minutes": 90, "number": 9, "position": "F", "rating": "9.2", "captain": False, "substitute": False},
                        "shots": {"total": 5, "on": 4}, "goals": {"total": 2}, "passes": {"total": 42},
                        "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
                    }],
                },
                {
                    "player": {"id": 112, "name": "Kevin De Bruyne", "photo": ""},
                    "statistics": [{
                        "games": {"minutes": 75, "number": 17, "position": "M", "rating": "8.5", "captain": True, "substitute": False},
                        "shots": {"total": 3, "on": 2}, "goals": {"total": 0}, "passes": {"total": 55},
                        "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
                    }],
                },
                {
                    "player": {"id": 337, "name": "Ederson", "photo": ""},
                    "statistics": [{
                        "games": {"minutes": 90, "number": 1, "position": "G", "rating": None, "captain": False, "substitute": False},
                        "shots": {"total": 0}, "goals": {"total": None, "conceded": 1, "saves": 3}, "passes": {"total": 28},
                        "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
                    }],
                },
            ],
        }

    @pytest.fixture
    def team(self, team_data):
        return TeamFixturePlayers.from_api(team_data)

    def test_from_api(self, team):
        assert team.team_id == 2284
        assert team.team_name == "Manchester City"
        assert team.team_logo == "https://x.com/logo.png"
        assert len(team.players) == 3

    def test_iter(self, team):
        names = [p.name for p in team]
        assert names == ["Erling Haaland", "Kevin De Bruyne", "Ederson"]

    def test_len(self, team):
        assert len(team) == 3

    def test_getitem(self, team):
        assert team[0].name == "Erling Haaland"

    def test_getitem_index_error(self, team):
        with pytest.raises(IndexError):
            team[100]

    def test_find_by_id_found(self, team):
        p = team.find_by_id(35931)
        assert p is not None
        assert p.name == "Erling Haaland"

    def test_find_by_id_not_found(self, team):
        assert team.find_by_id(99999) is None

    def test_find_by_name_found(self, team):
        p = team.find_by_name("Erling Haaland")
        assert p is not None
        assert p.id == 35931

    def test_find_by_name_case_insensitive(self, team):
        p = team.find_by_name("erling haaland")
        assert p is not None
        assert p.id == 35931

    def test_find_by_name_not_found(self, team):
        assert team.find_by_name("Nobody") is None

    def test_starters(self, team):
        starters = team.starters()
        assert len(starters) == 3

    def test_substitutes(self, team):
        team.players[1] = FixturePlayer(
            id=112, name="Sub", photo="",
            stats=PlayerMatchStats.from_api([{
                "games": {"minutes": 15, "number": 17, "position": "M", "rating": "6.0", "captain": False, "substitute": True},
                "shots": {}, "goals": {}, "passes": {}, "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
            }]),
        )
        subs = team.substitutes()
        assert len(subs) == 1
        assert subs[0].name == "Sub"

    def test_by_position(self, team):
        fwds = team.by_position("F")
        assert len(fwds) == 1
        assert fwds[0].name == "Erling Haaland"

    def test_sorted_by_rating_desc(self, team):
        rated = team.sorted_by_rating()
        assert rated[0].name == "Erling Haaland"
        assert rated[-1].name == "Kevin De Bruyne"

    def test_sorted_by_rating_asc(self, team):
        rated = team.sorted_by_rating(descending=False)
        assert rated[0].name == "Kevin De Bruyne"
        assert rated[-1].name == "Erling Haaland"

    def test_top_rated(self, team):
        p = team.top_rated
        assert p is not None
        assert p.name == "Erling Haaland"

    def test_top_rated_empty(self):
        t = TeamFixturePlayers(team_id=0, team_name="", team_logo="", players=[])
        assert t.top_rated is None

    def test_to_dict(self, team):
        d = team.to_dict()
        assert d["team"]["id"] == 2284
        assert d["team"]["name"] == "Manchester City"
        assert len(d["players"]) == 3

    def test_to_json(self, team):
        parsed = json.loads(team.to_json())
        assert parsed["team"]["name"] == "Manchester City"


# ---------------------------------------------------------------------------
#  FixturePlayers  (top-level)
# ---------------------------------------------------------------------------

class TestFixturePlayersFromApi:
    @pytest.fixture
    def home_player_data(self):
        return {
            "player": {"id": 35931, "name": "Haaland", "photo": ""},
            "statistics": [{
                "games": {"minutes": 90, "number": 9, "position": "F", "rating": "9.2", "captain": False, "substitute": False},
                "shots": {}, "goals": {"total": 2}, "passes": {}, "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
            }],
        }

    @pytest.fixture
    def away_player_data(self):
        return {
            "player": {"id": 111, "name": "Salah", "photo": ""},
            "statistics": [{
                "games": {"minutes": 90, "number": 11, "position": "F", "rating": "8.1", "captain": False, "substitute": False},
                "shots": {}, "goals": {"total": 0}, "passes": {}, "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
            }],
        }

    def test_from_api_two_teams(self, home_player_data, away_player_data):
        data = {
            "response": [
                {"team": {"id": 1, "name": "Home", "logo": ""}, "players": [home_player_data]},
                {"team": {"id": 2, "name": "Away", "logo": ""}, "players": [away_player_data]},
            ],
        }
        fp = FixturePlayers.from_api(data, fixture_id=100)
        assert fp.fixture_id == 100
        assert fp.home.team_id == 1
        assert fp.away.team_id == 2
        assert len(fp.home.players) == 1
        assert len(fp.away.players) == 1

    def test_from_api_one_team(self, home_player_data):
        data = {
            "response": [
                {"team": {"id": 1, "name": "Home", "logo": ""}, "players": [home_player_data]},
            ],
        }
        fp = FixturePlayers.from_api(data, fixture_id=100)
        assert fp.home.team_id == 1
        assert fp.away.team_id == 0
        assert fp.away.team_name == ""

    def test_from_api_empty_response(self):
        data = {"response": []}
        fp = FixturePlayers.from_api(data, fixture_id=100)
        assert fp.home.team_id == 0
        assert fp.away.team_id == 0
        assert len(fp.home.players) == 0
        assert len(fp.away.players) == 0


class TestFixturePlayersMethods:
    @pytest.fixture
    def players(self):
        home = TeamFixturePlayers(team_id=1, team_name="Home", team_logo="", players=[
            FixturePlayer(id=10, name="A", photo="", stats=PlayerMatchStats.from_api([{
                "games": {"minutes": 90, "number": 0, "position": "F", "rating": "8.0", "captain": False, "substitute": False},
                "shots": {}, "goals": {"total": 1}, "passes": {}, "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
            }])),
        ])
        away = TeamFixturePlayers(team_id=2, team_name="Away", team_logo="", players=[
            FixturePlayer(id=20, name="B", photo="", stats=PlayerMatchStats.from_api([{
                "games": {"minutes": 90, "number": 0, "position": "D", "rating": "7.0", "captain": False, "substitute": False},
                "shots": {}, "goals": {"total": 0}, "passes": {}, "tackles": {}, "dribbles": {}, "fouls": {}, "cards": {}, "penalty": {},
            }])),
        ])
        return FixturePlayers(fixture_id=100, home=home, away=away)

    def test_for_team_home(self, players):
        assert players.for_team(1).team_name == "Home"

    def test_for_team_away(self, players):
        assert players.for_team(2).team_name == "Away"

    def test_for_team_not_found(self, players):
        assert players.for_team(999) is None

    def test_find_player_found(self, players):
        result = players.find_player(10)
        assert result is not None
        team_block, player = result
        assert team_block.team_name == "Home"
        assert player.name == "A"

    def test_find_player_away(self, players):
        result = players.find_player(20)
        assert result is not None
        team_block, player = result
        assert team_block.team_name == "Away"
        assert player.name == "B"

    def test_find_player_not_found(self, players):
        assert players.find_player(999) is None

    def test_all_players(self, players):
        all_p = players.all_players()
        assert len(all_p) == 2
        assert all_p[0].name == "A"
        assert all_p[1].name == "B"

    def test_top_rated(self, players):
        top = players.top_rated()
        assert len(top) == 2
        assert top[0].name == "A"
        assert top[1].name == "B"

    def test_top_rated_n(self, players):
        top = players.top_rated(n=1)
        assert len(top) == 1
        assert top[0].name == "A"

    def test_top_rated_empty(self):
        fp = FixturePlayers(
            fixture_id=0,
            home=TeamFixturePlayers(team_id=0, team_name="", team_logo="", players=[]),
            away=TeamFixturePlayers(team_id=0, team_name="", team_logo="", players=[]),
        )
        assert fp.top_rated() == []

    def test_to_dict(self, players):
        d = players.to_dict()
        assert d["fixture_id"] == 100
        assert d["home"]["team"]["id"] == 1
        assert d["away"]["team"]["id"] == 2

    def test_to_json(self, players):
        parsed = json.loads(players.to_json())
        assert parsed["fixture_id"] == 100
        assert parsed["home"]["team"]["name"] == "Home"
