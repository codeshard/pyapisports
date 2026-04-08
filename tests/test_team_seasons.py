from pyapisports.football.models import TeamSeasonsList


class TestTeamSeasonsList:
    def test_from_api(self, seasons_list_data):
        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert sl.seasons == [
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

    def test_to_list(self, seasons_list_data):
        sl = TeamSeasonsList.from_api(seasons_list_data)
        assert isinstance(sl.to_list(), list)
        assert len(sl.to_list()) == 12

    def test_to_json(self, seasons_list_data):
        import json

        sl = TeamSeasonsList.from_api(seasons_list_data)
        parsed = json.loads(sl.to_json())
        assert 2020 in parsed
