import json
from dataclasses import dataclass, field
from typing import Any, Optional


class Position:
    GOALKEEPER = "G"
    DEFENDER = "D"
    MIDFIELDER = "M"
    ATTACKER = "F"


@dataclass
class KitColors:
    primary: Optional[str]
    number: Optional[str]
    border: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "KitColors":
        if not data:
            return cls(primary=None, number=None, border=None)
        return cls(
            primary=data.get("primary"),
            number=data.get("number"),
            border=data.get("border"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary": self.primary,
            "number": self.number,
            "border": self.border,
        }


@dataclass
class TeamColors:
    player: KitColors
    goalkeeper: KitColors

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "TeamColors":
        if not data:
            return cls(
                player=KitColors.from_api(None),
                goalkeeper=KitColors.from_api(None),
            )
        return cls(
            player=KitColors.from_api(data.get("player")),
            goalkeeper=KitColors.from_api(data.get("goalkeeper")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "player": self.player.to_dict(),
            "goalkeeper": self.goalkeeper.to_dict(),
        }


@dataclass
class Coach:
    id: Optional[int]
    name: Optional[str]
    photo: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "Coach":
        if not data:
            return cls(id=None, name=None, photo=None)
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            photo=data.get("photo"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "photo": self.photo}


@dataclass
class LineupPlayer:
    id: int
    name: str
    number: int
    pos: str
    grid: Optional[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "LineupPlayer":
        p = data["player"]
        return cls(
            id=p["id"],
            name=p["name"],
            number=p["number"],
            pos=p["pos"],
            grid=p.get("grid"),
        )

    @property
    def grid_row(self) -> Optional[int]:
        if not self.grid:
            return None
        return int(self.grid.split(":")[0])

    @property
    def grid_col(self) -> Optional[int]:
        if not self.grid:
            return None
        return int(self.grid.split(":")[1])

    @property
    def is_goalkeeper(self) -> bool:
        return self.pos == Position.GOALKEEPER

    @property
    def is_defender(self) -> bool:
        return self.pos == Position.DEFENDER

    @property
    def is_midfielder(self) -> bool:
        return self.pos == Position.MIDFIELDER

    @property
    def is_attacker(self) -> bool:
        return self.pos == Position.ATTACKER

    def to_dict(self) -> dict[str, Any]:
        return {
            "player": {
                "id": self.id,
                "name": self.name,
                "number": self.number,
                "pos": self.pos,
                "grid": self.grid,
            }
        }


@dataclass
class TeamLineup:
    team_id: int
    team_name: str
    team_logo: str
    formation: Optional[str]
    colors: TeamColors
    coach: Coach
    start_xi: list[LineupPlayer] = field(default_factory=list)
    substitutes: list[LineupPlayer] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamLineup":
        return cls(
            team_id=data["team"]["id"],
            team_name=data["team"]["name"],
            team_logo=data["team"]["logo"],
            formation=data.get("formation"),
            colors=TeamColors.from_api(data.get("team", {}).get("colors")),
            coach=Coach.from_api(data.get("coach")),
            start_xi=[
                LineupPlayer.from_api(p) for p in data.get("startXI", [])
            ],
            substitutes=[
                LineupPlayer.from_api(p) for p in data.get("substitutes", [])
            ],
        )

    @property
    def goalkeeper(self) -> Optional[LineupPlayer]:
        return next((p for p in self.start_xi if p.is_goalkeeper), None)

    @property
    def defenders(self) -> list[LineupPlayer]:
        return [p for p in self.start_xi if p.is_defender]

    @property
    def midfielders(self) -> list[LineupPlayer]:
        return [p for p in self.start_xi if p.is_midfielder]

    @property
    def attackers(self) -> list[LineupPlayer]:
        return [p for p in self.start_xi if p.is_attacker]

    def find_player(self, player_id: int) -> Optional[LineupPlayer]:
        """Search both start XI and substitutes."""
        all_players = self.start_xi + self.substitutes
        return next((p for p in all_players if p.id == player_id), None)

    def is_starter(self, player_id: int) -> bool:
        return any(p.id == player_id for p in self.start_xi)

    def is_substitute(self, player_id: int) -> bool:
        return any(p.id == player_id for p in self.substitutes)

    def grid_map(self) -> dict[str, LineupPlayer]:
        return {p.grid: p for p in self.start_xi if p.grid is not None}

    def to_dict(self) -> dict[str, Any]:
        return {
            "team": {
                "id": self.team_id,
                "name": self.team_name,
                "logo": self.team_logo,
                "colors": self.colors.to_dict(),
            },
            "coach": self.coach.to_dict(),
            "formation": self.formation,
            "startXI": [p.to_dict() for p in self.start_xi],
            "substitutes": [p.to_dict() for p in self.substitutes],
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class FixtureLineups:
    fixture_id: int
    home: TeamLineup
    away: TeamLineup

    @classmethod
    def from_api(
        cls, data: dict[str, Any], fixture_id: int
    ) -> "FixtureLineups":
        response = data["response"]
        return cls(
            fixture_id=fixture_id,
            home=TeamLineup.from_api(response[0]),
            away=TeamLineup.from_api(response[1]),
        )

    def for_team(self, team_id: int) -> Optional[TeamLineup]:
        if self.home.team_id == team_id:
            return self.home
        if self.away.team_id == team_id:
            return self.away
        return None

    def find_player(
        self, player_id: int
    ) -> Optional[tuple[TeamLineup, LineupPlayer]]:
        for lineup in (self.home, self.away):
            player = lineup.find_player(player_id)
            if player:
                return lineup, player
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "home": self.home.to_dict(),
            "away": self.away.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
