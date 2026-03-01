import json
from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class TimezoneList:
    timezones: list[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TimezoneList":
        return cls(timezones=data["response"])

    def __iter__(self) -> Iterator[str]:
        return iter(self.timezones)

    def __len__(self) -> int:
        return len(self.timezones)

    def __contains__(self, item: str) -> bool:
        return item in self.timezones

    def search(self, query: str) -> list[str]:
        q = query.lower()
        return [tz for tz in self.timezones if q in tz.lower()]

    def to_list(self) -> list[str]:
        return list(self.timezones)

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
