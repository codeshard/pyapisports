# PyAPISports
[![codecov](https://codecov.io/gh/codeshard/pyapisports/branch/main/graph/badge.svg?token=e8R2FvlITQ)](https://codecov.io/gh/codeshard/pyapisports)
[![PyPI version](https://img.shields.io/pypi/v/pyapisports.svg)](https://pypi.org/project/pyapisports/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyapisports.svg)](https://pypi.org/project/pyapisports/)
![CI](https://img.shields.io/github/actions/workflow/status/codeshard/pyapisports/unit-tests.yaml)

A modern Python client for the API-Sports APIs.

This SDK provides a simple, typed interface to interact with API-Sports endpoints such as Football, Basketball, and more.

## Features

- Simple and Pythonic API
- Automatic authentication
- Context-managed client
- Structured response objects
- JSON serialization support
- Easy access to request usage and subscription information

## Installation

```bash
uv add pyapisports
```


## Quick Start

```python
from api_sports import ApiSportsClient

with ApiSportsClient(api_key="YOUR_API_KEY") as client:
    status = client.football.get_status()

    print(status.account.email)
    print(status.subscription.plan)
    print(status.subscription.active)
    print(status.subscription.end)
    print(status.requests.remaining)
    print(status.requests.usage_percent)
    print(status.to_json(indent=2))
```


## Authentication
You need an API key from API-Sports.

Create a client using your API key:
```python
client = ApiSportsClient(api_key="YOUR_API_KEY")
```

The client can also be used as a context manager:
```python
with ApiSportsClient(api_key="YOUR_API_KEY") as client:
    ...
```
This ensures proper session handling and connection cleanup.

### Example: Account Status
Retrieve information about your account, subscription, and request usage.
```python
status = client.football.get_status()
```
Example fields available:
```python
status.account.email
status.subscription.plan
status.subscription.active
status.subscription.end
status.requests.remaining
status.requests.usage_percent
```
Convert the response to JSON:
```python
status.to_json(indent=2)
```

## Response Objects
Responses are returned as structured Python objects rather than raw dictionaries.

Example:
```python
status.subscription.plan
```
instead of:
```python
status["subscription"]["plan"]
```
Benefits:
- IDE autocomplete
- Type safety
- Cleaner code

## Error Handling
Example:
```python
from api_sports import ApiSportsError

try:
    with ApiSportsClient(api_key="YOUR_API_KEY") as client:
        status = client.football.get_status()
except ApiSportsError as e:
    print(e)
```

## Supported APIs

Currently supported:
- Football

Planned support:
- Basketball
- Baseball
- Hockey
- Handball

### Development
Clone the repository:

```bash
git clone https://github.com/codeshard/pyapisports.git
cd pyapisports
```

Install dependencies:

```bash
uv sync --group dev
```

Run tests:

```bash
uv run pytest --cov --cov-branch
```

## License

MIT License
