from pyapisports.models import Country, CountryList


class TestCountry:
    def test_from_api(self, country_data):
        c = Country.from_api(country_data)
        assert c.name == "England"
        assert c.code == "GB"
        assert c.flag == "https://flag.example.com/gb.svg"

    def test_from_api_optional_fields_missing(self):
        c = Country.from_api({"name": "Unknown"})
        assert c.name == "Unknown"
        assert c.code is None
        assert c.flag is None

    def test_to_dict(self, country_data):
        c = Country.from_api(country_data)
        d = c.to_dict()
        assert d == {
            "name": "England",
            "code": "GB",
            "flag": "https://flag.example.com/gb.svg",
        }

    def test_to_json(self, country_data):
        c = Country.from_api(country_data)
        import json

        parsed = json.loads(c.to_json())
        assert parsed["name"] == "England"


class TestCountryList:
    def test_from_api_length(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        assert len(cl) == 3

    def test_iteration(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        names = [c.name for c in cl]
        assert names == ["England", "France", "Germany"]

    def test_getitem(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        assert cl[0].name == "England"

    def test_find_by_name_found(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        c = cl.find_by_name("france")
        assert c is not None
        assert c.code == "FR"

    def test_find_by_name_case_insensitive(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        assert cl.find_by_name("ENGLAND") is not None

    def test_find_by_name_not_found(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        assert cl.find_by_name("Brazil") is None

    def test_find_by_code_found(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        c = cl.find_by_code("de")
        assert c is not None
        assert c.name == "Germany"

    def test_find_by_code_not_found(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        assert cl.find_by_code("XX") is None

    def test_to_list(self, country_list_data):
        cl = CountryList.from_api(country_list_data)
        result = cl.to_list()
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["name"] == "England"

    def test_to_json(self, country_list_data):
        import json

        cl = CountryList.from_api(country_list_data)
        parsed = json.loads(cl.to_json())
        assert len(parsed) == 3
