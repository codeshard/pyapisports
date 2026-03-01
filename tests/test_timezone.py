from pyapisports.models import TimezoneList


class TestTimezoneList:
    def test_from_api(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        assert len(tz) == 4

    def test_iteration(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        assert list(tz)[0] == "Africa/Abidjan"

    def test_contains_true(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        assert "Europe/London" in tz

    def test_contains_false(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        assert "Pacific/Auckland" not in tz

    def test_search(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        results = tz.search("america")
        assert results == ["America/New_York"]

    def test_search_case_insensitive(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        results = tz.search("EUROPE")
        assert "Europe/London" in results

    def test_search_no_results(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        assert tz.search("Antarctica") == []

    def test_to_list(self, timezone_data):
        tz = TimezoneList.from_api(timezone_data)
        assert isinstance(tz.to_list(), list)
        assert len(tz.to_list()) == 4

    def test_to_json(self, timezone_data):
        import json

        tz = TimezoneList.from_api(timezone_data)
        parsed = json.loads(tz.to_json())
        assert "Asia/Tokyo" in parsed
