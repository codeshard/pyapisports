import json
from dataclasses import dataclass, field
from typing import Any, Iterator, Optional


@dataclass
class PlayerGames:
    minutes: Optional[int]
    number: Optional[int]
    position: Optional[str]
    rating: Optional[str]
    captain: bool
    substitute: bool

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerGames":
        if not data:
            return cls(
                minutes=None,
                number=None,
                position=None,
                rating=None,
                captain=False,
                substitute=False,
            )
        return cls(
            minutes=data.get("minutes"),
            number=data.get("number"),
            position=data.get("position"),
            rating=data.get("rating"),
            captain=data.get("captain") or False,
            substitute=data.get("substitute") or False,
        )

    @property
    def rating_float(self) -> Optional[float]:
        try:
            return float(self.rating) if self.rating else None
        except ValueError:
            return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "minutes": self.minutes,
            "number": self.number,
            "position": self.position,
            "rating": self.rating,
            "captain": self.captain,
            "substitute": self.substitute,
        }


@dataclass
class PlayerShots:
    total: Optional[int]
    on: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerShots":
        if not data:
            return cls(total=None, on=None)
        return cls(total=data.get("total"), on=data.get("on"))

    def to_dict(self) -> dict[str, Any]:
        return {"total": self.total, "on": self.on}


@dataclass
class PlayerGoals:
    total: Optional[int]
    conceded: Optional[int]
    assists: Optional[int]
    saves: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerGoals":
        if not data:
            return cls(total=None, conceded=None, assists=None, saves=None)
        return cls(
            total=data.get("total"),
            conceded=data.get("conceded"),
            assists=data.get("assists"),
            saves=data.get("saves"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "conceded": self.conceded,
            "assists": self.assists,
            "saves": self.saves,
        }


@dataclass
class PlayerPasses:
    total: Optional[int]
    key: Optional[int]
    accuracy: Optional[str]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerPasses":
        if not data:
            return cls(total=None, key=None, accuracy=None)
        return cls(
            total=data.get("total"),
            key=data.get("key"),
            accuracy=data.get("accuracy"),
        )

    @property
    def accuracy_int(self) -> Optional[int]:
        if not self.accuracy:
            return None
        try:
            return int(str(self.accuracy).replace("%", "").strip())
        except ValueError:
            return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "key": self.key,
            "accuracy": self.accuracy,
        }


