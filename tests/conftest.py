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


@pytest.fixture
def standings_payload():
    return {
        "get": "standings",
        "parameters": {"league": "39", "season": "2024"},
        "errors": [],
        "results": 1,
        "paging": {"current": 1, "total": 1},
        "response": [
            {
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "standings": [
                        [
                            {
                                "rank": 1,
                                "team": {
                                    "id": 50,
                                    "name": "Manchester City",
                                    "logo": "https://media.api-sports.io/football/teams/50.png",
                                },
                                "points": 91,
                                "goalsDiff": 62,
                                "group": "Premier League",
                                "form": "WWDWW",
                                "status": "same",
                                "description": "Promotion - Champions League (Group Stage)",
                                "all": {
                                    "played": 38,
                                    "win": 28,
                                    "draw": 7,
                                    "lose": 3,
                                    "goals": {"for": 96, "against": 34},
                                },
                                "home": {
                                    "played": 19,
                                    "win": 15,
                                    "draw": 3,
                                    "lose": 1,
                                    "goals": {"for": 56, "against": 18},
                                },
                                "away": {
                                    "played": 19,
                                    "win": 13,
                                    "draw": 4,
                                    "lose": 2,
                                    "goals": {"for": 40, "against": 16},
                                },
                                "update": "2024-05-19T00:00:00+00:00",
                            },
                            {
                                "rank": 2,
                                "team": {
                                    "id": 42,
                                    "name": "Arsenal",
                                    "logo": "https://media.api-sports.io/football/teams/42.png",
                                },
                                "points": 89,
                                "goalsDiff": 55,
                                "group": "Premier League",
                                "form": "WWWDW",
                                "status": "up",
                                "description": "Promotion - Champions League (Group Stage)",
                                "all": {
                                    "played": 38,
                                    "win": 28,
                                    "draw": 5,
                                    "lose": 5,
                                    "goals": {"for": 91, "against": 36},
                                },
                                "home": {
                                    "played": 19,
                                    "win": 15,
                                    "draw": 2,
                                    "lose": 2,
                                    "goals": {"for": 50, "against": 19},
                                },
                                "away": {
                                    "played": 19,
                                    "win": 13,
                                    "draw": 3,
                                    "lose": 3,
                                    "goals": {"for": 41, "against": 17},
                                },
                                "update": "2024-05-19T00:00:00+00:00",
                            },
                            {
                                "rank": 3,
                                "team": {
                                    "id": 33,
                                    "name": "Manchester United",
                                    "logo": "https://media.api-sports.io/football/teams/33.png",
                                },
                                "points": 60,
                                "goalsDiff": 3,
                                "group": "Premier League",
                                "form": "WDLWL",
                                "status": "down",
                                "description": "Promotion - Europa League (Group Stage)",
                                "all": {
                                    "played": 38,
                                    "win": 18,
                                    "draw": 6,
                                    "lose": 14,
                                    "goals": {"for": 57, "against": 54},
                                },
                                "home": {
                                    "played": 19,
                                    "win": 11,
                                    "draw": 3,
                                    "lose": 5,
                                    "goals": {"for": 33, "against": 26},
                                },
                                "away": {
                                    "played": 19,
                                    "win": 7,
                                    "draw": 3,
                                    "lose": 9,
                                    "goals": {"for": 24, "against": 28},
                                },
                                "update": "2024-05-19T00:00:00+00:00",
                            },
                            {
                                "rank": 18,
                                "team": {
                                    "id": 63,
                                    "name": "Leeds United",
                                    "logo": "https://media.api-sports.io/football/teams/63.png",
                                },
                                "points": 31,
                                "goalsDiff": -23,
                                "group": "Premier League",
                                "form": "LLDLL",
                                "status": "down",
                                "description": "Relegation - Championship",
                                "all": {
                                    "played": 38,
                                    "win": 7,
                                    "draw": 10,
                                    "lose": 21,
                                    "goals": {"for": 48, "against": 71},
                                },
                                "home": {
                                    "played": 19,
                                    "win": 5,
                                    "draw": 5,
                                    "lose": 9,
                                    "goals": {"for": 28, "against": 40},
                                },
                                "away": {
                                    "played": 19,
                                    "win": 2,
                                    "draw": 5,
                                    "lose": 12,
                                    "goals": {"for": 20, "against": 31},
                                },
                                "update": "2024-05-19T00:00:00+00:00",
                            },
                            {
                                "rank": 19,
                                "team": {
                                    "id": 55,
                                    "name": "Brentford",
                                    "logo": "https://media.api-sports.io/football/teams/55.png",
                                },
                                "points": 28,
                                "goalsDiff": -28,
                                "group": "Premier League",
                                "form": "LLLLD",
                                "status": "same",
                                "description": "Relegation - Championship",
                                "all": {
                                    "played": 38,
                                    "win": 6,
                                    "draw": 10,
                                    "lose": 22,
                                    "goals": {"for": 45, "against": 73},
                                },
                                "home": {
                                    "played": 19,
                                    "win": 4,
                                    "draw": 5,
                                    "lose": 10,
                                    "goals": {"for": 26, "against": 40},
                                },
                                "away": {
                                    "played": 19,
                                    "win": 2,
                                    "draw": 5,
                                    "lose": 12,
                                    "goals": {"for": 19, "against": 33},
                                },
                                "update": "2024-05-19T00:00:00+00:00",
                            },
                            {
                                "rank": 20,
                                "team": {
                                    "id": 57,
                                    "name": "Sheffield Utd",
                                    "logo": "https://media.api-sports.io/football/teams/57.png",
                                },
                                "points": 16,
                                "goalsDiff": -69,
                                "group": "Premier League",
                                "form": "LLLLL",
                                "status": "down",
                                "description": "Relegation - Championship",
                                "all": {
                                    "played": 38,
                                    "win": 3,
                                    "draw": 7,
                                    "lose": 28,
                                    "goals": {"for": 35, "against": 104},
                                },
                                "home": {
                                    "played": 19,
                                    "win": 2,
                                    "draw": 4,
                                    "lose": 13,
                                    "goals": {"for": 20, "against": 55},
                                },
                                "away": {
                                    "played": 19,
                                    "win": 1,
                                    "draw": 3,
                                    "lose": 15,
                                    "goals": {"for": 15, "against": 49},
                                },
                                "update": "2024-05-19T00:00:00+00:00",
                            },
                        ]
                    ],
                }
            }
        ],
    }


