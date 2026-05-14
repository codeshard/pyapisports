import json

import pytest

from pyapisports.football.models.fixtures.events import (
    CardDetail,
    EventPlayer,
    EventTeam,
    EventTime,
    EventType,
    FixtureEvent,
    FixtureEventList,
    GoalDetail,
    VarDetail,
)


class TestEventTime:
    def test_from_api_without_extra(self):
        data = {"elapsed": 45, "extra": None}
        t = EventTime.from_api(data)
        assert t.elapsed == 45
        assert t.extra is None

    def test_from_api_with_extra(self):
        data = {"elapsed": 90, "extra": 5}
        t = EventTime.from_api(data)
        assert t.elapsed == 90
        assert t.extra == 5

    def test_display_without_extra(self):
        t = EventTime(elapsed=45, extra=None)
        assert t.display == "45"

    def test_display_with_extra(self):
        t = EventTime(elapsed=90, extra=5)
        assert t.display == "90+5"

    def test_to_dict(self):
        t = EventTime(elapsed=90, extra=5)
        assert t.to_dict() == {"elapsed": 90, "extra": 5}


class TestEventTeam:
    def test_from_api(self):
        data = {"id": 33, "name": "Man Utd", "logo": "https://x.png"}
        t = EventTeam.from_api(data)
        assert t.id == 33
        assert t.name == "Man Utd"
        assert t.logo == "https://x.png"

    def test_to_dict(self):
        t = EventTeam(id=33, name="Man Utd", logo="https://x.png")
        assert t.to_dict() == {
            "id": 33,
            "name": "Man Utd",
            "logo": "https://x.png",
        }


class TestEventPlayer:
    def test_from_api_with_data(self):
        data = {"id": 10, "name": "Marcus Rashford"}
        p = EventPlayer.from_api(data)
        assert p.id == 10
        assert p.name == "Marcus Rashford"

    def test_from_api_with_none(self):
        p = EventPlayer.from_api(None)
        assert p.id is None
        assert p.name is None

    def test_from_api_with_empty_dict(self):
        p = EventPlayer.from_api({})
        assert p.id is None
        assert p.name is None

    def test_to_dict(self):
        p = EventPlayer(id=10, name="Marcus Rashford")
        assert p.to_dict() == {"id": 10, "name": "Marcus Rashford"}


