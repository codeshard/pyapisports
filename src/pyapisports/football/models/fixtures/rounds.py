import json
from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class RoundsList:
    rounds: list[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "RoundsList":
        return cls(rounds=data["response"])

    def __iter__(self) -> Iterator[str]:
        return iter(self.rounds)

    def __len__(self) -> int:
        return len(self.rounds)

    def __contains__(self, item: str) -> bool:
        return item in self.rounds

    def to_list(self) -> list[str]:
        return list(self.rounds)

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
