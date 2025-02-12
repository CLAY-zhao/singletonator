import functools
from typing import Optional, Callable

from singletonator import Singletonator


def inject_method(method: Optional[Callable] = None) -> Callable:
    
    def inner(func: Optional[Callable]) -> Callable:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    if method:
        return inner(method)
    return inner
