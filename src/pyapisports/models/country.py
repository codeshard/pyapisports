import json
from dataclasses import dataclass
from typing import Any, Iterator, Optional


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
class CountryList:
    countries: list[Country]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "CountryList":
        return cls(countries=[Country.from_api(c) for c in data["response"]])

    def __iter__(self) -> Iterator[Country]:
        return iter(self.countries)

    def __len__(self) -> int:
        return len(self.countries)

    def __getitem__(self, index: int) -> Country:
        return self.countries[index]

    def find_by_name(self, name: str) -> Optional[Country]:
        name = name.lower()
        return next(
            (c for c in self.countries if c.name.lower() == name), None
        )

    def find_by_code(self, code: str) -> Optional[Country]:
        code = code.upper()
        return next((c for c in self.countries if c.code == code), None)

    def to_list(self) -> list[dict[str, Any]]:
        return [c.to_dict() for c in self.countries]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
