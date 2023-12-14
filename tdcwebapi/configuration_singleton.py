from dataclasses import dataclass

from tdcwebapi.components.authentication.abstract import AbstractAuthentication
from tdcwebapi.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class ConfigurationSingleton(metaclass=SingletonMetaclass):
    """Configuration data shared across whole application"""
    authentication: AbstractAuthentication = None
