import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterator, Optional


@dataclass
class StandingRecord:
    played: int
    win: int
    draw: int
    lose: int
    goals_for: int
    goals_against: int

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "StandingRecord":
        goals = data.get("goals", {})
        return cls(
            played=data["played"],
            win=data["win"],
            draw=data["draw"],
            lose=data["lose"],
            goals_for=goals.get("for", 0),
            goals_against=goals.get("against", 0),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "played": self.played,
            "win": self.win,
            "draw": self.draw,
            "lose": self.lose,
            "goals": {
                "for": self.goals_for,
                "against": self.goals_against,
            },
        }


@dataclass
class StandingEntry:
    rank: int
    team_id: int
    team_name: str
    team_logo: str
    points: int
    goals_diff: int
    group: str
    form: Optional[str]
    status: str
    description: Optional[str]
    all: StandingRecord
    home: StandingRecord
    away: StandingRecord
    updated: datetime

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "StandingEntry":
        return cls(
            rank=data["rank"],
            team_id=data["team"]["id"],
            team_name=data["team"]["name"],
            team_logo=data["team"]["logo"],
            points=data["points"],
            goals_diff=data["goalsDiff"],
            group=data["group"],
            form=data.get("form"),
            status=data["status"],
            description=data.get("description"),
            all=StandingRecord.from_api(data["all"]),
            home=StandingRecord.from_api(data["home"]),
            away=StandingRecord.from_api(data["away"]),
            updated=datetime.fromisoformat(data["update"]),
        )

    @property
    def played(self) -> int:
        return self.all.played

    @property
    def form_list(self) -> list[str]:
        return list(self.form) if self.form else []

    @property
    def is_promoted(self) -> bool:
        return bool(
            self.description and "promotion" in self.description.lower()
        )

    @property
    def is_relegated(self) -> bool:
        return bool(
            self.description and "relegation" in self.description.lower()
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "team": {
                "id": self.team_id,
                "name": self.team_name,
                "logo": self.team_logo,
            },
            "points": self.points,
            "goalsDiff": self.goals_diff,
            "group": self.group,
            "form": self.form,
            "status": self.status,
            "description": self.description,
            "all": self.all.to_dict(),
            "home": self.home.to_dict(),
            "away": self.away.to_dict(),
            "update": self.updated.isoformat(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class StandingsTable:
    entries: list[StandingEntry]

    def __iter__(self) -> Iterator[StandingEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index: int) -> StandingEntry:
        return self.entries[index]

    @classmethod
    def from_api(cls, data: list[dict[str, Any]]) -> "StandingsTable":
        return cls(entries=[StandingEntry.from_api(e) for e in data])

    def find_by_team_id(self, team_id: int) -> Optional[StandingEntry]:
        return next((e for e in self.entries if e.team_id == team_id), None)

    def find_by_team_name(self, name: str) -> Optional[StandingEntry]:
        name = name.lower()
        return next(
            (e for e in self.entries if e.team_name.lower() == name), None
        )

    def find_by_rank(self, rank: int) -> Optional[StandingEntry]:
        return next((e for e in self.entries if e.rank == rank), None)

    def promoted(self) -> "StandingsTable":
        return StandingsTable(
            entries=[e for e in self.entries if e.is_promoted]
        )

    def relegated(self) -> "StandingsTable":
        return StandingsTable(
            entries=[e for e in self.entries if e.is_relegated]
        )

    def top(self, n: int) -> "StandingsTable":
        return StandingsTable(entries=self.entries[:n])

    def to_list(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self.entries]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)


@dataclass
class Standings:
    league_id: int
    league_name: str
    league_country: str
    league_logo: str
    league_flag: Optional[str]
    league_season: int
    tables: list[StandingsTable]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Standings":
        league = data["response"][0]["league"]
        return cls(
            league_id=league["id"],
            league_name=league["name"],
            league_country=league["country"],
            league_logo=league["logo"],
            league_flag=league.get("flag"),
            league_season=league["season"],
            tables=[
                StandingsTable.from_api(table) for table in league["standings"]
            ],
        )

    @property
    def table(self) -> StandingsTable:
        return self.tables[0]

    @property
    def is_multi_group(self) -> bool:
        return len(self.tables) > 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "league": {
                "id": self.league_id,
                "name": self.league_name,
                "country": self.league_country,
                "logo": self.league_logo,
                "flag": self.league_flag,
                "season": self.league_season,
                "standings": [t.to_list() for t in self.tables],
            }
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
