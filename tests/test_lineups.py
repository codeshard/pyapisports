import json

import pytest

from pyapisports.football.models.fixtures.lineups import (
    Coach,
    FixtureLineups,
    KitColors,
    LineupPlayer,
    Position,
    TeamColors,
    TeamLineup,
)


# ---------------------------------------------------------------------------
#  KitColors
# ---------------------------------------------------------------------------

class TestKitColors:
    def test_from_api_none(self):
        k = KitColors.from_api(None)
        assert k.primary is None
        assert k.number is None
        assert k.border is None

    def test_from_api_full(self):
        k = KitColors.from_api({"primary": "#FF0000", "number": "#FFF", "border": "#000"})
        assert k.primary == "#FF0000"
        assert k.number == "#FFF"
        assert k.border == "#000"

    def test_to_dict(self):
        k = KitColors(primary="#FF0000", number="#FFF", border="#000")
        assert k.to_dict() == {"primary": "#FF0000", "number": "#FFF", "border": "#000"}


# ---------------------------------------------------------------------------
#  TeamColors
# ---------------------------------------------------------------------------

class TestTeamColors:
    def test_from_api_none(self):
        t = TeamColors.from_api(None)
        assert t.player.primary is None
        assert t.goalkeeper.primary is None

    def test_from_api_full(self):
        t = TeamColors.from_api({
            "player": {"primary": "#FF0000", "number": "#FFF", "border": "#000"},
            "goalkeeper": {"primary": "#00FF00", "number": "#000", "border": "#FFF"},
        })
        assert t.player.primary == "#FF0000"
        assert t.goalkeeper.primary == "#00FF00"

    def test_to_dict(self):
        t = TeamColors(
            player=KitColors(primary="#FF0000", number="#FFF", border="#000"),
            goalkeeper=KitColors(primary="#00FF00", number="#000", border="#FFF"),
        )
        d = t.to_dict()
        assert d["player"]["primary"] == "#FF0000"
        assert d["goalkeeper"]["primary"] == "#00FF00"


# ---------------------------------------------------------------------------
#  Coach
# ---------------------------------------------------------------------------

class TestCoach:
    def test_from_api_none(self):
        c = Coach.from_api(None)
        assert c.id is None
        assert c.name is None
        assert c.photo is None

    def test_from_api_full(self):
        c = Coach.from_api({"id": 123, "name": "Pep Guardiola", "photo": "https://x.com/pep.jpg"})
        assert c.id == 123
        assert c.name == "Pep Guardiola"
        assert c.photo == "https://x.com/pep.jpg"

    def test_to_dict(self):
        c = Coach(id=123, name="Pep Guardiola", photo="https://x.com/pep.jpg")
        assert c.to_dict() == {"id": 123, "name": "Pep Guardiola", "photo": "https://x.com/pep.jpg"}


# ---------------------------------------------------------------------------
#  LineupPlayer
# ---------------------------------------------------------------------------

