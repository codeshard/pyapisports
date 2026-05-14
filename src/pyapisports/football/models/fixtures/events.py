import json
from dataclasses import dataclass, field
from typing import Any, Iterator, Optional


class EventType:
    GOAL = "Goal"
    CARD = "Card"
    SUBST = "subst"
    VAR = "Var"


class GoalDetail:
    NORMAL_GOAL = "Normal Goal"
    OWN_GOAL = "Own Goal"
    PENALTY = "Penalty"
    MISSED_PENALTY = "Missed Penalty"


class CardDetail:
    YELLOW_CARD = "Yellow Card"
    RED_CARD = "Red Card"
    YELLOW_RED_CARD = "Yellow Red Card"


class VarDetail:
    GOAL_CANCELLED = "Goal cancelled"
    PENALTY_CONFIRMED = "Penalty confirmed"
    CARD_UPGRADE = "Card Upgrade"


@dataclass
class EventTime:
    elapsed: int
    extra: Optional[int]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "EventTime":
        return cls(
            elapsed=data["elapsed"],
            extra=data.get("extra"),
        )

    @property
    def display(self) -> str:
        if self.extra:
            return f"{self.elapsed}+{self.extra}"
        return str(self.elapsed)

    def to_dict(self) -> dict[str, Any]:
        return {"elapsed": self.elapsed, "extra": self.extra}


@dataclass
class EventTeam:
    id: int
    name: str
    logo: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "EventTeam":
        return cls(
            id=data["id"],
            name=data["name"],
            logo=data["logo"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "logo": self.logo}


@dataclass
class EventPlayer:
    id: Optional[int]
    name: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "EventPlayer":
        if not data:
            return cls(id=None, name=None)
        return cls(
            id=data.get("id"),
            name=data.get("name"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name}


@dataclass
class FixtureEvent:
    time: EventTime
    team: EventTeam
    player: EventPlayer
    assist: EventPlayer
    type: str
    detail: str
    comments: Optional[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureEvent":
        return cls(
            time=EventTime.from_api(data["time"]),
            team=EventTeam.from_api(data["team"]),
            player=EventPlayer.from_api(data.get("player")),
            assist=EventPlayer.from_api(data.get("assist")),
            type=data["type"],
            detail=data["detail"],
            comments=data.get("comments"),
        )

    @property
    def is_goal(self) -> bool:
        return self.type == EventType.GOAL

    @property
    def is_own_goal(self) -> bool:
        return (
            self.type == EventType.GOAL and self.detail == GoalDetail.OWN_GOAL
        )

    @property
    def is_penalty_goal(self) -> bool:
        return (
            self.type == EventType.GOAL and self.detail == GoalDetail.PENALTY
        )

    @property
    def is_missed_penalty(self) -> bool:
        return (
            self.type == EventType.GOAL
            and self.detail == GoalDetail.MISSED_PENALTY
        )

    @property
    def is_card(self) -> bool:
        return self.type == EventType.CARD

    @property
    def is_yellow_card(self) -> bool:
        return (
            self.type == EventType.CARD
            and self.detail == CardDetail.YELLOW_CARD
        )

    @property
    def is_red_card(self) -> bool:
        return (
            self.type == EventType.CARD and self.detail == CardDetail.RED_CARD
        )

    @property
    def is_second_yellow(self) -> bool:
        return (
            self.type == EventType.CARD
            and self.detail == CardDetail.YELLOW_RED_CARD
        )

    @property
    def is_substitution(self) -> bool:
        return self.type == EventType.SUBST

    @property
    def is_var(self) -> bool:
        return self.type == EventType.VAR

    @property
    def minute(self) -> str:
        return self.time.display

    def to_dict(self) -> dict[str, Any]:
        return {
            "time": self.time.to_dict(),
            "team": self.team.to_dict(),
            "player": self.player.to_dict(),
            "assist": self.assist.to_dict(),
            "type": self.type,
            "detail": self.detail,
            "comments": self.comments,
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class FixtureEventList:
    fixture_id: int
    items: list[FixtureEvent] = field(default_factory=list)

    @classmethod
    def from_api(
        cls, data: dict[str, Any], fixture_id: int
    ) -> "FixtureEventList":
        return cls(
            fixture_id=fixture_id,
            items=[FixtureEvent.from_api(e) for e in data["response"]],
        )

    def __iter__(self) -> Iterator[FixtureEvent]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> FixtureEvent:
        return self.items[index]

    def _wrap(self, items: list[FixtureEvent]) -> "FixtureEventList":
        return FixtureEventList(fixture_id=self.fixture_id, items=items)

    def by_team(self, team_id: int) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.team.id == team_id])

    def by_type(self, event_type: str) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.type == event_type])

    def goals(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.is_goal])

    def cards(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.is_card])

    def yellow_cards(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.is_yellow_card])

    def red_cards(self) -> "FixtureEventList":
        return self._wrap(
            [e for e in self.items if e.is_red_card or e.is_second_yellow]
        )

    def substitutions(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.is_substitution])

    def var_decisions(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.is_var])

    def own_goals(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.is_own_goal])

    def penalties(self) -> "FixtureEventList":
        return self._wrap(
            [e for e in self.items if e.is_penalty_goal or e.is_missed_penalty]
        )

    def by_player(self, player_id: int) -> "FixtureEventList":
        return self._wrap(
            [
                e
                for e in self.items
                if e.player.id == player_id or e.assist.id == player_id
            ]
        )

    def in_first_half(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.time.elapsed <= 45])

    def in_second_half(self) -> "FixtureEventList":
        return self._wrap([e for e in self.items if 45 < e.time.elapsed <= 90])

    def after_minute(self, minute: int) -> "FixtureEventList":
        return self._wrap([e for e in self.items if e.time.elapsed >= minute])

    def goal_count_for(self, team_id: int) -> int:
        """Goals scored by a team — own goals counted for the opposing team."""
        count = 0
        for e in self.items:
            if not e.is_goal or e.is_missed_penalty:
                continue
            if e.is_own_goal:
                if e.team.id != team_id:
                    count += 1
            else:
                if e.team.id == team_id:
                    count += 1
        return count

    def scorers(self) -> list[tuple[str, str]]:
        result = []
        for e in self.goals():
            if e.is_missed_penalty:
                continue
            name = e.player.name or "Unknown"
            suffix = " (OG)" if e.is_own_goal else ""
            result.append((f"{name}{suffix}", e.minute))
        return result

    def to_list(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self.items]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)
