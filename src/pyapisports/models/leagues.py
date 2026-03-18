import json
from dataclasses import dataclass
from typing import Any, Optional

from .base import BaseList
from .country import Country
from .seasons import Season

# from pyapisports.models import BaseList, Country, Season


@dataclass
class League:
    id: int
    name: str
    type: str
    logo: str
    country: Country
    seasons: list[Season]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "League":
        return cls(
            id=data["league"]["id"],
            name=data["league"]["name"],
            type=data["league"]["type"],
            logo=data["league"]["logo"],
            country=Country.from_api(data["country"]),
            seasons=[Season.from_api(s) for s in data["seasons"]],
        )

    @property
    def current_season(self) -> Optional[Season]:
        return next((s for s in self.seasons if s.current), None)

    def season(self, year: int) -> Optional[Season]:
        return next((s for s in self.seasons if s.year == year), None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "league": {
                "id": self.id,
                "name": self.name,
                "type": self.type,
                "logo": self.logo,
            },
            "country": self.country.to_dict(),
            "seasons": [s.to_dict() for s in self.seasons],
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class LeagueList(BaseList[League]):
    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "LeagueList":
        return cls(
            items=[League.from_api(league) for league in data["response"]]
        )

    def find_by_id(self, id: int) -> Optional[League]:
        return next((league for league in self.items if league.id == id), None)

    def find_by_name(self, name: str) -> Optional[League]:
        name = name.lower()
        return next(
            (league for league in self.items if league.name.lower() == name),
            None,
        )

    def filter_by_country(self, country_code: str) -> "LeagueList":
        code = country_code.upper()
        return LeagueList(
            items=[
                league for league in self.items if league.country.code == code
            ]
        )

    def to_list(self) -> list[dict[str, Any]]:
        return [league.to_dict() for league in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
