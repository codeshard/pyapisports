import json
from dataclasses import dataclass
from typing import Any, Optional

from .base import BaseList


@dataclass
class Country:
    name: str
    code: Optional[str]
    flag: Optional[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Country":
        return cls(
            name=data["name"],
            code=data.get("code"),
            flag=data.get("flag"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "code": self.code,
            "flag": self.flag,
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class CountryList(BaseList[Country]):
    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "CountryList":
        return cls(
            items=[Country.from_api(country) for country in data["response"]]
        )

    def find_by_name(self, name: str) -> Optional[Country]:
        name = name.lower()
        return next(
            (
                country
                for country in self.items
                if country.name.lower() == name
            ),
            None,
        )

    def find_by_code(self, code: str) -> Optional[Country]:
        code = code.upper()
        return next((c for c in self.items if c.code == code), None)

    def to_list(self) -> list[dict[str, Any]]:
        return [country.to_dict() for country in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
