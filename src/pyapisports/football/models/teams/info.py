import json
from dataclasses import dataclass
from typing import Any, Optional

from pyapisports.football.models.base import BaseList
from pyapisports.football.models.venues import Venue


@dataclass
class TeamInfo:
    id: int
    name: str
    code: Optional[str]
    country: Optional[str]
    founded: Optional[int]
    national: bool
    logo: str
    venue: Optional[Venue]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamInfo":
        venue_data = data.get("venue")
        return cls(
            id=data["team"]["id"],
            name=data["team"]["name"],
            code=data["team"].get("code"),
            country=data["team"].get("country"),
            founded=data["team"].get("founded"),
            national=data["team"].get("national", False),
            logo=data["team"]["logo"],
            venue=Venue.from_api(venue_data) if venue_data else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "team": {
                "id": self.id,
                "name": self.name,
                "code": self.code,
                "country": self.country,
                "founded": self.founded,
                "national": self.national,
                "logo": self.logo,
            },
            "venue": self.venue.to_dict() if self.venue else None,
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class TeamInfoList(BaseList[TeamInfo]):
    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamInfoList":
        return cls(
            items=[TeamInfo.from_api(team) for team in data["response"]]
        )

    def find_by_id(self, id: int) -> Optional[TeamInfo]:
        return next((team for team in self.items if team.id == id), None)

    def find_by_name(self, name: str) -> Optional[TeamInfo]:
        name = name.lower()
        return next(
            (team for team in self.items if team.name.lower() == name),
            None,
        )

    def filter_by_country(self, country: str) -> "TeamInfoList":
        return TeamInfoList(
            items=[
                team
                for team in self.items
                if team.country and team.country.lower() == country.lower()
            ]
        )

    def filter_by_code(self, code: str) -> "TeamInfoList":
        return TeamInfoList(
            items=[team for team in self.items if team.code == code.upper()]
        )

    def filter_by_venue(self, venue_id: int) -> "TeamInfoList":
        return TeamInfoList(
            items=[
                team
                for team in self.items
                if team.venue and team.venue.id == venue_id
            ]
        )

    def search(self, query: str) -> "TeamInfoList":
        query = query.lower()
        return TeamInfoList(
            items=[team for team in self.items if query in team.name.lower()]
        )

    def to_list(self) -> list[dict[str, Any]]:
        return [team.to_dict() for team in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
