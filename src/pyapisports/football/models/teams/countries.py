import json
from dataclasses import dataclass
from typing import Any, Iterator

from pyapisports.football.models import Country


@dataclass
class TeamCountryList:
    countries: list[Country]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamCountryList":
        return cls(countries=[Country.from_api(c) for c in data["response"]])

    def __iter__(self) -> Iterator[Country]:
        return iter(self.countries)

    def __len__(self) -> int:
        return len(self.countries)

    def __contains__(self, item: Country) -> bool:
        return item in self.countries

    def to_list(self) -> list[dict[str, Any]]:
        return [c.to_dict() for c in self.countries]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
