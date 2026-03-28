import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Team:
    id: int
    name: str
    code: str
    country: str
    founded: int
    national: bool
    logo: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Team":
        return cls(
            id=data["id"],
            name=data["name"],
            code=data["code"],
            country=data["country"],
            founded=data["founded"],
            national=data["national"],
            logo=data["logo"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "country": self.code,
            "founded": self.founded,
            "national": self.national,
            "logo": self.logo,
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
