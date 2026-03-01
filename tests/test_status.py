from datetime import datetime

from pyapisports.models import (
    Account,
    Requests,
    Status,
    Subscription,
)


class TestAccount:
    def test_from_api(self):
        data = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
        }
        a = Account.from_api(data)
        assert a.firstname == "John"
        assert a.lastname == "Doe"
        assert a.email == "john@example.com"


class TestSubscription:
    def test_from_api(self):
        data = {"plan": "Free", "end": "2025-12-31T00:00:00", "active": True}
        s = Subscription.from_api(data)
        assert s.plan == "Free"
        assert isinstance(s.end, datetime)
        assert s.active is True


class TestRequests:
    def test_from_api(self):
        r = Requests.from_api({"current": 50, "limit_day": 100})
        assert r.current == 50
        assert r.limit_day == 100

    def test_remaining(self):
        r = Requests(current=30, limit_day=100)
        assert r.remaining == 70

    def test_usage_percent(self):
        r = Requests(current=25, limit_day=100)
        assert r.usage_percent == 25.0

    def test_usage_percent_rounded(self):
        r = Requests(current=1, limit_day=3)
        assert r.usage_percent == 33.33


class TestStatus:
    def test_from_api(self, status_data):
        s = Status.from_api(status_data)
        assert s.account.email == "john@example.com"
        assert s.subscription.plan == "Free"
        assert s.requests.current == 50

    def test_to_dict(self, status_data):
        s = Status.from_api(status_data)
        d = s.to_dict()
        assert d["account"]["email"] == "john@example.com"
        assert d["requests"]["limit_day"] == 100

    def test_to_json(self, status_data):
        import json

        s = Status.from_api(status_data)
        parsed = json.loads(s.to_json())
        assert parsed["subscription"]["active"] is True
