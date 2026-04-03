from pyapisports.football.models import Venue


class TestVenue:
    def test_from_api(self, venue_data):
        venue = Venue.from_api(venue_data)
        assert venue.id == 556
        assert venue.name == "Old Trafford"

    def test_to_dict(self, venue_data):
        c = Venue.from_api(venue_data)
        d = c.to_dict()
        assert d == {
            "id": 556,
            "name": "Old Trafford",
            "address": "Sir Matt Busby Way",
            "city": "Manchester",
            "country": "England",
            "capacity": 76212,
            "surface": "grass",
            "image": "https://media.api-sports.io/football/venues/556.png",
        }

    def test_to_json(self, venue_data):
        c = Venue.from_api(venue_data)
        import json

        parsed = json.loads(c.to_json())
        assert parsed["name"] == "Old Trafford"
