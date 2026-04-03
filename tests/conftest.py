from unittest.mock import MagicMock

import pytest

from pyapisports.football.resources import FootballResource


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def football(mock_client):
    return FootballResource(mock_client)


@pytest.fixture
def country_data():
    return {
        "name": "England",
        "code": "GB",
        "flag": "https://flag.example.com/gb.svg",
    }


@pytest.fixture
def country_list_data():
    return {
        "response": [
            {
                "name": "England",
                "code": "GB",
                "flag": "https://flag.example.com/gb.svg",
            },
            {
                "name": "France",
                "code": "FR",
                "flag": "https://flag.example.com/fr.svg",
            },
            {"name": "Germany", "code": "DE", "flag": None},
        ]
    }


@pytest.fixture
def status_data():
    return {
        "response": {
            "account": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@example.com",
            },
            "subscription": {
                "plan": "Free",
                "end": "2025-12-31T00:00:00",
                "active": True,
            },
            "requests": {
                "current": 50,
                "limit_day": 100,
            },
        }
    }


@pytest.fixture
def timezone_data():
    return {
        "response": [
            "Africa/Abidjan",
            "America/New_York",
            "Europe/London",
            "Asia/Tokyo",
        ]
    }


@pytest.fixture
def fixture_coverage_data():
    return {
        "events": True,
        "lineups": True,
        "statistics_fixtures": False,
        "statistics_players": False,
    }


@pytest.fixture
def coverage_data():
    return {
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


@pytest.fixture
def league_data():
    return {
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


@pytest.fixture
def seasons_list_data():
    return {
        "response": [
            2008,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
        ]
    }


@pytest.fixture
def countries_payload():
    return {
        "get": "countries",
        "parameters": {"name": "England"},
        "errors": [],
        "results": 3,
        "response": [
            {
                "name": "England",
                "code": "GB",
                "flag": "https://media.api-sports.io/flags/gb.svg",
            },
            {
                "name": "France",
                "code": "FR",
                "flag": "https://media.api-sports.io/flags/fr.svg",
            },
            {"name": "Kosovo", "code": None, "flag": None},
        ],
    }


@pytest.fixture
def seasons_payload():
    return {
        "get": "leagues/seasons",
        "parameters": [],
        "errors": [],
        "results": 5,
        "response": [2015, 2016, 2017, 2018, 2019],
    }


@pytest.fixture
def leagues_payload():
    return {
        "get": "leagues",
        "parameters": {"id": "39"},
        "errors": [],
        "results": 1,
        "paging": {"current": 1, "total": 1},
        "response": [
            {
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
                        "year": 2018,
                        "start": "2018-08-10",
                        "end": "2019-05-12",
                        "current": False,
                        "coverage": {
                            "fixtures": {
                                "events": True,
                                "lineups": True,
                                "statistics_fixtures": True,
                                "statistics_players": True,
                            },
                            "standings": True,
                            "players": True,
                            "top_scorers": True,
                            "top_assists": True,
                            "top_cards": True,
                            "injuries": False,
                            "predictions": True,
                            "odds": False,
                        },
                    },
                    {
                        "year": 2019,
                        "start": "2019-08-09",
                        "end": "2020-07-26",
                        "current": True,
                        "coverage": {
                            "fixtures": {
                                "events": True,
                                "lineups": True,
                                "statistics_fixtures": True,
                                "statistics_players": True,
                            },
                            "standings": True,
                            "players": True,
                            "top_scorers": True,
                            "top_assists": True,
                            "top_cards": True,
                            "injuries": True,
                            "predictions": True,
                            "odds": True,
                        },
                    },
                ],
            }
        ],
    }


@pytest.fixture
def venue_data():
    return {
        "id": 556,
        "name": "Old Trafford",
        "address": "Sir Matt Busby Way",
        "city": "Manchester",
        "country": "England",
        "capacity": 76212,
        "surface": "grass",
        "image": "https://media.api-sports.io/football/venues/556.png",
    }


@pytest.fixture
def venues_payload():
    return {
        "get": "venues",
        "parameters": {"id": "556"},
        "errors": [],
        "results": 1,
        "paging": {"current": 1, "total": 1},
        "response": [
            {
                "id": 556,
                "name": "Old Trafford",
                "address": "Sir Matt Busby Way",
                "city": "Manchester",
                "country": "England",
                "capacity": 76212,
                "surface": "grass",
                "image": "https://media.api-sports.io/football/venues/556.png",
            }
        ],
    }
