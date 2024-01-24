#!/usr/bin/env python3
"""Module declares a redis class and methods"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    '''Decorator that counts how many times methods of Cache class are called.'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function that increments the call count and calls the decorated method.'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Decorator that stores the history of inputs and outputs for a particular function.'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function that stores the function inputs and outputs in Redis.'''
        input_args = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_args)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    '''Function that displays the history of calls of a particular function.'''
    redis_conn = redis.Redis()
    func_name = fn.__qualname__
    call_count = redis_conn.get(func_name)
    try:
        call_count = int(call_count.decode("utf-8"))
    except Exception:
        call_count = 0
    print("{} was called {} times:".format(func_name, call_count))
    inputs = redis_conn.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = redis_conn.lrange("{}:outputs".format(func_name), 0, -1)
    for input_arg, output in zip(inputs, outputs):
        try:
            input_arg = input_arg.decode("utf-8")
        except Exception:
            input_arg = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*{}) -> {}".format(func_name, input_arg, output))


class Cache:
    '''Redis cache class that stores and retrieves data.'''
    def __init__(self):
        '''Initializes the Redis connection and flushes the cache.'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores data in the cache and returns a unique key.'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''Retrieves the value associated with a key from the cache and optionally applies a conversion function.'''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''Retrieves the value associated with a key and converts it to a string.'''
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        '''Retrieves the value associated with a key and converts it to an integer.'''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
