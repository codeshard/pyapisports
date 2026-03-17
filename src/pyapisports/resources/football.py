from __future__ import annotations

from typing import TYPE_CHECKING

from pyapisports.models import SeasonsList
from pyapisports.resources import BaseResource

if TYPE_CHECKING:
    from pyapisports.client import ApiSportsClient


class FootballResource(BaseResource):
    def __init__(self, client: ApiSportsClient):
        self._client = client

    def get_seasons(self) -> SeasonsList:
        raw = self._client._get("/leagues/seasons")
        return SeasonsList.from_api(raw)
