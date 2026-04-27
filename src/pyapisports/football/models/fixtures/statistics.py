import json
from dataclasses import dataclass, field
from typing import Any, Optional, Union


class StatType:
    SHOTS_ON_GOAL = "Shots on Goal"
    SHOTS_OFF_GOAL = "Shots off Goal"
    SHOTS_TOTAL = "Total Shots"
    SHOTS_BLOCKED = "Blocked Shots"
    SHOTS_INSIDE_BOX = "Shots insidebox"
    SHOTS_OUTSIDE_BOX = "Shots outsidebox"
    FOULS = "Fouls"
    CORNERS = "Corner Kicks"
    OFFSIDES = "Offsides"
    BALL_POSSESSION = "Ball Possession"
    YELLOW_CARDS = "Yellow Cards"
    RED_CARDS = "Red Cards"
    GOALKEEPER_SAVES = "Goalkeeper Saves"
    TOTAL_PASSES = "Total passes"
    ACCURATE_PASSES = "Passes accurate"
    PASSES_PERCENTAGE = "Passes %"
    EXPECTED_GOALS = "expected_goals"


@dataclass
class StatEntry:
    type: str
    value: Optional[Union[int, str]]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "StatEntry":
        return cls(
            type=data["type"],
            value=data.get("value"),
        )

    @property
    def int_value(self) -> Optional[int]:
        if self.value is None:
            return None
        if isinstance(self.value, int):
            return self.value
        if isinstance(self.value, str):
            try:
                return int(self.value.replace("%", "").strip())
            except ValueError:
                return None
        return None

    @property
    def float_value(self) -> Optional[float]:
        if self.value is None:
            return None
        if isinstance(self.value, (int, float)):
            return float(self.value)
        if isinstance(self.value, str):
            try:
                return float(self.value.replace("%", "").strip())
            except ValueError:
                return None
        return None

    @property
    def is_percentage(self) -> bool:
        return isinstance(self.value, str) and "%" in self.value

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "value": self.value}


@dataclass
class TeamFixtureStatistics:
    team_id: int
    team_name: str
    team_logo: str
    stats: list[StatEntry] = field(default_factory=list)
    _index: dict[str, StatEntry] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self._index = {s.type: s for s in self.stats}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamFixtureStatistics":
        stats = [StatEntry.from_api(s) for s in data.get("statistics", [])]
        obj = cls(
            team_id=data["team"]["id"],
            team_name=data["team"]["name"],
            team_logo=data["team"]["logo"],
            stats=stats,
        )
        return obj

    def get(self, stat_type: str) -> Optional[StatEntry]:
        """Return a StatEntry by type string, or None if not present."""
        return self._index.get(stat_type)

    def value_of(self, stat_type: str) -> Optional[Union[int, str]]:
        """Return the raw value for a stat type, or None."""
        entry = self.get(stat_type)
        return entry.value if entry else None

    def int_value_of(self, stat_type: str) -> Optional[int]:
        entry = self.get(stat_type)
        return entry.int_value if entry else None

    def float_value_of(self, stat_type: str) -> Optional[float]:
        entry = self.get(stat_type)
        return entry.float_value if entry else None

    @property
    def shots_on_goal(self) -> Optional[int]:
        return self.int_value_of(StatType.SHOTS_ON_GOAL)

    @property
    def shots_off_goal(self) -> Optional[int]:
        return self.int_value_of(StatType.SHOTS_OFF_GOAL)

    @property
    def total_shots(self) -> Optional[int]:
        return self.int_value_of(StatType.SHOTS_TOTAL)

    @property
    def blocked_shots(self) -> Optional[int]:
        return self.int_value_of(StatType.SHOTS_BLOCKED)

    @property
    def shots_inside_box(self) -> Optional[int]:
        return self.int_value_of(StatType.SHOTS_INSIDE_BOX)

    @property
    def shots_outside_box(self) -> Optional[int]:
        return self.int_value_of(StatType.SHOTS_OUTSIDE_BOX)

    @property
    def fouls(self) -> Optional[int]:
        return self.int_value_of(StatType.FOULS)

    @property
    def corners(self) -> Optional[int]:
        return self.int_value_of(StatType.CORNERS)

    @property
    def offsides(self) -> Optional[int]:
        return self.int_value_of(StatType.OFFSIDES)

    @property
    def ball_possession(self) -> Optional[int]:
        """Possession as an integer percentage e.g. 56."""
        return self.int_value_of(StatType.BALL_POSSESSION)

    @property
    def yellow_cards(self) -> Optional[int]:
        return self.int_value_of(StatType.YELLOW_CARDS)

    @property
    def red_cards(self) -> Optional[int]:
        return self.int_value_of(StatType.RED_CARDS)

    @property
    def goalkeeper_saves(self) -> Optional[int]:
        return self.int_value_of(StatType.GOALKEEPER_SAVES)

    @property
    def total_passes(self) -> Optional[int]:
        return self.int_value_of(StatType.TOTAL_PASSES)

    @property
    def accurate_passes(self) -> Optional[int]:
        return self.int_value_of(StatType.ACCURATE_PASSES)

    @property
    def pass_accuracy(self) -> Optional[int]:
        """Pass accuracy as an integer percentage e.g. 87."""
        return self.int_value_of(StatType.PASSES_PERCENTAGE)

    @property
    def expected_goals(self) -> Optional[float]:
        return self.float_value_of(StatType.EXPECTED_GOALS)

    def to_dict(self) -> dict[str, Any]:
        return {
            "team": {
                "id": self.team_id,
                "name": self.team_name,
                "logo": self.team_logo,
            },
            "statistics": [s.to_dict() for s in self.stats],
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class FixtureStatistics:
    fixture_id: int
    home: TeamFixtureStatistics
    away: TeamFixtureStatistics

    @classmethod
    def from_api(
        cls, data: dict[str, Any], fixture_id: int
    ) -> "FixtureStatistics":
        response = data["response"]
        return cls(
            fixture_id=fixture_id,
            home=TeamFixtureStatistics.from_api(response[0]),
            away=TeamFixtureStatistics.from_api(response[1]),
        )

    def compare(self, stat_type: str) -> dict[str, Any]:
        return {
            "type": stat_type,
            "home": self.home.int_value_of(stat_type),
            "away": self.away.int_value_of(stat_type),
        }

    def summary(self) -> dict[str, Any]:
        all_types = [s.type for s in self.home.stats]
        return {
            "fixture_id": self.fixture_id,
            "home_team": self.home.team_name,
            "away_team": self.away.team_name,
            "stats": [self.compare(t) for t in all_types],
        }

    def for_team(self, team_id: int) -> Optional[TeamFixtureStatistics]:
        if self.home.team_id == team_id:
            return self.home
        if self.away.team_id == team_id:
            return self.away
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "home": self.home.to_dict(),
            "away": self.away.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
