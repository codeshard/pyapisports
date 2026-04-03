from unittest.mock import MagicMock

from pyapisports.football.models import Status, TimezoneList
from pyapisports.football.resources import BaseResource


class TestBaseResource:
    def _make_resource(self, mock_responses: dict):
        client = MagicMock()
        client._get.side_effect = lambda endpoint, **_: mock_responses[
            endpoint
        ]
        return BaseResource(client)

    def test_get_status(self, status_data):
        resource = self._make_resource({"/status": status_data})
        status = resource.get_status()
        assert isinstance(status, Status)
        assert status.account.firstname == "John"

    def test_get_timezones(self, timezone_data):
        resource = self._make_resource({"/timezone": timezone_data})
        tz = resource.get_timezones()
        assert isinstance(tz, TimezoneList)
        assert len(tz) == 4