class TestFixtureEvent:
    @pytest.fixture
    def normal_goal(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 5, "extra": None},
                "team": {"id": 33, "name": "Man Utd", "logo": "https://x.png"},
                "player": {"id": 10, "name": "Marcus Rashford"},
                "assist": {"id": 7, "name": "Bruno Fernandes"},
                "type": "Goal",
                "detail": "Normal Goal",
                "comments": None,
            }
        )

    @pytest.fixture
    def own_goal(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 82, "extra": None},
                "team": {"id": 34, "name": "Spurs", "logo": "https://y.png"},
                "player": {"id": 4, "name": "Cristian Romero"},
                "assist": None,
                "type": "Goal",
                "detail": "Own Goal",
                "comments": None,
            }
        )

    @pytest.fixture
    def penalty(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 70, "extra": None},
                "team": {"id": 34, "name": "Spurs", "logo": "https://y.png"},
                "player": {"id": 9, "name": "Harry Kane"},
                "assist": None,
                "type": "Goal",
                "detail": "Penalty",
                "comments": None,
            }
        )

    @pytest.fixture
    def missed_penalty(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 75, "extra": None},
                "team": {"id": 33, "name": "Man Utd", "logo": "https://x.png"},
                "player": {"id": 10, "name": "Marcus Rashford"},
                "assist": None,
                "type": "Goal",
                "detail": "Missed Penalty",
                "comments": None,
            }
        )

    @pytest.fixture
    def yellow_card(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 35, "extra": None},
                "team": {"id": 33, "name": "Man Utd", "logo": "https://x.png"},
                "player": {"id": 10, "name": "Marcus Rashford"},
                "assist": None,
                "type": "Card",
                "detail": "Yellow Card",
                "comments": None,
            }
        )

    @pytest.fixture
    def red_card(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 55, "extra": None},
                "team": {"id": 33, "name": "Man Utd", "logo": "https://x.png"},
                "player": {"id": 5, "name": "Harry Maguire"},
                "assist": None,
                "type": "Card",
                "detail": "Red Card",
                "comments": None,
            }
        )

    @pytest.fixture
    def second_yellow(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 67, "extra": None},
                "team": {"id": 34, "name": "Spurs", "logo": "https://y.png"},
                "player": {"id": 4, "name": "Cristian Romero"},
                "assist": None,
                "type": "Card",
                "detail": "Yellow Red Card",
                "comments": None,
            }
        )

    @pytest.fixture
    def substitution(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 85, "extra": None},
                "team": {"id": 33, "name": "Man Utd", "logo": "https://x.png"},
                "player": None,
                "assist": None,
                "type": "subst",
                "detail": "Substitution 1",
                "comments": None,
            }
        )

    @pytest.fixture
    def var_event(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 90, "extra": None},
                "team": {"id": 34, "name": "Spurs", "logo": "https://y.png"},
                "player": None,
                "assist": None,
                "type": "Var",
                "detail": "Goal cancelled",
                "comments": "Offside",
            }
        )

    @pytest.fixture
    def injury_time_goal(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 90, "extra": 3},
                "team": {"id": 33, "name": "Man Utd", "logo": "https://x.png"},
                "player": {"id": 10, "name": "Marcus Rashford"},
                "assist": {"id": 7, "name": "Bruno Fernandes"},
                "type": "Goal",
                "detail": "Normal Goal",
                "comments": None,
            }
        )

    @pytest.fixture
    def normal_card(self):
        return FixtureEvent.from_api(
            {
                "time": {"elapsed": 42, "extra": None},
                "team": {"id": 34, "name": "Spurs", "logo": "https://y.png"},
                "player": None,
                "assist": None,
                "type": "Card",
                "detail": "Yellow Card",
                "comments": "Time wasting",
            }
        )

    def test_type_constants(self):
        assert EventType.GOAL == "Goal"
        assert EventType.CARD == "Card"
        assert EventType.SUBST == "subst"
        assert EventType.VAR == "Var"

    def test_goal_detail_constants(self):
        assert GoalDetail.NORMAL_GOAL == "Normal Goal"
        assert GoalDetail.OWN_GOAL == "Own Goal"
        assert GoalDetail.PENALTY == "Penalty"
        assert GoalDetail.MISSED_PENALTY == "Missed Penalty"

    def test_card_detail_constants(self):
        assert CardDetail.YELLOW_CARD == "Yellow Card"
        assert CardDetail.RED_CARD == "Red Card"
        assert CardDetail.YELLOW_RED_CARD == "Yellow Red Card"

    def test_var_detail_constants(self):
        assert VarDetail.GOAL_CANCELLED == "Goal cancelled"
        assert VarDetail.PENALTY_CONFIRMED == "Penalty confirmed"
        assert VarDetail.CARD_UPGRADE == "Card Upgrade"

    def test_is_goal_true(self, normal_goal):
        assert normal_goal.is_goal is True

    def test_is_goal_false(self, yellow_card):
        assert yellow_card.is_goal is False

    def test_is_own_goal_true(self, own_goal):
        assert own_goal.is_own_goal is True

    def test_is_own_goal_false(self, normal_goal):
        assert normal_goal.is_own_goal is False

    def test_is_penalty_goal_true(self, penalty):
        assert penalty.is_penalty_goal is True

    def test_is_penalty_goal_false(self, normal_goal):
        assert normal_goal.is_penalty_goal is False

    def test_is_missed_penalty_true(self, missed_penalty):
        assert missed_penalty.is_missed_penalty is True

    def test_is_missed_penalty_false(self, normal_goal):
        assert normal_goal.is_missed_penalty is False

    def test_is_card_true(self, yellow_card):
        assert yellow_card.is_card is True

    def test_is_card_false(self, normal_goal):
        assert normal_goal.is_card is False

    def test_is_yellow_card_true(self, yellow_card):
        assert yellow_card.is_yellow_card is True

    def test_is_yellow_card_false(self, red_card):
        assert red_card.is_yellow_card is False

    def test_is_red_card_true(self, red_card):
        assert red_card.is_red_card is True

    def test_is_red_card_false(self, yellow_card):
        assert yellow_card.is_red_card is False

    def test_is_second_yellow_true(self, second_yellow):
        assert second_yellow.is_second_yellow is True

    def test_is_second_yellow_false(self, yellow_card):
        assert yellow_card.is_second_yellow is False

    def test_is_substitution_true(self, substitution):
        assert substitution.is_substitution is True

    def test_is_substitution_false(self, normal_goal):
        assert normal_goal.is_substitution is False

    def test_is_var_true(self, var_event):
        assert var_event.is_var is True

    def test_is_var_false(self, normal_goal):
        assert normal_goal.is_var is False

    def test_minute_without_extra(self, normal_goal):
        assert normal_goal.minute == "5"

    def test_minute_with_extra(self, injury_time_goal):
        assert injury_time_goal.minute == "90+3"

    def test_to_dict(self, var_event):
        d = var_event.to_dict()
        assert d["type"] == "Var"
        assert d["detail"] == "Goal cancelled"
        assert d["time"]["elapsed"] == 90
        assert d["team"]["id"] == 34
        assert d["player"]["id"] is None
        assert d["assist"]["id"] is None
        assert d["comments"] == "Offside"

    def test_to_json(self, normal_goal):
        parsed = json.loads(normal_goal.to_json())
        assert parsed["type"] == "Goal"
        assert parsed["detail"] == "Normal Goal"

    def test_from_api_with_comments(self, normal_card):
        assert normal_card.comments == "Time wasting"
        assert normal_card.player.id is None
        assert normal_card.player.name is None


