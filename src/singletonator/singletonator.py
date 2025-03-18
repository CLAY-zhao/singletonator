import atexit
import faulthandler
import json
import sys
import traceback
import threading

from .registry import SingletonatorRegistry
from .color_util import COLOR
from .decorator import MethodWrapper
from .permission import SingletonPermissionGroup
from .exceptions import CallPermissionError
from .reporting import generate_html_report


def recursive_subclasses(subclasses: list, tab: int = 2) -> None:
    for obj in subclasses:
        COLOR.green(f"{' ' * tab}↑ {obj.__name__}")
        subclass_list = obj.__subclasses__()
        if subclass_list:
            recursive_subclasses(subclass_list, tab + 2)


class SingletonatorMeta(type):

    _instance = {}
    _lock = threading.Lock()
    _subclasses = []
    _print_subclasses = False
    _trace_method = False
    _permission_group = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    instance = super().__call__(*args, **kwargs)
                    instance._trace_method = cls._trace_method
                    instance._permission_group = cls._permission_group
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
        
    def set_permission(self, permission_group: SingletonPermissionGroup):
        self._permission_group = permission_group
    

class Singletonator(metaclass=SingletonatorMeta):
    class_permission = None

    def call_share(self, alias, *args, version=1, **kwargs):
        share_method = SingletonatorRegistry.get_method(alias, version)
        if not share_method:
            raise AttributeError(f"No shared method found with alias '{alias}', version: '{version}'")
        if isinstance(share_method, MethodWrapper):
            return share_method(*args, **kwargs)
        func = share_method["method"]
        required_permission = share_method["level"]
        if self._permission_group and not self._permission_group.has_permission(required_permission):
            raise CallPermissionError(
                f"Class '{self.__class__.__name__}' does not have permission to call '{alias}' (version {version}). "
                f"Required permission: {required_permission}"
            )
        return func(*args, **kwargs)
    
    def call_sequence(self, *call):
        pass
    
    def get_share_method(self):
        return SingletonatorRegistry.get_all_methods()
    
    def reload_share_method(self, method, alias):
        SingletonatorRegistry.reload_shared_method(method, alias)

    @classmethod
    def _generate_debug_report(cls, exception=None, exc_traceback=None, do_open=True):
        stack_trace = traceback.extract_stack()

        if exc_traceback:
            exception_trace = traceback.extract_tb(exc_traceback)
            stack_trace.extend(exception_trace)

        if not hasattr(cls, "_report"):
            cls._report = {
                "shared_methods": SingletonatorRegistry.get_all_methods(),
                # "singleton_state": vars(Singletonator) if cls._instance else None,
                "stack_trace": [],
                "exception": str(exception) if exception else None
            }
        
        for frame in stack_trace:
            cls._report["stack_trace"].append({
                "filename": frame.filename,
                "lineno": frame.lineno,
                "function": frame.name,
                "code": frame.line,
                "is_exception_frame": frame in exception_trace if exc_traceback else False
            })

        def stack_trace_report(report_dict):
            generate_html_report(report_dict, do_open=do_open)

        with open("crash.json", "w") as f:
            json.dump(cls._report, f, indent=4)

            atexit.register(stack_trace_report, cls._report)

    @classmethod
    def enable_crash_reporting(cls, do_open: bool = True):
        faulthandler.enable(file=open("crash.log", "w"))

        def global_excepthook(exc_type, exc_value, exc_traceback):
            cls._generate_debug_report(exc_value, exc_traceback)
            
            # with open("crash.log", "a") as file:
            #     file.write("Python Exception:\n")
            #     traceback.print_exception(exc_type, exc_value, exc_traceback, file=file)
            #     file.write("\nFull Stack Trace:\n")
            #     traceback.print_stack(file=file)

            sys.__excepthook__(exc_type, exc_value, exc_traceback)

        def threading_excepthook(args):
            exc_type = args.exc_type
            exc_value = args.exc_value
            exc_traceback = args.exc_traceback
            global_excepthook(exc_type, exc_value, exc_traceback)

        sys.excepthook = global_excepthook
        threading.excepthook = threading_excepthook
