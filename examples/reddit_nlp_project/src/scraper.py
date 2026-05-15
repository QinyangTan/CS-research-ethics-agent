"""Example Reddit collection script."""

import time

import praw
import requests


def collect_posts(subreddit: str) -> list[dict[str, str]]:
    response = requests.get(f"https://www.reddit.com/r/{subreddit}/new.json", timeout=10)
    response.raise_for_status()
    time.sleep(1)
    listing = response.json()["data"]["children"]
    return [
        {
            "username": item["data"].get("author", ""),
            "subreddit": subreddit,
            "timestamp": item["data"].get("created_utc", ""),
            "post_text": item["data"].get("selftext", ""),
            "profile_url": f"https://www.reddit.com/user/{item['data'].get('author', '')}",
        }
        for item in listing
    ]
