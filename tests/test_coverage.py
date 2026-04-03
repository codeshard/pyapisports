from pyapisports.football.models import Coverage, FixtureCoverage


class TestFixtureCoverage:
    def test_from_api(self, fixture_coverage_data):
        fc = FixtureCoverage.from_api(fixture_coverage_data)
        assert fc.events is True
        assert fc.lineups is True
        assert fc.statistics_fixtures is False
        assert fc.statistics_players is False

    def test_to_dict(self, fixture_coverage_data):
        c = FixtureCoverage.from_api(fixture_coverage_data)
        d = c.to_dict()
        assert d == {
            "events": True,
            "lineups": True,
            "statistics_fixtures": False,
            "statistics_players": False,
        }

    def test_to_json(self, fixture_coverage_data):
        c = FixtureCoverage.from_api(fixture_coverage_data)
        import json

        parsed = json.loads(c.to_json())
        assert parsed["events"] is True


class TestCoverage:
    def test_from_api(self, coverage_data):
        c = Coverage.from_api(coverage_data)
        assert c.fixtures == FixtureCoverage(
            events=True,
            lineups=True,
            statistics_fixtures=False,
            statistics_players=False,
        )
        assert c.standings is True
        assert c.players is True
        assert c.top_scorers is True
        assert c.top_assists is True
        assert c.top_cards is True
        assert c.predictions is True
        assert c.odds is False

    def test_to_dict(self, coverage_data):
        c = Coverage.from_api(coverage_data)
        d = c.to_dict()
        print(d)
        assert d == {
            "fixtures": {
                "events": True,
                "lineups": True,
                "statistics_fixtures": False,
                "statistics_players": False,
            },
            "standings": True,
            "players": True,
            "top_scorers": True,
            "top_assists": True,
            "top_cards": True,
            "injuries": True,
            "predictions": True,
            "odds": False,
        }

    def test_to_json(self, coverage_data):
        c = Coverage.from_api(coverage_data)
        import json

        parsed = json.loads(c.to_json())
        assert parsed["standings"] is True
