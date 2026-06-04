import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterator, Optional


@dataclass
class OddValue:
    value: str
    odd: str
    handicap: Optional[str]
    main: Optional[bool]
    suspended: Optional[bool]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "OddValue":
        return cls(
            value=data["value"],
            odd=data["odd"],
            handicap=data.get("handicap"),
            main=data.get("main"),
            suspended=data.get("suspended"),
        )

    @property
    def odd_float(self) -> Optional[float]:
        try:
            return float(self.odd)
        except (ValueError, TypeError):
            return None

    @property
    def implied_probability(self) -> Optional[float]:
        f = self.odd_float
        if not f or f <= 0:
            return None
        return round((1 / f) * 100, 2)

    @property
    def is_suspended(self) -> bool:
        return self.suspended is True

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "odd": self.odd,
            "handicap": self.handicap,
            "main": self.main,
            "suspended": self.suspended,
        }


@dataclass
class Bet:
    id: int
    name: str
    values: list[OddValue] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Bet":
        return cls(
            id=data["id"],
            name=data["name"],
            values=[OddValue.from_api(v) for v in data.get("values", [])],
        )

    def get(self, value: str) -> Optional[OddValue]:
        value_lower = value.lower()
        return next(
            (v for v in self.values if v.value.lower() == value_lower), None
        )

    @property
    def available(self) -> list[OddValue]:
        return [v for v in self.values if not v.is_suspended]

    @property
    def best_value(self) -> Optional[OddValue]:
        available = self.available
        if not available:
            return None
        return max(available, key=lambda v: v.odd_float or 0.0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "values": [v.to_dict() for v in self.values],
        }


@dataclass
class Bookmaker:
    id: int
    name: str
    bets: list[Bet] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Bookmaker":
        return cls(
            id=data["id"],
            name=data["name"],
            bets=[Bet.from_api(b) for b in data.get("bets", [])],
        )

    def get_bet(self, bet_id: int) -> Optional[Bet]:
        return next((b for b in self.bets if b.id == bet_id), None)

    def get_bet_by_name(self, name: str) -> Optional[Bet]:
        name_lower = name.lower()
        return next(
            (b for b in self.bets if b.name.lower() == name_lower), None
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "bets": [b.to_dict() for b in self.bets],
        }


@dataclass
class FixtureOdds:
    fixture_id: int
    league_id: int
    league_name: str
    league_season: int
    update: datetime
    bookmakers: list[Bookmaker] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureOdds":
        return cls(
            fixture_id=data["fixture"]["id"],
            league_id=data["league"]["id"],
            league_name=data["league"]["name"],
            league_season=data["league"]["season"],
            update=datetime.fromisoformat(data["update"]),
            bookmakers=[
                Bookmaker.from_api(b) for b in data.get("bookmakers", [])
            ],
        )

    def get_bookmaker(self, bookmaker_id: int) -> Optional[Bookmaker]:
        return next((b for b in self.bookmakers if b.id == bookmaker_id), None)

    def get_bookmaker_by_name(self, name: str) -> Optional[Bookmaker]:
        name_lower = name.lower()
        return next(
            (b for b in self.bookmakers if b.name.lower() == name_lower), None
        )

    def best_odd_for(self, bet_name: str, value: str) -> Optional[OddValue]:
        candidates: list[OddValue] = []
        for bm in self.bookmakers:
            bet = bm.get_bet_by_name(bet_name)
            if bet:
                ov = bet.get(value)
                if ov and not ov.is_suspended:
                    candidates.append(ov)
        if not candidates:
            return None
        return max(candidates, key=lambda v: v.odd_float or 0.0)

    def compare_bookmakers(
        self, bet_name: str, value: str
    ) -> list[dict[str, Any]]:
        results = []
        for bm in self.bookmakers:
            bet = bm.get_bet_by_name(bet_name)
            if bet:
                ov = bet.get(value)
                if ov and not ov.is_suspended:
                    results.append(
                        {
                            "bookmaker": bm.name,
                            "odd": ov.odd,
                            "implied": ov.implied_probability,
                        }
                    )
        return sorted(
            results,
            key=lambda r: float(r["odd"]) if r["odd"] else 0.0,
            reverse=True,
        )

    def market_summary(self, bet_name: str) -> dict[str, Any]:
        outcome_map: dict[str, dict[str, Any]] = {}
        for bm in self.bookmakers:
            bet = bm.get_bet_by_name(bet_name)
            if not bet:
                continue
            for ov in bet.available:
                current = outcome_map.get(ov.value)
                ov_float = ov.odd_float or 0.0
                if not current or ov_float > float(current["best_odd"]):
                    outcome_map[ov.value] = {
                        "best_odd": ov.odd,
                        "bookmaker": bm.name,
                        "implied": ov.implied_probability,
                    }
        return {"market": bet_name, "outcomes": outcome_map}

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture": {"id": self.fixture_id},
            "league": {
                "id": self.league_id,
                "name": self.league_name,
                "season": self.league_season,
            },
            "update": self.update.isoformat(),
            "bookmakers": [b.to_dict() for b in self.bookmakers],
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class OddsList:
    items: list[FixtureOdds] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "OddsList":
        return cls(items=[FixtureOdds.from_api(f) for f in data["response"]])

    def __iter__(self) -> Iterator[FixtureOdds]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> FixtureOdds:
        return self.items[index]

    def find_by_fixture(self, fixture_id: int) -> Optional[FixtureOdds]:
        return next(
            (o for o in self.items if o.fixture_id == fixture_id), None
        )

    def to_list(self) -> list[dict[str, Any]]:
        return [o.to_dict() for o in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
