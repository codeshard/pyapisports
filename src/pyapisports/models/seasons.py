import json
from dataclasses import dataclass
from datetime import date
from typing import Any, Iterator

from .coverage import Coverage


@dataclass
class Season:
    year: int
    start: date
    end: date
    current: bool
    coverage: Coverage

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Season":
        return cls(
            year=data["year"],
            start=date.fromisoformat(data["start"]),
            end=date.fromisoformat(data["end"]),
            current=data["current"],
            coverage=Coverage.from_api(data["coverage"]),
        )

    @property
    def is_active(self) -> bool:
        return self.current

    def to_dict(self) -> dict[str, Any]:
        return {
            "year": self.year,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "current": self.current,
            "coverage": self.coverage.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


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

    def to_list(self) -> list[str]:
        return list(self.seasons)

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
