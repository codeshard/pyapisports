import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Account:
    firstname: str
    lastname: str
    email: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Account":
        return cls(
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
        )


@dataclass
class Subscription:
    plan: str
    end: datetime
    active: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Subscription":
        return cls(
            plan=data["plan"],
            end=datetime.fromisoformat(data["end"]),
            active=data["active"],
        )


@dataclass
class Requests:
    current: int
    limit_day: int

    @property
    def remaining(self) -> int:
        return self.limit_day - self.current

    @property
    def usage_percent(self) -> float:
        return round((self.current / self.limit_day) * 100, 2)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Requests":
        return cls(
            current=data["current"],
            limit_day=data["limit_day"],
        )


@dataclass
class Status:
    account: Account
    subscription: Subscription
    requests: Requests

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Status":
        response = data["response"]
        return cls(
            account=Account.from_api(response["account"]),
            subscription=Subscription.from_api(response["subscription"]),
            requests=Requests.from_api(response["requests"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "account": {
                "firstname": self.account.firstname,
                "lastname": self.account.lastname,
                "email": self.account.email,
            },
            "subscription": {
                "plan": self.subscription.plan,
                "end": self.subscription.end.isoformat(),
                "active": self.subscription.active,
            },
            "requests": {
                "current": self.requests.current,
                "limit_day": self.requests.limit_day,
            },
        }

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(self.to_dict(), **kwargs)
