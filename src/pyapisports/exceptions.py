class APISportsError(Exception):
    pass


class RateLimitError(APISportsError):
    pass


class AuthenticationError(APISportsError):
    pass
