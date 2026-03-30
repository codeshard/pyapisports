import json
from dataclasses import dataclass
from typing import Any, Optional

from .base import BaseList
from .venues import Venue


@dataclass
class Team:
    id: int
    name: str
    code: str
    country: str
    founded: int
    national: bool
    logo: str
    venue: Venue

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Team":
        return cls(
            id=data["team"]["id"],
            name=data["team"]["name"],
            code=data["team"]["code"],
            country=data["team"]["country"],
            founded=data["team"]["founded"],
            national=data["team"]["national"],
            logo=data["team"]["logo"],
            venue=Venue.from_api(data["venue"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "team": {
                "id": self.id,
                "name": self.name,
                "code": self.code,
                "team": self.code,
                "founded": self.founded,
                "national": self.national,
                "logo": self.logo,
            },
            "venue": self.venue.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class TeamList(BaseList[Team]):
    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamList":
        return cls(items=[Team.from_api(team) for team in data["response"]])

    def filter_by_id(self, id: int) -> Optional[Team]:
        return next((team for team in self.items if team.id == id), None)

    def filter_by_name(self, name: str) -> Optional[Team]:
        name = name.lower()
        return next(
            (team for team in self.items if team.name.lower() == name),
            None,
        )

    def filter_by_country(self, country: str) -> "TeamList":
        return TeamList(
            items=[
                team
                for team in self.items
                if team.country == country.capitalize()
            ]
        )

    def filter_by_code(self, code: str) -> "TeamList":
        return TeamList(
            items=[team for team in self.items if team.code == code.upper()]
        )

    def filter_by_venue(self, venue_id: int) -> "TeamList":
        return TeamList(
            items=[team for team in self.items if team.venue.id == venue_id]
        )

    def filter_by_param(self, search: str) -> "TeamList":
        search = search.lower()
        return TeamList(
            items=[team for team in self.items if team.name == search]
        )

    def to_list(self) -> list[dict[str, Any]]:
        return [team.to_dict() for team in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
