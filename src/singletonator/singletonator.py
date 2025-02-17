from threading import Lock

from .registry import SingletonatorRegistry
from .color_util import COLOR
from .decorator import MethodWrapper


def recursive_subclasses(subclasses: list, tab: int = 2) -> None:
    for obj in subclasses:
        COLOR.green(f"{' ' * tab}↑ {obj.__name__}")
        subclass_list = obj.__subclasses__()
        if subclass_list:
            recursive_subclasses(subclass_list, tab + 2)


class SingletonatorMeta(type):

    _instance = {}
    _lock = Lock()
    _subclasses = []
    _print_subclasses = False
    _trace_method = False

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    instance = super().__call__(*args, **kwargs)
                    instance._trace_method = cls._trace_method
                    cls._instance[cls] = instance
        return cls._instance[cls]
    
    def __init__(cls, name, bases, attr):
        if bases and Singletonator in bases:
            cls._subclasses.append(cls)
            if cls._print_subclasses:
                print(f"Class '{name}' inherits from Singletonator.")
                cls.print_subclasses()
                
    @classmethod
    def print_subclasses(cls, recursive: bool = False, verbose: bool = False, show_list: bool = False):
        """
            参数:
                recursive (bool, 可选): 是否输出所有继承子类
                verbose (bool, 可选): 是否打印所有类、子类更详细的信息
                show_list (bool, 可选): 快速查看子类列表, 而不需要额外的递归或详细信息。如果为True, 则忽略 `recursive` 和 `verbose` 参数
        """
        if cls._subclasses:
            if show_list:
                return print(list(map(lambda x: x.__name__, cls._subclasses)))

            for subclass in cls._subclasses:
                subclasses = subclass.__subclasses__()
                if len(subclasses) > 0:
                    COLOR.blue(f"- {subclass.__name__} (*{len(subclasses)})")
                else:
                    COLOR.blue(f"- {subclass.__name__}")

                if recursive:
                    recursive_subclasses(subclasses, 2)
            print()
        else:
            print("No subclasses found for Singletonator.")
    
    @classmethod
    def set_print_subclasses(cls, enabled: bool = True):
        """设置是否打印子类的开关"""
        cls._print_subclasses = enabled

    @classmethod
    def set_trace_method(cls, enabled: bool = True):
        cls._trace_method = enabled


class Singletonator(metaclass=SingletonatorMeta):

    def call_share(self, alias, *args, version=1, **kwargs):
        share_method = SingletonatorRegistry.get_method(alias, version)
        if not share_method:
            raise AttributeError(f"No shared method found with alias '{alias}', version: '{version}'")
        if isinstance(share_method, MethodWrapper):
            return share_method(*args, **kwargs)
        return share_method(*args, **kwargs)
    
    def call_sequence(self, *call):
        pass
    
    def get_share_method(self):
        return SingletonatorRegistry.get_all_methods()
    
    def reload_share_method(self, method, alias):
        SingletonatorRegistry.reload_shared_method(method, alias)
