import functools
from typing import Optional, Callable

from .registry import SingletonatorRegistry
from .utils import MethodWrapper


def singleton_extend(
        method: Optional[Callable] = None,
        alias: str = None,
        version: int = 1
    ) -> Callable:

    def inner(func: Optional[Callable]) -> Callable:
        nonlocal alias
        if alias is None:
            alias = method.__name__ if method is not None else func.__name__
        SingletonatorRegistry.register_method(method or func, alias, version)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    if method:
        return inner(method)
    return inner


def hot_reload(alias: str, version: int, new_func: Optional[Callable]):
    if not alias:
        raise ValueError("Alias cannot be empty. Please provide a valid alias for the method.")
    if version < 1:
        raise ValueError(f"Version must be at least 1. Received version: {version}.")
    if new_func is None:
        raise ValueError("New function cannot be None. Please provide a valid callable function.")
    
    SingletonatorRegistry.reload_shared_method(new_func, alias, version)