@pytest.fixture
def rounds_payload():
    return {
        "get": "fixtures/rounds",
        "parameters": {"league": "39", "season": "2024"},
        "errors": [],
        "results": 6,
        "response": [
            "1st Round",
            "2nd Round",
            "3rd Round",
            "4th Round",
            "5th Round",
            "6th Round",
        ],
    }


@pytest.fixture
def rounds_empty_payload():
    return {
        "get": "fixtures/rounds",
        "parameters": {"league": "39", "season": "2024"},
        "errors": [],
        "results": 0,
        "response": [],
    }


@pytest.fixture
def standings_multi_payload():
    return {
        "get": "standings",
        "parameters": {"league": "2", "season": "2024"},
        "errors": [],
        "results": 1,
        "response": [
            {
                "league": {
                    "id": 2,
                    "name": "UEFA Champions League",
                    "country": "World",
                    "logo": "https://media.api-sports.io/football/leagues/2.png",
                    "flag": None,
                    "season": 2024,
                    "standings": [
                        [
                            {
                                "rank": 1,
                                "team": {
                                    "id": 50,
                                    "name": "Manchester City",
                                    "logo": "https://media.api-sports.io/football/teams/50.png",
                                },
                                "points": 12,
                                "goalsDiff": 8,
                                "group": "Group A",
                                "form": "WWWW",
                                "status": "same",
                                "description": "Promotion - Champions League (Round of 16)",
                                "all": {
                                    "played": 4,
                                    "win": 4,
                                    "draw": 0,
                                    "lose": 0,
                                    "goals": {"for": 12, "against": 4},
                                },
                                "home": {
                                    "played": 2,
                                    "win": 2,
                                    "draw": 0,
                                    "lose": 0,
                                    "goals": {"for": 6, "against": 2},
                                },
                                "away": {
                                    "played": 2,
                                    "win": 2,
                                    "draw": 0,
                                    "lose": 0,
                                    "goals": {"for": 6, "against": 2},
                                },
                                "update": "2024-11-01T00:00:00+00:00",
                            }
                        ],
                        [
                            {
                                "rank": 1,
                                "team": {
                                    "id": 42,
                                    "name": "Arsenal",
                                    "logo": "https://media.api-sports.io/football/teams/42.png",
                                },
                                "points": 10,
                                "goalsDiff": 5,
                                "group": "Group B",
                                "form": "WWDW",
                                "status": "same",
                                "description": "Promotion - Champions League (Round of 16)",
                                "all": {
                                    "played": 4,
                                    "win": 3,
                                    "draw": 1,
                                    "lose": 0,
                                    "goals": {"for": 9, "against": 4},
                                },
                                "home": {
                                    "played": 2,
                                    "win": 2,
                                    "draw": 0,
                                    "lose": 0,
                                    "goals": {"for": 5, "against": 2},
                                },
                                "away": {
                                    "played": 2,
                                    "win": 1,
                                    "draw": 1,
                                    "lose": 0,
                                    "goals": {"for": 4, "against": 2},
                                },
                                "update": "2024-11-01T00:00:00+00:00",
                            }
                        ],
                    ],
                }
            }
        ],
    }


