import pytest


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
