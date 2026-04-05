from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class HomeAwayTotal:
    home: Optional[int]
    away: Optional[int]
    total: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "HomeAwayTotal":
        if not data:
            return cls(home=None, away=None, total=None)
        return cls(
            home=data.get("home"),
            away=data.get("away"),
            total=data.get("total"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"home": self.home, "away": self.away, "total": self.total}


@dataclass
class HomeAwayTotalStr:
    home: Optional[str]
    away: Optional[str]
    total: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "HomeAwayTotalStr":
        if not data:
            return cls(home=None, away=None, total=None)
        return cls(
            home=data.get("home"),
            away=data.get("away"),
            total=data.get("total"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"home": self.home, "away": self.away, "total": self.total}


@dataclass
class FixturesStats:
    played: HomeAwayTotal
    wins: HomeAwayTotal
    draws: HomeAwayTotal
    loses: HomeAwayTotal

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixturesStats":
        return cls(
            played=HomeAwayTotal.from_api(data.get("played")),
            wins=HomeAwayTotal.from_api(data.get("wins")),
            draws=HomeAwayTotal.from_api(data.get("draws")),
            loses=HomeAwayTotal.from_api(data.get("loses")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "played": self.played.to_dict(),
            "wins": self.wins.to_dict(),
            "draws": self.draws.to_dict(),
            "loses": self.loses.to_dict(),
        }


@dataclass
class GoalMinuteSlot:
    """Goals scored/conceded in a specific minute range."""

    total: Optional[int]
    percentage: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "GoalMinuteSlot":
        if not data:
            return cls(total=None, percentage=None)
        return cls(
            total=data.get("total"),
            percentage=data.get("percentage"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"total": self.total, "percentage": self.percentage}


@dataclass
class GoalMinuteBreakdown:
    """Goals distributed across 15-minute intervals."""

    slot_0_15: GoalMinuteSlot
    slot_16_30: GoalMinuteSlot
    slot_31_45: GoalMinuteSlot
    slot_46_60: GoalMinuteSlot
    slot_61_75: GoalMinuteSlot
    slot_76_90: GoalMinuteSlot
    slot_91_105: GoalMinuteSlot
    slot_106_120: GoalMinuteSlot

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "GoalMinuteBreakdown":
        return cls(
            slot_0_15=GoalMinuteSlot.from_api(data.get("0-15")),
            slot_16_30=GoalMinuteSlot.from_api(data.get("16-30")),
            slot_31_45=GoalMinuteSlot.from_api(data.get("31-45")),
            slot_46_60=GoalMinuteSlot.from_api(data.get("46-60")),
            slot_61_75=GoalMinuteSlot.from_api(data.get("61-75")),
            slot_76_90=GoalMinuteSlot.from_api(data.get("76-90")),
            slot_91_105=GoalMinuteSlot.from_api(data.get("91-105")),
            slot_106_120=GoalMinuteSlot.from_api(data.get("106-120")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "0-15": self.slot_0_15.to_dict(),
            "16-30": self.slot_16_30.to_dict(),
            "31-45": self.slot_31_45.to_dict(),
            "46-60": self.slot_46_60.to_dict(),
            "61-75": self.slot_61_75.to_dict(),
            "76-90": self.slot_76_90.to_dict(),
            "91-105": self.slot_91_105.to_dict(),
            "106-120": self.slot_106_120.to_dict(),
        }


@dataclass
class GoalsStats:
    scored: HomeAwayTotal
    conceded: HomeAwayTotal
    average_scored: HomeAwayTotalStr
    average_conceded: HomeAwayTotalStr
    minute_breakdown: GoalMinuteBreakdown

    @classmethod
    def from_api(
        cls, goals: dict[str, Any], average: dict[str, Any]
    ) -> "GoalsStats":
        return cls(
            scored=HomeAwayTotal.from_api(goals.get("for", {}).get("total")),
            conceded=HomeAwayTotal.from_api(
                goals.get("against", {}).get("total")
            ),
            average_scored=HomeAwayTotalStr.from_api(
                goals.get("for", {}).get("average")
            ),
            average_conceded=HomeAwayTotalStr.from_api(
                goals.get("against", {}).get("average")
            ),
            minute_breakdown=GoalMinuteBreakdown.from_api(
                goals.get("for", {}).get("minute", {})
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "scored": self.scored.to_dict(),
            "conceded": self.conceded.to_dict(),
            "average_scored": self.average_scored.to_dict(),
            "average_conceded": self.average_conceded.to_dict(),
            "minute_breakdown": self.minute_breakdown.to_dict(),
        }


@dataclass
class BiggestScoreline:
    home: Optional[str]
    away: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "BiggestScoreline":
        if not data:
            return cls(home=None, away=None)
        return cls(home=data.get("home"), away=data.get("away"))

    def to_dict(self) -> dict[str, Any]:
        return {"home": self.home, "away": self.away}


@dataclass
class Biggest:
    streak_wins: Optional[int]
    streak_draws: Optional[int]
    streak_loses: Optional[int]
    wins: BiggestScoreline
    loses: BiggestScoreline
    goals_scored: HomeAwayTotal
    goals_conceded: HomeAwayTotal

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Biggest":
        streak = data.get("streak", {})
        return cls(
            streak_wins=streak.get("wins"),
            streak_draws=streak.get("draws"),
            streak_loses=streak.get("loses"),
            wins=BiggestScoreline.from_api(data.get("wins")),
            loses=BiggestScoreline.from_api(data.get("loses")),
            goals_scored=HomeAwayTotal.from_api(
                data.get("goals", {}).get("for")
            ),
            goals_conceded=HomeAwayTotal.from_api(
                data.get("goals", {}).get("against")
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "streak": {
                "wins": self.streak_wins,
                "draws": self.streak_draws,
                "loses": self.streak_loses,
            },
            "wins": self.wins.to_dict(),
            "loses": self.loses.to_dict(),
            "goals": {
                "for": self.goals_scored.to_dict(),
                "against": self.goals_conceded.to_dict(),
            },
        }


@dataclass
class CleanSheet:
    home: Optional[int]
    away: Optional[int]
    total: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "CleanSheet":
        if not data:
            return cls(home=None, away=None, total=None)
        return cls(
            home=data.get("home"),
            away=data.get("away"),
            total=data.get("total"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"home": self.home, "away": self.away, "total": self.total}


@dataclass
class PenaltyStat:
    total: Optional[int]
    percentage: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PenaltyStat":
        if not data:
            return cls(total=None, percentage=None)
        return cls(
            total=data.get("total"),
            percentage=data.get("percentage"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"total": self.total, "percentage": self.percentage}


@dataclass
class PenaltyStats:
    scored: PenaltyStat
    missed: PenaltyStat
    total: Optional[int]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "PenaltyStats":
        return cls(
            scored=PenaltyStat.from_api(data.get("scored")),
            missed=PenaltyStat.from_api(data.get("missed")),
            total=data.get("total"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "scored": self.scored.to_dict(),
            "missed": self.missed.to_dict(),
        }


@dataclass
class CardStats:
    yellow: GoalMinuteBreakdown
    red: GoalMinuteBreakdown

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "CardStats":
        return cls(
            yellow=GoalMinuteBreakdown.from_api(data.get("yellow", {})),
            red=GoalMinuteBreakdown.from_api(data.get("red", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "yellow": self.yellow.to_dict(),
            "red": self.red.to_dict(),
        }


@dataclass
class LineupEntry:
    formation: str
    played: int

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "LineupEntry":
        return cls(
            formation=data["formation"],
            played=data["played"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {"formation": self.formation, "played": self.played}


@dataclass
class TeamStatistics:
    league_id: int
    league_name: str
    league_country: str
    league_logo: str
    league_flag: Optional[str]
    league_season: int
    team_id: int
    team_name: str
    team_logo: str
    form: Optional[str]
    fixtures: FixturesStats
    goals: GoalsStats
    biggest: Biggest
    clean_sheet: CleanSheet
    failed_to_score: CleanSheet  # same shape as clean_sheet
    penalty: PenaltyStats
    lineups: list[LineupEntry]
    cards: CardStats

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamStatistics":
        r = data["response"]
        league = r["league"]
        team = r["team"]
        return cls(
            league_id=league["id"],
            league_name=league["name"],
            league_country=league["country"],
            league_logo=league["logo"],
            league_flag=league.get("flag"),
            league_season=league["season"],
            team_id=team["id"],
            team_name=team["name"],
            team_logo=team["logo"],
            form=r.get("form"),
            fixtures=FixturesStats.from_api(r["fixtures"]),
            goals=GoalsStats.from_api(r["goals"], r.get("average", {})),
            biggest=Biggest.from_api(r["biggest"]),
            clean_sheet=CleanSheet.from_api(r.get("clean_sheet")),
            failed_to_score=CleanSheet.from_api(r.get("failed_to_score")),
            penalty=PenaltyStats.from_api(r["penalty"]),
            lineups=[
                LineupEntry.from_api(lineup) for lineup in r.get("lineups", [])
            ],
            cards=CardStats.from_api(r["cards"]),
        )

    @property
    def win_rate(self) -> Optional[float]:
        played = self.fixtures.played.total
        wins = self.fixtures.wins.total
        if not played or wins is None:
            return None
        return round(wins / played * 100, 1)

    @property
    def most_used_formation(self) -> Optional[str]:
        if not self.lineups:
            return None
        return max(self.lineups, key=lambda lineup: lineup.played).formation

    @property
    def current_form(self) -> list[str]:
        """Returns form as a list e.g. ['W', 'W', 'D', 'L', 'W']"""
        if not self.form:
            return []
        return list(self.form)

    def to_dict(self) -> dict[str, Any]:
        return {
            "league": {
                "id": self.league_id,
                "name": self.league_name,
                "country": self.league_country,
                "logo": self.league_logo,
                "flag": self.league_flag,
                "season": self.league_season,
            },
            "team": {
                "id": self.team_id,
                "name": self.team_name,
                "logo": self.team_logo,
            },
            "form": self.form,
            "fixtures": self.fixtures.to_dict(),
            "goals": self.goals.to_dict(),
            "biggest": self.biggest.to_dict(),
            "clean_sheet": self.clean_sheet.to_dict(),
            "failed_to_score": self.failed_to_score.to_dict(),
            "penalty": self.penalty.to_dict(),
            "lineups": [lineup.to_dict() for lineup in self.lineups],
            "cards": self.cards.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