@pytest.fixture
def fixture_list_payload():
    return {
        "get": "fixtures",
        "parameters": {"id": "868078"},
        "errors": [],
        "results": 1,
        "paging": {"current": 1, "total": 1},
        "response": [
            {
                "fixture": {
                    "id": 868078,
                    "referee": "Anthony Taylor",
                    "timezone": "America/New_York",
                    "date": "2024-12-01T15:00:00+00:00",
                    "timestamp": 1733068800,
                    "venue": {
                        "id": 556,
                        "name": "Old Trafford",
                        "city": "Manchester",
                    },
                    "status": {
                        "long": "Match Finished",
                        "short": "FT",
                        "elapsed": 90,
                        "extra": None,
                    },
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "round": "Regular Season - 14",
                },
                "teams": {
                    "home": {
                        "id": 33,
                        "name": "Manchester United",
                        "logo": "https://media.api-sports.io/football/teams/33.png",
                        "winner": True,
                    },
                    "away": {
                        "id": 34,
                        "name": "Tottenham Hotspur",
                        "logo": "https://media.api-sports.io/football/teams/34.png",
                        "winner": False,
                    },
                },
                "goals": {"home": 2, "away": 1},
                "score": {
                    "halftime": {"home": 1, "away": 0},
                    "fulltime": {"home": 2, "away": 1},
                    "extratime": {"home": None, "away": None},
                    "penalty": {"home": None, "away": None},
                },
            }
        ],
    }


@pytest.fixture
def fixture_payload():
    return {
        "response": [
            {
                "fixture": {
                    "id": 868078,
                    "referee": "Anthony Taylor",
                    "timezone": "America/New_York",
                    "date": "2024-12-01T15:00:00+00:00",
                    "timestamp": 1733068800,
                    "venue": {
                        "id": 556,
                        "name": "Old Trafford",
                        "city": "Manchester",
                    },
                    "status": {
                        "long": "Match Finished",
                        "short": "FT",
                        "elapsed": 90,
                        "extra": None,
                    },
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "round": "Regular Season - 14",
                },
                "teams": {
                    "home": {
                        "id": 33,
                        "name": "Manchester United",
                        "logo": "https://media.api-sports.io/football/teams/33.png",
                        "winner": True,
                    },
                    "away": {
                        "id": 34,
                        "name": "Tottenham Hotspur",
                        "logo": "https://media.api-sports.io/football/teams/34.png",
                        "winner": False,
                    },
                },
                "goals": {"home": 2, "away": 1},
                "score": {
                    "halftime": {"home": 1, "away": 0},
                    "fulltime": {"home": 2, "away": 1},
                    "extratime": {"home": None, "away": None},
                    "penalty": {"home": None, "away": None},
                },
            }
        ]
    }


@pytest.fixture
def live_fixture_payload():
    return {
        "response": [
            {
                "fixture": {
                    "id": 868079,
                    "referee": None,
                    "timezone": "UTC",
                    "date": "2024-12-01T20:00:00+00:00",
                    "timestamp": 1733086800,
                    "venue": {
                        "id": 556,
                        "name": "Old Trafford",
                        "city": "Manchester",
                    },
                    "status": {
                        "long": "2nd Half",
                        "short": "2H",
                        "elapsed": 67,
                        "extra": None,
                    },
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "round": "Regular Season - 14",
                },
                "teams": {
                    "home": {
                        "id": 33,
                        "name": "Manchester United",
                        "logo": "https://x.png",
                        "winner": None,
                    },
                    "away": {
                        "id": 34,
                        "name": "Tottenham",
                        "logo": "https://y.png",
                        "winner": None,
                    },
                },
                "goals": {"home": 1, "away": 1},
                "score": {
                    "halftime": {"home": 0, "away": 1},
                    "fulltime": {"home": None, "away": None},
                    "extratime": {"home": None, "away": None},
                    "penalty": {"home": None, "away": None},
                },
            }
        ]
    }


