from typing import Callable

from .utils import MethodWrapper


class SingletonatorRegistry:
    _shared_methods = {}
    
    @classmethod
    def register_method(cls, method: Callable, identifier: str = None, version: int = 1):
        if identifier in cls._shared_methods:
            if version in cls._shared_methods[identifier]:
                raise ValueError(
                    f"Method with identifier '{identifier}' already exists. "
                    f"Current version: {list(cls._shared_methods[identifier].keys())}. "
                    f"Attempted to register version: {version}."
                )
        else:
            cls._shared_methods[identifier] = {}
        
        if not isinstance(method, MethodWrapper):
            cls._shared_methods[identifier][version] = method
        else:
            setattr(cls, identifier, method)
        return method
    
    @classmethod
    def reload_shared_method(cls, method, identifier: str, version: int):
        if identifier in cls._shared_methods:
            cls._shared_methods[identifier][version] = method
    
    @classmethod
    def get_method(cls, identifier: str, version: int):
        # method = cls._shared_methods.get(identifier, None) or getattr(cls(), identifier, None)
        if identifier in cls._shared_methods and version in cls._shared_methods[identifier]:
            return cls._shared_methods[identifier][version]
        raise AttributeError(f"Method '{identifier}' with version '{version}' not found in share methods.")

    @classmethod
    def get_all_methods(cls):
        return cls._shared_methods.keys()
