from typing import Callable

from .utils import MethodWrapper


class SingletonatorRegistry:
    _shared_methods = {}
    
    @classmethod
    def register_method(cls, method: Callable, identifier: str = None):
        if identifier in cls._shared_methods:
            raise ValueError(f"Method with identifier '{identifier}' already exists.")
        if not isinstance(method, MethodWrapper):
            cls._shared_methods[identifier] = method
        else:
            setattr(cls, identifier, method)
        return method
    
    @classmethod
    def get_method(cls, identifier):
        method = cls._shared_methods.get(identifier, None) or getattr(cls(), identifier, None)
        return method

    @classmethod
    def get_all_methods(cls):
        return cls._shared_methods.keys()