@pytest.fixture
def scheduled_fixture_payload():
    return {
        "response": [
            {
                "fixture": {
                    "id": 868080,
                    "referee": None,
                    "timezone": "UTC",
                    "date": "2024-12-05T15:00:00+00:00",
                    "timestamp": 1733408400,
                    "venue": {
                        "id": 556,
                        "name": "Old Trafford",
                        "city": "Manchester",
                    },
                    "status": {
                        "long": "Not Started",
                        "short": "NS",
                        "elapsed": None,
                        "extra": None,
                    },
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "round": "Regular Season - 15",
                },
                "teams": {
                    "home": {
                        "id": 33,
                        "name": "Manchester United",
                        "logo": "https://x.png",
                        "winner": None,
                    },
                    "away": {
                        "id": 40,
                        "name": "Arsenal",
                        "logo": "https://y.png",
                        "winner": None,
                    },
                },
                "goals": {"home": None, "away": None},
                "score": {
                    "halftime": {"home": None, "away": None},
                    "fulltime": {"home": None, "away": None},
                    "extratime": {"home": None, "away": None},
                    "penalty": {"home": None, "away": None},
                },
            }
        ]
    }


@pytest.fixture
def cancelled_fixture_payload():
    return {
        "response": [
            {
                "fixture": {
                    "id": 868081,
                    "referee": None,
                    "timezone": "UTC",
                    "date": "2024-12-01T15:00:00+00:00",
                    "timestamp": 1733068800,
                    "venue": {
                        "id": 556,
                        "name": "Old Trafford",
                        "city": "Manchester",
                    },
                    "status": {
                        "long": "Match Cancelled",
                        "short": "CANC",
                        "elapsed": None,
                        "extra": None,
                    },
                },
                "league": {
                    "id": 39,
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/39.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "round": "Regular Season - 14",
                },
                "teams": {
                    "home": {
                        "id": 33,
                        "name": "Man Utd",
                        "logo": "https://x.png",
                        "winner": None,
                    },
                    "away": {
                        "id": 34,
                        "name": "Spurs",
                        "logo": "https://y.png",
                        "winner": None,
                    },
                },
                "goals": {"home": None, "away": None},
                "score": {
                    "halftime": {"home": None, "away": None},
                    "fulltime": {"home": None, "away": None},
                    "extratime": {"home": None, "away": None},
                    "penalty": {"home": None, "away": None},
                },
            }
        ]
    }


@pytest.fixture
def aet_fixture_payload():
    return {
        "response": [
            {
                "fixture": {
                    "id": 868082,
                    "referee": "M. Oliver",
                    "timezone": "UTC",
                    "date": "2024-12-01T17:00:00+00:00",
                    "timestamp": 1733076000,
                    "venue": {
                        "id": 556,
                        "name": "Old Trafford",
                        "city": "Manchester",
                    },
                    "status": {
                        "long": "Finished After Extra Time",
                        "short": "AET",
                        "elapsed": 120,
                        "extra": 30,
                    },
                },
                "league": {
                    "id": 2,
                    "name": "FA Cup",
                    "country": "England",
                    "logo": "https://media.api-sports.io/football/leagues/2.png",
                    "flag": "https://media.api-sports.io/flags/gb.svg",
                    "season": 2024,
                    "round": "Quarter Final",
                },
                "teams": {
                    "home": {
                        "id": 33,
                        "name": "Man Utd",
                        "logo": "https://x.png",
                        "winner": True,
                    },
                    "away": {
                        "id": 34,
                        "name": "Spurs",
                        "logo": "https://y.png",
                        "winner": False,
                    },
                },
                "goals": {"home": 3, "away": 2},
                "score": {
                    "halftime": {"home": 1, "away": 1},
                    "fulltime": {"home": 2, "away": 2},
                    "extratime": {"home": 3, "away": 2},
                    "penalty": {"home": None, "away": None},
                },
            }
        ]
    }
