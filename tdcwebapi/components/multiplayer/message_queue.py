import asyncio

from tdcwebapi.python_extensions.singleton_metaclass import SingletonMetaclass


class MessageQueueSingleton(metaclass=SingletonMetaclass):
    def __init__(self):
        self.messages = asyncio.Queue()
