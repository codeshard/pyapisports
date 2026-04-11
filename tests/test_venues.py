import json

import pytest

from pyapisports.football.models import Venue, VenueList


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


class TestVenueList:
    def test_find_by_id(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        venue = venues.find_by_id(556)
        assert venue is not None
        assert venue.name == "Old Trafford"

    def test_find_by_id_not_found(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        assert venues.find_by_id(999) is None

    def test_find_by_name(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        venue = venues.find_by_name("Old Trafford")
        assert venue is not None
        assert venue.id == 556

    def test_find_by_name_case_insensitive(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        assert venues.find_by_name("old trafford") == venues.find_by_name(
            "Old Trafford"
        )

    def test_find_by_name_not_found(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        assert venues.find_by_name("Nonexistent") is None

    def test_find_by_city(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        venue = venues.find_by_city("Manchester")
        assert venue is not None
        assert venue.name == "Old Trafford"

    def test_find_by_city_not_found(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        assert venues.find_by_city("London") is None

    def test_find_by_country(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        venue = venues.find_by_country("england")
        assert venue is not None
        assert venue.name == "Old Trafford"

    def test_find_by_country_not_found(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        assert venues.find_by_country("Spain") is None

    def test_filter_by_param(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        result = venues.filter_by_param("Old Trafford")
        assert len(result) == 1
        assert result[0].name == "Old Trafford"

    def test_to_list(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        result = venues.to_list()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "Old Trafford"

    def test_to_json(self, venues_payload):
        venues = VenueList.from_api(venues_payload)
        parsed = json.loads(venues.to_json())
        assert isinstance(parsed, list)
        assert len(parsed) == 1
