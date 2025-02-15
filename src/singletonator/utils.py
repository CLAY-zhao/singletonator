import inspect


class MethodWrapper:
            
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self.func
        try:
            return lambda *args, **kwargs: self.func(instance, *args, **kwargs)
        except TypeError:
            return lambda : self.func(instance)


def isroutines(obj: object) -> bool:
    return (inspect.isfunction(obj) 
        or inspect.ismethod(obj)
        or isinstance(obj, property)
    )


def get_members(obj):
    if isinstance(obj, type):
        obj = obj.__class__

    return inspect.getmembers(obj, predicate=isroutines)
