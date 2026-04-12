import json

from pyapisports.football.models.fixtures.rounds import RoundsList


class TestRoundsList:
    def test_from_api(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        assert rounds.rounds == [
            "1st Round",
            "2nd Round",
            "3rd Round",
            "4th Round",
            "5th Round",
            "6th Round",
        ]

    def test_iter(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        items = list(rounds)
        assert items == [
            "1st Round",
            "2nd Round",
            "3rd Round",
            "4th Round",
            "5th Round",
            "6th Round",
        ]

    def test_len(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        assert len(rounds) == 6

    def test_len_empty(self, rounds_empty_payload):
        rounds = RoundsList.from_api(rounds_empty_payload)
        assert len(rounds) == 0

    def test_contains(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        assert "1st Round" in rounds
        assert "Final" not in rounds

    def test_to_list(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        result = rounds.to_list()
        assert isinstance(result, list)
        assert result == [
            "1st Round",
            "2nd Round",
            "3rd Round",
            "4th Round",
            "5th Round",
            "6th Round",
        ]

    def test_to_json(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        parsed = json.loads(rounds.to_json())
        assert parsed == [
            "1st Round",
            "2nd Round",
            "3rd Round",
            "4th Round",
            "5th Round",
            "6th Round",
        ]

    def test_to_json_with_indent(self, rounds_payload):
        rounds = RoundsList.from_api(rounds_payload)
        json_str = rounds.to_json(indent=2)
        parsed = json.loads(json_str)
        assert parsed == [
            "1st Round",
            "2nd Round",
            "3rd Round",
            "4th Round",
            "5th Round",
            "6th Round",
        ]
