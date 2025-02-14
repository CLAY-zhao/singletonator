import inspect


class MethodWrapper:
            
    def __init__(self, func):
        self.func = func
        self.owner = None
        self.name = None

    def __set_name__(self, owner, name):
        self.owner = owner
        print(f"Class '{owner.__name__}' assigned method '{name}'")
    
    def __get__(self, instance, owner):
        print(instance, owner)
        if instance is None:
            return self.func
        return lambda *args, **kwargs: self.func(instance, *args, **kwargs)
    
    def __set__(self, instance, value):
        print(f"__set__ called with instance: {instance}, value: {value}")
        if self.owner is None:
            self.owner = instance.__class__
            self.name = value.__name__ if hasattr(value, "__name__") else "unknown"
            print(f"Manually set owner: {self.owner}, name: {self.name}")


def isroutines(obj: object) -> bool:
    return (inspect.isfunction(obj) 
        or inspect.ismethod(obj)
        or isinstance(obj, property)
    )


def get_members(obj):
    if isinstance(obj, type):
        obj = obj.__class__

    return inspect.getmembers(obj, predicate=isroutines)
