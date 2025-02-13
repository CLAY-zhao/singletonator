import inspect
from threading import Lock, current_thread, main_thread

from .color_util import COLOR


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

            COLOR.red("====== Trace Subclasses ======")
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

    @classmethod
    def add_trace(cls, obj):
        if not isinstance(obj, type):
            obj = obj.__class__
        ...


class Singletonator(metaclass=SingletonatorMeta):
    
    def _log_parameters(self, signature, bound_args):
        for param_name, param in signature.parameters.items():
            if param_name in bound_args.arguments:
                param_value = bound_args.arguments[param_name]
            else:
                param_value = param.default if param.default != inspect.Parameter.empty else "No default"
            default = param.default if param.default != inspect.Parameter.empty else 'No default'
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else type(param_value).__name__
            COLOR.blue(f"{param_name} [Type: {param_type} | Default: {default} | Value: {param_value}]")
    
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if Singletonator._trace_method and inspect.isroutine(attr):
            def traced_method(*args, **kwargs):
                signature = inspect.signature(attr)
                bound_args = signature.bind(*args, **kwargs)
                method_type = "Method" if inspect.ismethod(attr) else "Function"

                current_thread_id = current_thread()
                is_subthread = current_thread_id != main_thread()

                COLOR.red(f"============= Calling {method_type}: <{attr.__name__}> =============")
                if is_subthread:
                    COLOR.red(f"Executing in subthread: [Thread Name: {current_thread_id.name} | Thread ID: {current_thread_id.ident}]")
                else:
                    COLOR.red("Executing in main thread")

                object.__getattribute__(self, "_log_parameters")(signature, bound_args)

                result = attr(*args, **kwargs)
                return result
            
            return traced_method

        return attr
    
    def __setattr__(self, name, value):
        if isinstance(getattr(self.__class__, name, None), property):
            print("Setting property")
        super().__setattr__(name, value)