class TestLineupPlayer:
    @pytest.fixture
    def player_data(self):
        return {"player": {"id": 10, "name": "John Stones", "number": 5, "pos": "D", "grid": "2:3"}}

    @pytest.fixture
    def player(self, player_data):
        return LineupPlayer.from_api(player_data)

    def test_from_api(self, player):
        assert player.id == 10
        assert player.name == "John Stones"
        assert player.number == 5
        assert player.pos == "D"
        assert player.grid == "2:3"

    def test_from_api_no_grid(self):
        p = LineupPlayer.from_api({"player": {"id": 1, "name": "GK", "number": 1, "pos": "G", "grid": None}})
        assert p.grid is None

    def test_grid_row(self, player):
        assert player.grid_row == 2

    def test_grid_row_none(self):
        p = LineupPlayer(id=1, name="", number=0, pos="", grid=None)
        assert p.grid_row is None

    def test_grid_col(self, player):
        assert player.grid_col == 3

    def test_grid_col_none(self):
        p = LineupPlayer(id=1, name="", number=0, pos="", grid=None)
        assert p.grid_col is None

    def test_is_goalkeeper(self):
        assert LineupPlayer(id=1, name="", number=0, pos="G", grid=None).is_goalkeeper is True
        assert LineupPlayer(id=2, name="", number=0, pos="D", grid=None).is_goalkeeper is False

    def test_is_defender(self):
        assert LineupPlayer(id=1, name="", number=0, pos="D", grid=None).is_defender is True
        assert LineupPlayer(id=2, name="", number=0, pos="M", grid=None).is_defender is False

    def test_is_midfielder(self):
        assert LineupPlayer(id=1, name="", number=0, pos="M", grid=None).is_midfielder is True
        assert LineupPlayer(id=2, name="", number=0, pos="D", grid=None).is_midfielder is False

    def test_is_attacker(self):
        assert LineupPlayer(id=1, name="", number=0, pos="F", grid=None).is_attacker is True
        assert LineupPlayer(id=2, name="", number=0, pos="M", grid=None).is_attacker is False

    def test_position_constants(self):
        assert Position.GOALKEEPER == "G"
        assert Position.DEFENDER == "D"
        assert Position.MIDFIELDER == "M"
        assert Position.ATTACKER == "F"

    def test_to_dict(self, player):
        d = player.to_dict()
        assert d["player"]["id"] == 10
        assert d["player"]["name"] == "John Stones"
        assert d["player"]["pos"] == "D"
        assert d["player"]["grid"] == "2:3"


# ---------------------------------------------------------------------------
#  TeamLineup
# ---------------------------------------------------------------------------

class TestTeamLineup:
    @pytest.fixture
    def lineup_data(self):
        return {
            "team": {"id": 2284, "name": "Manchester City", "logo": "https://x.com/mci.png"},
            "formation": "4-3-3",
            "coach": {"id": 123, "name": "Pep Guardiola", "photo": "https://x.com/pep.jpg"},
            "startXI": [
                {"player": {"id": 1, "name": "Ederson", "number": 1, "pos": "G", "grid": "1:1"}},
                {"player": {"id": 2, "name": "Walker", "number": 2, "pos": "D", "grid": "2:1"}},
                {"player": {"id": 3, "name": "Stones", "number": 5, "pos": "D", "grid": "2:2"}},
                {"player": {"id": 10, "name": "De Bruyne", "number": 17, "pos": "M", "grid": "3:2"}},
                {"player": {"id": 9, "name": "Haaland", "number": 9, "pos": "F", "grid": "4:2"}},
            ],
            "substitutes": [
                {"player": {"id": 18, "name": "Ortega", "number": 18, "pos": "G", "grid": None}},
            ],
        }

    @pytest.fixture
    def lineup(self, lineup_data):
        return TeamLineup.from_api(lineup_data)

    def test_from_api(self, lineup):
        assert lineup.team_id == 2284
        assert lineup.team_name == "Manchester City"
        assert lineup.formation == "4-3-3"
        assert lineup.coach.name == "Pep Guardiola"
        assert len(lineup.start_xi) == 5
        assert len(lineup.substitutes) == 1

    def test_goalkeeper(self, lineup):
        gk = lineup.goalkeeper
        assert gk is not None
        assert gk.name == "Ederson"

    def test_goalkeeper_none(self):
        t = TeamLineup(team_id=0, team_name="", team_logo="", formation=None,
                       colors=TeamColors.from_api(None), coach=Coach.from_api(None))
        assert t.goalkeeper is None

    def test_defenders(self, lineup):
        defs = lineup.defenders
        assert len(defs) == 2
        assert all(p.pos == "D" for p in defs)

    def test_midfielders(self, lineup):
        mids = lineup.midfielders
        assert len(mids) == 1
        assert mids[0].name == "De Bruyne"

    def test_attackers(self, lineup):
        fwds = lineup.attackers
        assert len(fwds) == 1
        assert fwds[0].name == "Haaland"

    def test_find_player_in_start_xi(self, lineup):
        p = lineup.find_player(9)
        assert p is not None
        assert p.name == "Haaland"

    def test_find_player_in_substitutes(self, lineup):
        p = lineup.find_player(18)
        assert p is not None
        assert p.name == "Ortega"

    def test_find_player_not_found(self, lineup):
        assert lineup.find_player(999) is None

    def test_is_starter_true(self, lineup):
        assert lineup.is_starter(1) is True

    def test_is_starter_false(self, lineup):
        assert lineup.is_starter(18) is False

    def test_is_substitute_true(self, lineup):
        assert lineup.is_substitute(18) is True

    def test_is_substitute_false(self, lineup):
        assert lineup.is_substitute(1) is False

    def test_grid_map(self, lineup):
        g = lineup.grid_map()
        assert g["1:1"].name == "Ederson"
        assert g["2:1"].name == "Walker"
        assert g["2:2"].name == "Stones"
        assert g["3:2"].name == "De Bruyne"
        assert g["4:2"].name == "Haaland"
        assert len(g) == 5

    def test_to_dict(self, lineup):
        d = lineup.to_dict()
        assert d["team"]["id"] == 2284
        assert d["formation"] == "4-3-3"
        assert d["coach"]["name"] == "Pep Guardiola"
        assert len(d["startXI"]) == 5
        assert len(d["substitutes"]) == 1

    def test_to_json(self, lineup):
        parsed = json.loads(lineup.to_json())
        assert parsed["team"]["name"] == "Manchester City"
        assert parsed["formation"] == "4-3-3"


