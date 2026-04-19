import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterator, Optional

from pyapisports.football.models.venues import Venue


@dataclass
class FixtureStatus:
    long: str
    short: str
    elapsed: Optional[int]
    extra: Optional[int]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureStatus":
        return cls(
            long=data["long"],
            short=data["short"],
            elapsed=data.get("elapsed"),
            extra=data.get("extra"),
        )

    @property
    def is_live(self) -> bool:
        return self.short in {"1H", "HT", "2H", "ET", "BT", "P", "INT", "LIVE"}

    @property
    def is_finished(self) -> bool:
        return self.short in {"FT", "AET", "PEN"}

    @property
    def is_scheduled(self) -> bool:
        return self.short == "NS"

    @property
    def is_cancelled(self) -> bool:
        return self.short in {"CANC", "ABD", "PST"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "long": self.long,
            "short": self.short,
            "elapsed": self.elapsed,
            "extra": self.extra,
        }


@dataclass
class FixtureLeague:
    id: int
    name: str
    country: str
    logo: str
    flag: Optional[str]
    season: int
    round: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureLeague":
        return cls(
            id=data["id"],
            name=data["name"],
            country=data["country"],
            logo=data["logo"],
            flag=data.get("flag"),
            season=data["season"],
            round=data["round"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "logo": self.logo,
            "flag": self.flag,
            "season": self.season,
            "round": self.round,
        }


@dataclass
class FixtureTeam:
    id: int
    name: str
    logo: str
    winner: Optional[bool]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureTeam":
        return cls(
            id=data["id"],
            name=data["name"],
            logo=data["logo"],
            winner=data.get("winner"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "logo": self.logo,
            "winner": self.winner,
        }


@dataclass
class PeriodScore:
    home: Optional[int]
    away: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PeriodScore":
        if not data:
            return cls(home=None, away=None)
        return cls(home=data.get("home"), away=data.get("away"))

    def to_dict(self) -> dict[str, Any]:
        return {"home": self.home, "away": self.away}


@dataclass
class FixtureScore:
    halftime: PeriodScore
    fulltime: PeriodScore
    extratime: PeriodScore
    penalty: PeriodScore

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureScore":
        return cls(
            halftime=PeriodScore.from_api(data.get("halftime")),
            fulltime=PeriodScore.from_api(data.get("fulltime")),
            extratime=PeriodScore.from_api(data.get("extratime")),
            penalty=PeriodScore.from_api(data.get("penalty")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "halftime": self.halftime.to_dict(),
            "fulltime": self.fulltime.to_dict(),
            "extratime": self.extratime.to_dict(),
            "penalty": self.penalty.to_dict(),
        }


@dataclass
class Fixture:
    id: int
    referee: Optional[str]
    timezone: str
    date: datetime
    timestamp: int
    venue: Venue
    status: FixtureStatus
    league: FixtureLeague
    home_team: FixtureTeam
    away_team: FixtureTeam
    goals_home: Optional[int]
    goals_away: Optional[int]
    score: FixtureScore

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Fixture":
        f = data["fixture"]
        goals = data.get("goals", {})
        return cls(
            id=f["id"],
            referee=f.get("referee"),
            timezone=f["timezone"],
            date=datetime.fromisoformat(f["date"]),
            timestamp=f["timestamp"],
            venue=Venue.from_api(f.get("venue")),
            status=FixtureStatus.from_api(f["status"]),
            league=FixtureLeague.from_api(data["league"]),
            home_team=FixtureTeam.from_api(data["teams"]["home"]),
            away_team=FixtureTeam.from_api(data["teams"]["away"]),
            goals_home=goals.get("home"),
            goals_away=goals.get("away"),
            score=FixtureScore.from_api(data["score"]),
        )

    @property
    def is_live(self) -> bool:
        return self.status.is_live

    @property
    def is_finished(self) -> bool:
        return self.status.is_finished

    @property
    def is_scheduled(self) -> bool:
        return self.status.is_scheduled

    @property
    def is_cancelled(self) -> bool:
        return self.status.is_cancelled

    @property
    def score_str(self) -> str:
        h = self.goals_home if self.goals_home is not None else "?"
        a = self.goals_away if self.goals_away is not None else "?"
        return f"{h} - {a}"

    @property
    def winner(self) -> Optional[FixtureTeam]:
        if self.home_team.winner is True:
            return self.home_team
        if self.away_team.winner is True:
            return self.away_team
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture": {
                "id": self.id,
                "referee": self.referee,
                "timezone": self.timezone,
                "date": self.date.isoformat(),
                "timestamp": self.timestamp,
                "venue": self.venue.to_dict(),
                "status": self.status.to_dict(),
            },
            "league": self.league.to_dict(),
            "teams": {
                "home": self.home_team.to_dict(),
                "away": self.away_team.to_dict(),
            },
            "goals": {
                "home": self.goals_home,
                "away": self.goals_away,
            },
            "score": self.score.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class FixtureList:
    items: list[Fixture] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureList":
        return cls(items=[Fixture.from_api(f) for f in data["response"]])

    def __iter__(self) -> Iterator[Fixture]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> Fixture:
        return self.items[index]

    def find_by_id(self, fixture_id: int) -> Optional[Fixture]:
        return next((f for f in self.items if f.id == fixture_id), None)

    def live(self) -> "FixtureList":
        return FixtureList(items=[f for f in self.items if f.is_live])

    def finished(self) -> "FixtureList":
        return FixtureList(items=[f for f in self.items if f.is_finished])

    def scheduled(self) -> "FixtureList":
        return FixtureList(items=[f for f in self.items if f.is_scheduled])

    def by_team(self, team_id: int) -> "FixtureList":
        return FixtureList(
            items=[
                f
                for f in self.items
                if f.home_team.id == team_id or f.away_team.id == team_id
            ]
        )

    def by_round(self, round_name: str) -> "FixtureList":
        return FixtureList(
            items=[f for f in self.items if f.league.round == round_name]
        )

    def to_list(self) -> list[dict[str, Any]]:
        return [f.to_dict() for f in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
