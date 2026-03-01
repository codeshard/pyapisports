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
