from __future__ import annotations

from typing import TYPE_CHECKING

from pyapisports.models import CountryList, Status, TimezoneList

if TYPE_CHECKING:
    from pyapisports.client import ApiSportsClient


class BaseResource:
    def __init__(self, client: ApiSportsClient):
        self._client = client

    def get_status(self) -> Status:
        raw = self._client._get("/status")
        return Status.from_api(raw)

    def get_timezones(self) -> TimezoneList:
        raw = self._client._get("/timezone")
        return TimezoneList.from_api(raw)

    def get_countries(
        self,
        name: str | None = None,
        code: str | None = None,
        search: str | None = None,
    ) -> CountryList:
        params = {}
        if name:
            params["name"] = name
        if code:
            params["code"] = code
        if search:
            params["search"] = search

        raw = self._client._get("/countries", params=params)
        return CountryList.from_api(raw)
