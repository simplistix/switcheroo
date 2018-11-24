from functools import partial

from six import add_metaclass


def default(handler):
    handler.__switcheroo__ = default
    return handler


class handles(object):

    def __init__(self, case):
        self.case = case

    def __call__(self, handler):
        handler.__switcheroo__ = self.case
        return handler


def __getitem__(self, item):
    try:
        return self.mapping[item]
    except KeyError:
        _default = self.mapping.get(default)
        if _default is None:
            raise
        return _default


class SwitchMeta(type):

    __getitem__ = __getitem__

    def __new__(cls, name, bases, attrs):
        type_ = type.__new__(cls, name, bases, attrs)
        if name != 'Switch':
            switch = Switch()
            for name, unbound in attrs.items():
                case = getattr(unbound, '__switcheroo__', None)
                if case:
                    setattr(type_, name, staticmethod(unbound))
                    method = getattr(type_, name)
                    switch.register(case, method)
            type_.mapping = switch.mapping
        return type_


@add_metaclass(SwitchMeta)
class Switch(object):

    def __init__(self, mapping=None):
        self.mapping = mapping or {}

    __getitem__ = __getitem__

    def register(self, case, handler):
        if case in self.mapping:
            raise KeyError('{!r} already handled by {!r}'.format(
                case, self.mapping[case]
            ))
        self.mapping[case] = handler
        return handler

    def handles(self, case):
        return partial(self.register, case)

    @property
    def default(self):
        return partial(self.register, default)
