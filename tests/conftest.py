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


@pytest.fixture
def teams_payload():
    return {
        "get": "teams",
        "parameters": {"league": "39", "season": "2024"},
        "errors": [],
        "results": 3,
        "response": [
            {
                "team": {
                    "id": 33,
                    "name": "Manchester United",
                    "code": "MUN",
                    "country": "England",
                    "founded": 1878,
                    "national": False,
                    "logo": "https://media.api-sports.io/football/teams/33.png",
                },
                "venue": {
                    "id": 556,
                    "name": "Old Trafford",
                    "address": "Sir Matt Busby Way",
                    "city": "Manchester",
                    "capacity": 76212,
                    "surface": "grass",
                    "image": "https://media.api-sports.io/football/venues/556.png",
                },
            },
            {
                "team": {
                    "id": 40,
                    "name": "Liverpool",
                    "code": "LIV",
                    "country": "England",
                    "founded": 1892,
                    "national": False,
                    "logo": "https://media.api-sports.io/football/teams/40.png",
                },
                "venue": {
                    "id": 741,
                    "name": "Anfield",
                    "address": "Anfield Road",
                    "city": "Liverpool",
                    "capacity": 53394,
                    "surface": "grass",
                    "image": "https://media.api-sports.io/football/venues/741.png",
                },
            },
            {
                "team": {
                    "id": 99,
                    "name": "AZ Alkmaar",
                    "code": None,
                    "country": None,
                    "founded": None,
                    "national": True,
                    "logo": "https://media.api-sports.io/football/teams/99.png",
                },
                "venue": None,
            },
        ],
    }


@pytest.fixture
def teams_statistics_payload():
    return {
        "get": "teams/statistics",
        "parameters": {"league": "39", "season": "2024", "team": "33"},
        "errors": [],
        "results": 1,
        "response": {
            "league": {
                "id": 39,
                "name": "Premier League",
                "country": "England",
                "logo": "https://media.api-sports.io/football/leagues/39.png",
                "flag": "https://media.api-sports.io/flags/gb.svg",
                "season": 2024,
            },
            "team": {
                "id": 33,
                "name": "Manchester United",
                "logo": "https://media.api-sports.io/football/teams/33.png",
            },
            "form": "WDLWW",
            "fixtures": {
                "played": {"home": 19, "away": 19, "total": 38},
                "wins": {"home": 10, "away": 7, "total": 17},
                "draws": {"home": 4, "away": 5, "total": 9},
                "loses": {"home": 5, "away": 7, "total": 12},
            },
            "goals": {
                "for": {
                    "total": {"home": 30, "away": 22, "total": 52},
                    "average": {"home": "1.6", "away": "1.2", "total": "1.4"},
                    "minute": {
                        "0-15": {"total": 5, "percentage": "9.6%"},
                        "16-30": {"total": 8, "percentage": "15.4%"},
                        "31-45": {"total": 7, "percentage": "13.5%"},
                        "46-60": {"total": 10, "percentage": "19.2%"},
                        "61-75": {"total": 9, "percentage": "17.3%"},
                        "76-90": {"total": 8, "percentage": "15.4%"},
                        "91-105": {"total": 4, "percentage": "7.7%"},
                        "106-120": {"total": 1, "percentage": "1.9%"},
                    },
                },
                "against": {
                    "total": {"home": 20, "away": 28, "total": 48},
                    "average": {"home": "1.1", "away": "1.5", "total": "1.3"},
                    "minute": {
                        "0-15": {"total": 3, "percentage": "6.3%"},
                        "16-30": {"total": 6, "percentage": "12.5%"},
                        "31-45": {"total": 5, "percentage": "10.4%"},
                        "46-60": {"total": 8, "percentage": "16.7%"},
                        "61-75": {"total": 10, "percentage": "20.8%"},
                        "76-90": {"total": 9, "percentage": "18.8%"},
                        "91-105": {"total": 5, "percentage": "10.4%"},
                        "106-120": {"total": 2, "percentage": "4.2%"},
                    },
                },
            },
            "biggest": {
                "streak": {"wins": 4, "draws": 2, "loses": 3},
                "wins": {"home": "4-0", "away": "3-0"},
                "loses": {"home": "1-3", "away": "0-4"},
                "goals": {
                    "for": {"home": 4, "away": 3, "total": None},
                    "against": {"home": 3, "away": 4, "total": None},
                },
            },
            "clean_sheet": {"home": 8, "away": 5, "total": 13},
            "failed_to_score": {"home": 3, "away": 6, "total": 9},
            "penalty": {
                "scored": {"total": 7, "percentage": "87.5%"},
                "missed": {"total": 1, "percentage": "12.5%"},
                "total": 8,
            },
            "lineups": [
                {"formation": "4-2-3-1", "played": 22},
                {"formation": "4-3-3", "played": 10},
                {"formation": "3-4-3", "played": 6},
            ],
            "cards": {
                "yellow": {
                    "0-15": {"total": 2, "percentage": "4.5%"},
                    "16-30": {"total": 5, "percentage": "11.4%"},
                    "31-45": {"total": 6, "percentage": "13.6%"},
                    "46-60": {"total": 8, "percentage": "18.2%"},
                    "61-75": {"total": 9, "percentage": "20.5%"},
                    "76-90": {"total": 10, "percentage": "22.7%"},
                    "91-105": {"total": 4, "percentage": "9.1%"},
                    "106-120": {"total": 0, "percentage": "0%"},
                },
                "red": {
                    "0-15": {"total": 0, "percentage": "0%"},
                    "16-30": {"total": 0, "percentage": "0%"},
                    "31-45": {"total": 1, "percentage": "33.3%"},
                    "46-60": {"total": 0, "percentage": "0%"},
                    "61-75": {"total": 1, "percentage": "33.3%"},
                    "76-90": {"total": 1, "percentage": "33.3%"},
                    "91-105": {"total": 0, "percentage": "0%"},
                    "106-120": {"total": 0, "percentage": "0%"},
                },
            },
        },
    }
