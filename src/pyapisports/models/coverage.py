from dataclasses import dataclass
from typing import Any


@dataclass
class FixtureCoverage:
    events: bool
    lineups: bool
    statistics_fixtures: bool
    statistics_players: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixtureCoverage":
        return cls(
            events=data["events"],
            lineups=data["lineups"],
            statistics_fixtures=data["statistics_fixtures"],
            statistics_players=data["statistics_players"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "events": self.events,
            "lineups": self.lineups,
            "statistics_fixtures": self.statistics_fixtures,
            "statistics_players": self.statistics_players,
        }


@dataclass
class Coverage:
    fixtures: FixtureCoverage
    standings: bool
    players: bool
    top_scorers: bool
    top_assists: bool
    top_cards: bool
    injuries: bool
    predictions: bool
    odds: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Coverage":
        return cls(
            fixtures=FixtureCoverage.from_api(data["fixtures"]),
            standings=data["standings"],
            players=data["players"],
            top_scorers=data["top_scorers"],
            top_assists=data["top_assists"],
            top_cards=data["top_cards"],
            injuries=data["injuries"],
            predictions=data["predictions"],
            odds=data["odds"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixtures": self.fixtures.to_dict(),
            "standings": self.standings,
            "players": self.players,
            "top_scorers": self.top_scorers,
            "top_assists": self.top_assists,
            "top_cards": self.top_cards,
            "injuries": self.injuries,
            "predictions": self.predictions,
            "odds": self.odds,
        }
