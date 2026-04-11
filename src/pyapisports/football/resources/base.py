from typing import TYPE_CHECKING

from pyapisports.football.models import Status, TimezoneList

if TYPE_CHECKING:
    from pyapisports.client import ApiSportsClient


class BaseResource:
    def __init__(self, client: ApiSportsClient):
        self._client = client

    def get_status(self) -> Status:
        """Retrieve the current API account status.

        Returns:
            Status: Object containing:
            - account: Account holder's name and email.
            - subscription: Active plan name, expiry date, and active flag.
            - requests: Requests used today, daily limit, and remaining count.

        Example:
            >>> status = client.resource.get_status()
            >>> status.account.email
            'john@doe.com'
            >>> status.requests.remaining
            88
            >>> status.subscription.active
            True

        API Reference:
            GET https://v3.football.api-sports.io/status
        """
        raw = self._client._get("/status")
        return Status.from_api(raw)

    def get_timezones(self) -> TimezoneList:
        """Retrieve available timezones.

        Returns:
            TimezoneList: Collection of supported timezone strings.

        Example:
            >>> timezones = client.resource.get_timezones()
            >>> timezones.to_json()

        API Reference:
            GET https://v3.football.api-sports.io/timezone
        """
        raw = self._client._get("/timezone")
        return TimezoneList.from_api(raw)
