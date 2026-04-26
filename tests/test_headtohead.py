import json

import pytest


class TestHeadToHead:
    @pytest.fixture
    def h2h(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        return football.get_head_to_head(team_a=33, team_b=34)

    def test_from_api(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        h2h = football.get_head_to_head(team_a=33, team_b=34)
        assert h2h.team_a_id == 33
        assert h2h.team_b_id == 34
        assert len(h2h.fixtures) == 4

    def test_iter(self, h2h):
        fixtures = list(h2h)
        assert len(fixtures) == 4
        assert fixtures[0].id == 868078

    def test_len(self, h2h):
        assert len(h2h) == 4

    def test_getitem(self, h2h):
        assert h2h[0].id == 868078
        assert h2h[-1].id == 868079

    def test_finished_property(self, h2h):
        finished = h2h.finished
        assert len(finished) == 3

    def test_total_played(self, h2h):
        assert h2h.total_played == 3

    def test_wins_for_team_a(self, h2h):
        assert h2h.wins_for(33) == 1

    def test_wins_for_team_b(self, h2h):
        assert h2h.wins_for(34) == 1

    def test_wins_for_no_wins(self, h2h):
        assert h2h.wins_for(99) == 0

    def test_draws(self, h2h):
        assert h2h.draws() == 1

    def test_goals_for_team_a_home(self, h2h):
        assert h2h.goals_for(33) == 3

    def test_goals_for_team_b_away(self, h2h):
        assert h2h.goals_for(34) == 5

    def test_goals_for_no_goals(self, h2h):
        assert h2h.goals_for(99) == 0

    def test_last_n(self, h2h):
        last_two = h2h.last(2)
        assert len(last_two) == 2

    def test_in_league(self, h2h):
        filtered = h2h.in_league(39)
        assert len(filtered) == 4

    def test_in_league_not_found(self, h2h):
        filtered = h2h.in_league(999)
        assert len(filtered) == 0

    def test_summary(self, h2h):
        summary = h2h.summary()
        assert summary["team_a_id"] == 33
        assert summary["team_b_id"] == 34
        assert summary["played"] == 3
        assert summary["team_a_wins"] == 1
        assert summary["team_b_wins"] == 1
        assert summary["draws"] == 1

    def test_to_list(self, h2h):
        result = h2h.to_list()
        assert isinstance(result, list)
        assert len(result) == 4

    def test_to_json(self, h2h):
        result = h2h.to_json()
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) == 4


class TestGetHeadToHead:
    def test_passes_team_ids(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34)
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead", params={"h2h": "33-34"}
        )

    def test_passes_date(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, date="2024-12-01")
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead",
            params={"h2h": "33-34", "date": "2024-12-01"},
        )

    def test_passes_league(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, league=39)
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead", params={"h2h": "33-34", "league": 39}
        )

    def test_passes_season(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, season=2024)
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead", params={"h2h": "33-34", "season": 2024}
        )

    def test_passes_status(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, status="FT")
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead", params={"h2h": "33-34", "status": "FT"}
        )

    def test_passes_from_date(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, from_date="2024-01-01")
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead",
            params={"h2h": "33-34", "from": "2024-01-01"},
        )

    def test_passes_to_date(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, to_date="2024-12-31")
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead",
            params={"h2h": "33-34", "to": "2024-12-31"},
        )

    def test_passes_last(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, last=5)
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead", params={"h2h": "33-34", "last": 5}
        )

    def test_passes_next(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(team_a=33, team_b=34, next=5)
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead", params={"h2h": "33-34", "next": 5}
        )

    def test_passes_timezone(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(
            team_a=33, team_b=34, timezone="America/New_York"
        )
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead",
            params={"h2h": "33-34", "timezone": "America/New_York"},
        )

    def test_passes_all_params(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        football.get_head_to_head(
            team_a=33,
            team_b=34,
            date="2024-12-01",
            league=39,
            season=2024,
            status="FT",
            from_date="2024-01-01",
            to_date="2024-12-31",
            last=5,
            next=5,
            timezone="UTC",
        )
        mock_client._get.assert_called_once_with(
            "/fixtures/headtohead",
            params={
                "h2h": "33-34",
                "date": "2024-12-01",
                "league": 39,
                "season": 2024,
                "status": "FT",
                "from": "2024-01-01",
                "to": "2024-12-31",
                "last": 5,
                "next": 5,
                "timezone": "UTC",
            },
        )

    def test_returns_head_to_head(self, football, mock_client, h2h_payload):
        mock_client._get.return_value = h2h_payload
        result = football.get_head_to_head(team_a=33, team_b=34)
        assert result is not None
        assert result.team_a_id == 33
        assert result.team_b_id == 34
        assert len(result.fixtures) == 4