@dataclass
class PlayerTackles:
    total: Optional[int]
    blocks: Optional[int]
    interceptions: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerTackles":
        if not data:
            return cls(total=None, blocks=None, interceptions=None)
        return cls(
            total=data.get("total"),
            blocks=data.get("blocks"),
            interceptions=data.get("interceptions"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "blocks": self.blocks,
            "interceptions": self.interceptions,
        }


@dataclass
class PlayerDribbles:
    attempts: Optional[int]
    success: Optional[int]
    past: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerDribbles":
        if not data:
            return cls(attempts=None, success=None, past=None)
        return cls(
            attempts=data.get("attempts"),
            success=data.get("success"),
            past=data.get("past"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempts": self.attempts,
            "success": self.success,
            "past": self.past,
        }


@dataclass
class PlayerFouls:
    drawn: Optional[int]
    committed: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerFouls":
        if not data:
            return cls(drawn=None, committed=None)
        return cls(drawn=data.get("drawn"), committed=data.get("committed"))

    def to_dict(self) -> dict[str, Any]:
        return {"drawn": self.drawn, "committed": self.committed}


@dataclass
class PlayerCards:
    yellow: Optional[int]
    red: Optional[int]

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerCards":
        if not data:
            return cls(yellow=None, red=None)
        return cls(yellow=data.get("yellow"), red=data.get("red"))

    def to_dict(self) -> dict[str, Any]:
        return {"yellow": self.yellow, "red": self.red}


@dataclass
class PlayerPenalty:
    won: Optional[int]
    committed: Optional[int]
    scored: Optional[int]
    missed: Optional[int]
    saved: Optional[int]  # GK only

    @classmethod
    def from_api(cls, data: Optional[dict[str, Any]]) -> "PlayerPenalty":
        if not data:
            return cls(
                won=None,
                committed=None,
                scored=None,
                missed=None,
                saved=None,
            )
        return cls(
            won=data.get("won"),
            committed=data.get("commited"),
            scored=data.get("scored"),
            missed=data.get("missed"),
            saved=data.get("saved"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "won": self.won,
            "commited": self.committed,
            "scored": self.scored,
            "missed": self.missed,
            "saved": self.saved,
        }


@dataclass
class PlayerMatchStats:
    games: PlayerGames
    offsides: Optional[int]
    shots: PlayerShots
    goals: PlayerGoals
    passes: PlayerPasses
    tackles: PlayerTackles
    dribbles: PlayerDribbles
    fouls: PlayerFouls
    cards: PlayerCards
    penalty: PlayerPenalty

    @classmethod
    def from_api(cls, data: list[dict[str, Any]]) -> "PlayerMatchStats":
        """data is the 'statistics' array — always a single-element list."""
        s = data[0] if data else {}
        return cls(
            games=PlayerGames.from_api(s.get("games")),
            offsides=s.get("offsides"),
            shots=PlayerShots.from_api(s.get("shots")),
            goals=PlayerGoals.from_api(s.get("goals")),
            passes=PlayerPasses.from_api(s.get("passes")),
            tackles=PlayerTackles.from_api(s.get("tackles")),
            dribbles=PlayerDribbles.from_api(s.get("dribbles")),
            fouls=PlayerFouls.from_api(s.get("fouls")),
            cards=PlayerCards.from_api(s.get("cards")),
            penalty=PlayerPenalty.from_api(s.get("penalty")),
        )

    @property
    def rating(self) -> Optional[float]:
        return self.games.rating_float

    @property
    def minutes_played(self) -> Optional[int]:
        return self.games.minutes

    @property
    def is_captain(self) -> bool:
        return self.games.captain

    @property
    def is_substitute(self) -> bool:
        return self.games.substitute

    def to_dict(self) -> dict[str, Any]:
        return {
            "games": self.games.to_dict(),
            "offsides": self.offsides,
            "shots": self.shots.to_dict(),
            "goals": self.goals.to_dict(),
            "passes": self.passes.to_dict(),
            "tackles": self.tackles.to_dict(),
            "dribbles": self.dribbles.to_dict(),
            "fouls": self.fouls.to_dict(),
            "cards": self.cards.to_dict(),
            "penalty": self.penalty.to_dict(),
        }


@dataclass
class FixturePlayer:
    id: int
    name: str
    photo: str
    stats: PlayerMatchStats

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "FixturePlayer":
        return cls(
            id=data["player"]["id"],
            name=data["player"]["name"],
            photo=data["player"]["photo"],
            stats=PlayerMatchStats.from_api(data.get("statistics", [])),
        )

    @property
    def rating(self) -> Optional[float]:
        return self.stats.rating

    @property
    def minutes_played(self) -> Optional[int]:
        return self.stats.minutes_played

    @property
    def position(self) -> Optional[str]:
        return self.stats.games.position

    @property
    def is_captain(self) -> bool:
        return self.stats.is_captain

    @property
    def is_substitute(self) -> bool:
        return self.stats.is_substitute

    @property
    def goals(self) -> Optional[int]:
        return self.stats.goals.total

    @property
    def assists(self) -> Optional[int]:
        return self.stats.goals.assists

    def to_dict(self) -> dict[str, Any]:
        return {
            "player": {
                "id": self.id,
                "name": self.name,
                "photo": self.photo,
            },
            "statistics": [self.stats.to_dict()],
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class TeamFixturePlayers:
    team_id: int
    team_name: str
    team_logo: str
    players: list[FixturePlayer] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "TeamFixturePlayers":
        return cls(
            team_id=data["team"]["id"],
            team_name=data["team"]["name"],
            team_logo=data["team"]["logo"],
            players=[
                FixturePlayer.from_api(p) for p in data.get("players", [])
            ],
        )

    def __iter__(self) -> Iterator[FixturePlayer]:
        return iter(self.players)

    def __len__(self) -> int:
        return len(self.players)

    def __getitem__(self, index: int) -> FixturePlayer:
        return self.players[index]

    def find_by_id(self, player_id: int) -> Optional[FixturePlayer]:
        return next((p for p in self.players if p.id == player_id), None)

    def find_by_name(self, name: str) -> Optional[FixturePlayer]:
        name = name.lower()
        return next((p for p in self.players if p.name.lower() == name), None)

    def starters(self) -> list[FixturePlayer]:
        return [p for p in self.players if not p.is_substitute]

    def substitutes(self) -> list[FixturePlayer]:
        return [p for p in self.players if p.is_substitute]

    def by_position(self, position: str) -> list[FixturePlayer]:
        return [p for p in self.players if p.position == position]

    def sorted_by_rating(self, descending: bool = True) -> list[FixturePlayer]:
        return sorted(
            [p for p in self.players if p.rating is not None],
            key=lambda p: p.rating,  # type: ignore
            reverse=descending,
        )

    @property
    def top_rated(self) -> Optional[FixturePlayer]:
        rated = self.sorted_by_rating()
        return rated[0] if rated else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "team": {
                "id": self.team_id,
                "name": self.team_name,
                "logo": self.team_logo,
            },
            "players": [p.to_dict() for p in self.players],
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)


@dataclass
class FixturePlayers:
    fixture_id: int
    home: TeamFixturePlayers
    away: TeamFixturePlayers
    available: bool = True

    @classmethod
    def empty(cls, fixture_id: int) -> "FixturePlayers":
        placeholder = TeamFixturePlayers(team_id=0, team_name="", team_logo="")
        return cls(
            fixture_id=fixture_id,
            home=placeholder,
            away=placeholder,
            available=False,
        )

    @classmethod
    def from_api(
        cls, data: dict[str, Any], fixture_id: int
    ) -> "FixturePlayers":
        response = data["response"]
        if not response:
            return cls.empty(fixture_id)
        teams = [TeamFixturePlayers.from_api(t) for t in response]
        home = teams[0]
        away = (
            teams[1]
            if len(teams) > 1
            else TeamFixturePlayers(team_id=0, team_name="", team_logo="")
        )
        return cls(fixture_id=fixture_id, home=home, away=away)

    def for_team(self, team_id: int) -> Optional[TeamFixturePlayers]:
        if self.home.team_id == team_id:
            return self.home
        if self.away.team_id == team_id:
            return self.away
        return None

    def find_player(
        self, player_id: int
    ) -> Optional[tuple[TeamFixturePlayers, FixturePlayer]]:
        for team in (self.home, self.away):
            player = team.find_by_id(player_id)
            if player:
                return team, player
        return None

    def all_players(self) -> list[FixturePlayer]:
        return self.home.players + self.away.players

    def top_rated(self, n: int = 3) -> list[FixturePlayer]:
        rated = [p for p in self.all_players() if p.rating is not None]
        return sorted(rated, key=lambda p: p.rating, reverse=True)[:n]  # type: ignore

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "home": self.home.to_dict(),
            "away": self.away.to_dict(),
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
