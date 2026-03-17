import json
from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class SeasonsList:
    seasons: list[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "SeasonsList":
        return cls(seasons=data["response"])

    def __iter__(self) -> Iterator[str]:
        return iter(self.seasons)

    def __len__(self) -> int:
        return len(self.seasons)

    def __contains__(self, item: str) -> bool:
        return item in self.seasons

    def search(self, query: str) -> list[str]:
        q = query.lower()
        return [tz for tz in self.seasons if q in tz.lower()]

    def to_list(self) -> list[str]:
        return list(self.seasons)

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
