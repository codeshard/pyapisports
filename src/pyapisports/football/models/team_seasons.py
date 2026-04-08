import json
from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class TeamSeasonsList:
    seasons: list[int]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamSeasonsList":
        return cls(seasons=data["response"])

    def __iter__(self) -> Iterator[int]:
        return iter(self.seasons)

    def __len__(self) -> int:
        return len(self.seasons)

    def __contains__(self, item: int) -> bool:
        return item in self.seasons

    def to_list(self) -> list[int]:
        return list(self.seasons)

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
