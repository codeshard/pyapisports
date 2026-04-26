import json
from dataclasses import dataclass
from typing import Any, Iterator

from .fixtures import Fixture, FixtureList


@dataclass
class HeadToHead:
    team_a_id: int
    team_b_id: int
    fixtures: FixtureList

    @classmethod
    def from_api(
        cls,
        data: dict[str, Any],
        team_a_id: int,
        team_b_id: int,
    ) -> "HeadToHead":
        return cls(
            team_a_id=team_a_id,
            team_b_id=team_b_id,
            fixtures=FixtureList.from_api(data),
        )

    def __iter__(self) -> Iterator[Fixture]:
        return iter(self.fixtures)

    def __len__(self) -> int:
        return len(self.fixtures)

    def __getitem__(self, index: int) -> Fixture:
        return self.fixtures[index]

    @property
    def finished(self) -> "HeadToHead":
        return self._wrap(self.fixtures.finished())

    @property
    def total_played(self) -> int:
        return len(self.fixtures.finished())

    def wins_for(self, team_id: int) -> int:
        return sum(
            1
            for f in self.fixtures.finished()
            if f.winner and f.winner.id == team_id
        )

    def draws(self) -> int:
        return sum(
            1
            for f in self.fixtures.finished()
            if f.is_finished and f.winner is None
        )

    def goals_for(self, team_id: int) -> int:
        total = 0
        for f in self.fixtures.finished():
            if f.home_team.id == team_id and f.goals_home is not None:
                total += f.goals_home
            elif f.away_team.id == team_id and f.goals_away is not None:
                total += f.goals_away
        return total

    def last(self, n: int) -> "HeadToHead":
        sorted_fixtures = sorted(
            self.fixtures.items,
            key=lambda f: f.timestamp,
            reverse=True,
        )
        return self._wrap(FixtureList(items=sorted_fixtures[:n]))

    def in_league(self, league_id: int) -> "HeadToHead":
        return self._wrap(
            FixtureList(
                items=[f for f in self.fixtures if f.league.id == league_id]
            )
        )

    def summary(self) -> dict[str, Any]:
        return {
            "team_a_id": self.team_a_id,
            "team_b_id": self.team_b_id,
            "played": self.total_played,
            "team_a_wins": self.wins_for(self.team_a_id),
            "team_b_wins": self.wins_for(self.team_b_id),
            "draws": self.draws(),
            "team_a_goals": self.goals_for(self.team_a_id),
            "team_b_goals": self.goals_for(self.team_b_id),
        }

    def to_list(self) -> list[dict[str, Any]]:
        return self.fixtures.to_list()

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_list(), **kwargs)

    def _wrap(self, fixture_list: FixtureList) -> "HeadToHead":
        return HeadToHead(
            team_a_id=self.team_a_id,
            team_b_id=self.team_b_id,
            fixtures=fixture_list,
        )
