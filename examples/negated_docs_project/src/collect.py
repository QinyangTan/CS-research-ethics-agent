import requests


def fetch() -> dict:
    return requests.get("https://www.reddit.com/r/example/new.json", timeout=10).json()

