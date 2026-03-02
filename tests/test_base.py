from unittest.mock import MagicMock

from pyapisports.models import CountryList, Status, TimezoneList
from pyapisports.resources import BaseResource


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

    def test_get_countries_no_params(self, country_list_data):

        client = MagicMock()
        client._get.return_value = country_list_data
        resource = BaseResource(client)
        cl = resource.get_countries()
        client._get.assert_called_once_with("/countries", params={})
        assert isinstance(cl, CountryList)

    def test_get_countries_with_params(self, country_list_data):

        client = MagicMock()
        client._get.return_value = country_list_data
        resource = BaseResource(client)
        resource.get_countries(name="England", code="GB")
        client._get.assert_called_once_with(
            "/countries", params={"name": "England", "code": "GB"}
        )
