from typing import Callable

from .utils import MethodWrapper


class SingletonatorRegistry:
    _shared_methods = {}
    
    @classmethod
    def register_method(cls, method: Callable, alias: str = None, version: int = 1):
        if alias in cls._shared_methods:
            if version in cls._shared_methods[alias]:
                raise ValueError(
                    f"Method with alias '{alias}' already exists. "
                    f"Current version: {list(cls._shared_methods[alias].keys())}. "
                    f"Attempted to register version: {version}."
                )
        else:
            cls._shared_methods[alias] = {}
        
        if not isinstance(method, MethodWrapper):
            cls._shared_methods[alias][version] = method
        else:
            setattr(cls, alias, method)
        return method
    
    @classmethod
    def reload_shared_method(cls, method, alias: str, version: int):
        if alias not in cls._shared_methods:
            raise ValueError(
                f"Alias '{alias}' does not exist. "
                f"Available aliases: {list(cls._shared_methods.keys())}. "
                f"To register a new alias, use the @singleton_extend decorator."
            )
        cls._shared_methods[alias][version] = method
    
    @classmethod
    def get_method(cls, alias: str, version: int):
        # method = cls._shared_methods.get(alias, None) or getattr(cls(), alias, None)
        if alias in cls._shared_methods and version in cls._shared_methods[alias]:
            return cls._shared_methods[alias][version]
        raise AttributeError(f"Method '{alias}' with version '{version}' not found in share methods.")

    @classmethod
    def get_all_methods(cls):
        return list(cls._shared_methods.keys())
