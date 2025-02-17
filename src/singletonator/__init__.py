from .singletonator import Singletonator
from .decorator import singleton_extend, hot_reload
from .permission import SingletonPermissionGroup


__version__ = "0.1.0"

__all__ = [
    "__version__",
    "Singletonator",
    "singleton_extend",
    "hot_reload",
    "SingletonPermissionGroup"
]
