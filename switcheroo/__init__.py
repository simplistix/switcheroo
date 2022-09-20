from functools import partial

def default(handler):
    handler.__switcheroo__ = default
    return handler


class handles:

    def __init__(self, case):
        self.case = case

    def __call__(self, handler):
        handler.__switcheroo__ = self.case
        return handler


def lookup(self, item):
    try:
        return self.mapping[item]
    except KeyError:
        _default = self.mapping.get(default)
        if _default is None:
            raise
        return _default


def register_decorated_handler(name, obj, type_, switch):
    case = getattr(obj, '__switcheroo__', None)
    if case:
        setattr(type_, name, staticmethod(obj))
        method = getattr(type_, name)
        switch.register(case, method)


class SwitchMeta(type):

    __getitem__ = lookup

    def __new__(cls, name, bases, attrs):
        type_ = type.__new__(cls, name, bases, attrs)
        if name != 'Switch':
            switch = Switch()
            for name, unbound in attrs.items():
                register_decorated_handler(name, unbound, type_, switch)
            for base in bases:
                for name in dir(base):
                    obj = getattr(base, name)
                    register_decorated_handler(name, obj, type_, switch)
            type_.mapping = switch.mapping
        return type_


class Switch(metaclass=SwitchMeta):

    def __init__(self, mapping=None):
        self.mapping = mapping or {}

    __getitem__ = lookup = lookup

    def register(self, case, handler, force=False):
        if case in self.mapping and not force:
            raise KeyError('{!r} already handled by {!r}'.format(
                case, self.mapping[case]
            ))
        self.mapping[case] = handler
        return handler

    def override(self, case, handler):
        self.register(case, handler, force=True)

    def handles(self, case):
        return partial(self.register, case)

    def overrides(self, case):
        return partial(self.register, case, force=True)

    @property
    def default(self):
        return partial(self.register, default)
