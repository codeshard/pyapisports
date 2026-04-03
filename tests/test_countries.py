import json

import pytest

from pyapisports.football.models import Country, CountryList

FIXTURE = {
    "response": [
        {
            "name": "England",
            "code": "GB",
            "flag": "https://media.api-sports.io/flags/gb.svg",
        },
        {
            "name": "France",
            "code": "FR",
            "flag": "https://media.api-sports.io/flags/fr.svg",
        },
        {"name": "Kosovo", "code": None, "flag": None},
    ]
}


@pytest.fixture
def country_list():
    return CountryList.from_api(FIXTURE)


class TestCountry:
    def test_from_api_fields(self):
        raw = {
            "name": "England",
            "code": "GB",
            "flag": "https://media.api-sports.io/flags/gb.svg",
        }
        c = Country.from_api(raw)
        assert c.name == "England"
        assert c.code == "GB"
        assert c.flag == "https://media.api-sports.io/flags/gb.svg"

    def test_nullable_code(self):
        c = Country.from_api({"name": "Kosovo", "code": None, "flag": None})
        assert c.code is None

    def test_nullable_flag(self):
        c = Country.from_api({"name": "Kosovo", "code": None, "flag": None})
        assert c.flag is None

    def test_to_dict(self):
        c = Country.from_api(
            {
                "name": "England",
                "code": "GB",
                "flag": "https://media.api-sports.io/flags/gb.svg",
            }
        )
        assert c.to_dict() == {
            "name": "England",
            "code": "GB",
            "flag": "https://media.api-sports.io/flags/gb.svg",
        }

    def test_to_dict_nullable(self):
        c = Country.from_api({"name": "Kosovo", "code": None, "flag": None})
        assert c.to_dict() == {"name": "Kosovo", "code": None, "flag": None}

    def test_to_json(self):
        c = Country.from_api(
            {
                "name": "England",
                "code": "GB",
                "flag": "https://media.api-sports.io/flags/gb.svg",
            }
        )
        parsed = json.loads(c.to_json())
        assert parsed["name"] == "England"
        assert parsed["code"] == "GB"


class TestCountryListConstruction:
    def test_from_api_returns_country_list(self, country_list):
        assert isinstance(country_list, CountryList)

    def test_items_are_country_instances(self, country_list):
        for c in country_list:
            assert isinstance(c, Country)

    def test_length(self, country_list):
        assert len(country_list) == 3


class TestCountryListAccess:
    def test_iterable(self, country_list):
        names = [c.name for c in country_list]
        assert names == ["England", "France", "Kosovo"]

    def test_getitem(self, country_list):
        assert country_list[0].name == "England"
        assert country_list[-1].name == "Kosovo"


class TestCountryListFinders:
    def test_find_by_name(self, country_list):
        result = country_list.find_by_name("England")
        assert result is not None
        assert result.code == "GB"

    def test_find_by_name_case_insensitive(self, country_list):
        assert country_list.find_by_name(
            "england"
        ) == country_list.find_by_name("ENGLAND")

    def test_find_by_name_not_found(self, country_list):
        assert country_list.find_by_name("Narnia") is None

    def test_find_by_code(self, country_list):
        result = country_list.find_by_code("FR")
        assert result is not None
        assert result.name == "France"

    def test_find_by_code_case_insensitive(self, country_list):
        assert country_list.find_by_code("fr") == country_list.find_by_code(
            "FR"
        )

    def test_find_by_code_not_found(self, country_list):
        assert country_list.find_by_code("ZZ") is None

    def test_find_by_code_skips_null_codes(self, country_list):
        assert country_list.find_by_code("None") is None


class TestCountryListSerialization:
    def test_to_list_returns_list_of_dicts(self, country_list):
        result = country_list.to_list()
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    def test_to_list_values(self, country_list):
        result = country_list.to_list()
        assert result[0] == {
            "name": "England",
            "code": "GB",
            "flag": "https://media.api-sports.io/flags/gb.svg",
        }

    def test_to_list_nullable(self, country_list):
        result = country_list.to_list()
        assert result[2] == {"name": "Kosovo", "code": None, "flag": None}

    def test_to_json(self, country_list):
        parsed = json.loads(country_list.to_json())
        assert isinstance(parsed, list)
        assert len(parsed) == 3
        assert parsed[1]["code"] == "FR"

    def test_to_json_kwargs(self, country_list):
        result = country_list.to_json(indent=2)
        assert "\n" in result
