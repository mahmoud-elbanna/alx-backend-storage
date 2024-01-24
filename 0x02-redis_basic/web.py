#!/usr/bin/env python3
"""
Web cache and tracker
"""

import requests
import redis
from functools import wraps

# Establish a connection to Redis
redis_store = redis.Redis()

def count_url_access(method):
    """
    Decorator that counts how many times a URL is accessed and caches the result.
    """

    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that counts URL access, caches the result, and returns the HTML content.
        """
        # Generate the Redis keys for caching and counting
        cached_key = f"cached:{url}"
        count_key = f"count:{url}"

        # Check if the URL's HTML content is already cached in Redis
        cached_data = redis_store.get(cached_key)
        if cached_data:
            # If cached data exists, return it
            return cached_data.decode("utf-8")

        # If cached data doesn't exist, fetch the HTML content using the original method
        html_content = method(url)

        # Increment the count for the URL
        redis_store.incr(count_key)

        # Cache the HTML content in Redis with an expiration time of 10 seconds
        redis_store.set(cached_key, html_content)
        redis_store.expire(cached_key, 10)

        # Return the HTML content
        return html_content

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using an HTTP GET request.
    """
    response = requests.get(url)
    html_content = response.text
    return html_content
