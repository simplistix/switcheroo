from functools import partial

from six import add_metaclass


def default(handler):
    handler = staticmethod(handler)
    handler.__switcheroo__ = default
    return handler


class handles(object):

    def __init__(self, case):
        self.case = case

    def __call__(self, handler):
        handler = staticmethod(handler)
        handler.__switcheroo__ = self.case
        return handler


def __getitem__(self, item):
    try:
        return self.mapping[item]
    except KeyError:
        if self._default is None:
            raise
        return self._default


class SwitchMeta(type):

    __getitem__ = __getitem__

    def __new__(cls, name, bases, attrs):
        type_ = super().__new__(cls, name, bases, attrs)
        if name != 'Switch':
            switch = Switch()
            for name, unbound in attrs.items():
                method = getattr(type_, name)
                case = getattr(unbound, '__switcheroo__', None)
                if case is default:
                    switch._default = method
                elif case:
                    switch.register(case, method)
            type_.mapping = switch.mapping
            type_._default = switch._default
        return type_


@add_metaclass(SwitchMeta)
class Switch(object):

    def __init__(self, mapping=None):
        self.mapping = mapping or {}
        self._default = self.mapping.pop(default, None)

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
        return partial(setattr, self, '_default')