# ---------------------------------------------------------------------------
#  FixtureLineups
# ---------------------------------------------------------------------------

class TestFixtureLineups:
    @pytest.fixture
    def home_data(self):
        return {
            "team": {"id": 1, "name": "Home", "logo": ""},
            "formation": "4-4-2",
            "coach": {"id": 1, "name": "Coach A", "photo": ""},
            "startXI": [{"player": {"id": 10, "name": "A", "number": 10, "pos": "F", "grid": "4:1"}}],
            "substitutes": [],
        }

    @pytest.fixture
    def away_data(self):
        return {
            "team": {"id": 2, "name": "Away", "logo": ""},
            "formation": "3-5-2",
            "coach": {"id": 2, "name": "Coach B", "photo": ""},
            "startXI": [{"player": {"id": 20, "name": "B", "number": 20, "pos": "M", "grid": "3:2"}}],
            "substitutes": [],
        }

    @pytest.fixture
    def lineups(self, home_data, away_data):
        data = {"response": [home_data, away_data]}
        return FixtureLineups.from_api(data, fixture_id=100)

    def test_from_api(self, lineups):
        assert lineups.fixture_id == 100
        assert lineups.home.team_id == 1
        assert lineups.away.team_id == 2

    def test_for_team_home(self, lineups):
        assert lineups.for_team(1).team_name == "Home"

    def test_for_team_away(self, lineups):
        assert lineups.for_team(2).team_name == "Away"

    def test_for_team_not_found(self, lineups):
        assert lineups.for_team(999) is None

    def test_find_player_found(self, lineups):
        result = lineups.find_player(10)
        assert result is not None
        lineup, player = result
        assert lineup.team_name == "Home"
        assert player.name == "A"

    def test_find_player_not_found(self, lineups):
        assert lineups.find_player(999) is None

    def test_to_dict(self, lineups):
        d = lineups.to_dict()
        assert d["fixture_id"] == 100
        assert d["home"]["team"]["id"] == 1
        assert d["away"]["team"]["id"] == 2

    def test_to_json(self, lineups):
        parsed = json.loads(lineups.to_json())
        assert parsed["fixture_id"] == 100
        assert parsed["home"]["formation"] == "4-4-2"
