import json
from dataclasses import dataclass
from typing import Any, Optional

from .base import BaseList


@dataclass
class Venue:
    id: int
    name: str
    address: Optional[str]
    city: str
    country: Optional[str]
    capacity: Optional[int]
    surface: Optional[str]
    image: Optional[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Venue":
        return cls(
            id=data["id"],
            name=data["name"],
            address=data.get("address"),
            city=data["city"],
            country=data.get("country"),
            capacity=data.get("capacity"),
            surface=data.get("surface"),
            image=data.get("image"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "capacity": self.capacity,
            "surface": self.surface,
            "image": self.image,
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class VenueList(BaseList[Venue]):
    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "VenueList":
        return cls(items=[Venue.from_api(venue) for venue in data["response"]])

    def find_by_id(self, id: int) -> Optional[Venue]:
        return next((venue for venue in self.items if venue.id == id), None)

    def find_by_name(self, name: str) -> Optional[Venue]:
        name = name.lower()
        return next(
            (venue for venue in self.items if venue.name.lower() == name),
            None,
        )

    def find_by_city(self, city: str) -> Optional[Venue]:
        city = city.lower()
        return next(
            (venue for venue in self.items if venue.city.lower() == city),
            None,
        )

    def find_by_country(self, country: str) -> Optional[Venue]:
        country = country.capitalize()
        return next(
            (venue for venue in self.items if venue.country == country),
            None,
        )

    def filter_by_param(self, search: str) -> "VenueList":
        search = search.lower()
        return VenueList(
            items=[
                venue for venue in self.items if venue.name.lower() == search
            ]
        )

    def to_list(self) -> list[dict[str, Any]]:
        return [venue.to_dict() for venue in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
