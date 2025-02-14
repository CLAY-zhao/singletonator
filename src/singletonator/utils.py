import inspect


def isroutines(obj: object) -> bool:
    return (inspect.isfunction(obj) 
        or inspect.ismethod(obj)
        or isinstance(obj, property)
    )


def get_members(obj):
    if isinstance(obj, type):
        obj = obj.__class__

    return inspect.getmembers(obj, predicate=isroutines)
