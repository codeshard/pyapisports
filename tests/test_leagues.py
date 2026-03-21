from pyapisports.models import League


class TestCountry:
    def test_from_api(self, league_data):
        league = League.from_api(league_data)
        assert league.id == 39
        assert league.name == "Premier League"

    def test_to_dict(self, league_data):
        c = League.from_api(league_data)
        d = c.to_dict()
        assert d == {
            "league": {
                "id": 39,
                "name": "Premier League",
                "type": "League",
                "logo": "https://media.api-sports.io/football/leagues/2.png",
            },
            "country": {
                "name": "England",
                "code": "GB",
                "flag": "https://media.api-sports.io/flags/gb.svg",
            },
            "seasons": [
                {
                    "year": 2010,
                    "start": "2010-08-14",
                    "end": "2011-05-17",
                    "current": False,
                    "coverage": {
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
                    },
                }
            ],
        }

    def test_to_json(self, league_data):
        c = League.from_api(league_data)
        import json

        parsed = json.loads(c.to_json())
        assert parsed["league"]["name"] == "Premier League"
