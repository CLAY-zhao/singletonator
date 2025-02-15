import functools
from typing import Optional, Callable

from .registry import SingletonatorRegistry
from .utils import MethodWrapper


def singleton_extend(
        method: Optional[Callable] = None,
        identifier: str = None,
        version: int = 1
    ) -> Callable:

    def inner(func: Optional[Callable]) -> Callable:
        nonlocal identifier
        if identifier is None:
            identifier = method.__name__
        # method_wrapper = MethodWrapper(method)
        # SingletonatorRegistry.register_method(method_wrapper, identifier)
        SingletonatorRegistry.register_method(method, identifier, version)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    if method:
        return inner(method)
    return inner


def singleton_versioned(identifier: str = None, version: int = 1) -> Callable:
    
    def inner(func: Optional[Callable]) -> Callable:
        nonlocal identifier
        if identifier is None:
            identifier = func.__name__
        print("gogogo", func, version)
        SingletonatorRegistry.register_method(func, identifier, version)
        
        return func
    
    return inner        
