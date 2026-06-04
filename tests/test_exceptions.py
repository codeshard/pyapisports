import pytest

from pyapisports.exceptions import APISportsError, AuthenticationError, RateLimitError


class TestAPISportsError:
    def test_is_exception(self):
        assert issubclass(APISportsError, Exception)

    def test_can_be_raised(self):
        with pytest.raises(APISportsError):
            raise APISportsError("Something went wrong")

    def test_message(self):
        with pytest.raises(APISportsError, match="custom error"):
            raise APISportsError("custom error")


class TestRateLimitError:
    def test_is_subclass(self):
        assert issubclass(RateLimitError, APISportsError)

    def test_can_be_raised(self):
        with pytest.raises(RateLimitError):
            raise RateLimitError("Rate limited")


class TestAuthenticationError:
    def test_is_subclass(self):
        assert issubclass(AuthenticationError, APISportsError)

    def test_can_be_raised(self):
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("Invalid key")
