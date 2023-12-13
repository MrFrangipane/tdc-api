from dataclasses import dataclass

from tdcwebapi.components.security.abstract import AbstractSecurity
from tdcwebapi.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class ConfigurationSingleton(metaclass=SingletonMetaclass):
    """Configuration data shared across whole application"""
    security: AbstractSecurity = None
