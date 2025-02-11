from threading import Lock


class SingletonatorMeta(type):

    _instance = {}
    _lock = Lock()
    _subclasses = []
    _print_subclasses = False

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    instance = super().__call__(*args, **kwargs)
                    cls._instance[cls] = instance
        return cls._instance[cls]
    
    def __init__(cls, name, bases, attr):
        if bases and Singletonator in bases:
            cls._subclasses.append(cls)
            if cls._print_subclasses:
                print(f"Class '{name}' inherits from Singletonator.")
                cls.print_subclasses()
                
    @classmethod
    def print_subclasses(cls):
        if cls._subclasses:
            print("All subclasses of Singletonator:")
            for subclass in cls._subclasses:
                print(subclass.__subclasses__())
                print(f"- {subclass.__name__}")
        else:
            print("No subclasses found for Singletonator.")
    
    @classmethod
    def set_print_subclasses(cls, enabled: bool = True):
        """设置是否打印子类的开关"""
        cls._print_subclasses = enabled
        print(f"Print subclasses is {'enabled' if enabled else 'disabled'}.")


class Singletonator(metaclass=SingletonatorMeta):

    pass