class TestFixtureEventList:
    @pytest.fixture
    def events(self, events_payload):
        return FixtureEventList.from_api(events_payload, fixture_id=215662)

    def test_from_api(self, events):
        assert events.fixture_id == 215662
        assert len(events) == 13

    def test_iter(self, events):
        assert [e.type for e in events].count("Goal") == 6

    def test_len(self, events):
        assert len(events) == 13

    def test_getitem(self, events):
        assert events[0].type == "Goal"
        assert events[0].team.id == 33

    def test_getitem_index_error(self, events):
        with pytest.raises(IndexError):
            events[100]

    def test_by_team(self, events):
        team_33 = events.by_team(33)
        assert len(team_33) == 6
        assert all(e.team.id == 33 for e in team_33)

    def test_by_type(self, events):
        goals = events.by_type("Goal")
        assert len(goals) == 6
        assert all(e.type == "Goal" for e in goals)

    def test_goals(self, events):
        goals = events.goals()
        assert len(goals) == 6

    def test_cards(self, events):
        cards = events.cards()
        assert len(cards) == 4

    def test_yellow_cards(self, events):
        yellows = events.yellow_cards()
        assert len(yellows) == 2

    def test_red_cards(self, events):
        reds = events.red_cards()
        assert len(reds) == 2

    def test_substitutions(self, events):
        subs = events.substitutions()
        assert len(subs) == 2

    def test_var_decisions(self, events):
        vars = events.var_decisions()
        assert len(vars) == 1
        assert vars[0].detail == "Goal cancelled"

    def test_own_goals(self, events):
        ogs = events.own_goals()
        assert len(ogs) == 1
        assert ogs[0].detail == "Own Goal"

    def test_penalties(self, events):
        pens = events.penalties()
        assert len(pens) == 2

    def test_by_player(self, events):
        rashford = events.by_player(10)
        assert len(rashford) == 4

    def test_by_player_assist(self, events):
        bruno = events.by_player(7)
        assert len(bruno) == 3

    def test_by_player_not_found(self, events):
        nobody = events.by_player(999)
        assert len(nobody) == 0

    def test_in_first_half(self, events):
        first = events.in_first_half()
        assert all(e.time.elapsed <= 45 for e in first)
        assert len(first) == 4

    def test_in_second_half(self, events):
        second = events.in_second_half()
        assert all(45 < e.time.elapsed <= 90 for e in second)
        assert len(second) == 9

    def test_after_minute(self, events):
        after_80 = events.after_minute(80)
        assert all(e.time.elapsed >= 80 for e in after_80)
        assert len(after_80) == 5

    def test_goal_count_for_team_33(self, events):
        assert events.goal_count_for(33) == 3

    def test_goal_count_for_team_34(self, events):
        assert events.goal_count_for(34) == 2

    def test_scorers(self, events):
        scorers = events.scorers()
        assert ("Marcus Rashford", "5") in scorers
        assert ("Harry Kane", "23") in scorers
        assert ("Harry Kane", "70") in scorers
        assert ("Cristian Romero (OG)", "82") in scorers
        assert ("Marcus Rashford", "90+3") in scorers
        assert len(scorers) == 5

    def test_to_list(self, events):
        lst = events.to_list()
        assert len(lst) == 13
        assert lst[0]["type"] == "Goal"
        assert lst[0]["time"]["elapsed"] == 5

    def test_to_json(self, events):
        parsed = json.loads(events.to_json())
        assert len(parsed) == 13
        assert parsed[0]["detail"] == "Normal Goal"

    def test_empty_events(self):
        empty_data = {"response": []}
        el = FixtureEventList.from_api(empty_data, fixture_id=100)
        assert len(el) == 0
        assert list(el) == []
        assert el.by_team(1).items == []
        assert el.goals().items == []

    def test_red_cards_includes_second_yellow(self, events):
        reds = events.red_cards()
        second_yellows = [e for e in events if e.is_second_yellow]
        for sy in second_yellows:
            assert sy in reds.items
