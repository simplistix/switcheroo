from testfixtures import ShouldRaise, compare

from switcheroo import Switch, handles, default


def test_no_dupes():
    switch = Switch()

    @switch.handles('foo')
    def handle_foo(x): pass

    with ShouldRaise(KeyError):
        @switch.handles('foo')
        def handle_others(x): pass


def test_subclass():
    class MySwitch(Switch):

        @handles('foo')
        def handler_1(x):
            return x+1

        @handles('bar')
        def handler_2(x):
            return x

        @default
        def the_rest(x):
            return x-1

    compare(MySwitch['foo'](1), expected=2)
    compare(MySwitch['bar'](1), expected=1)
    compare(MySwitch['baz'](1), expected=0)


def test_subclass_no_dupes():
    with ShouldRaise(KeyError):

        class MySwitch(Switch):

            @handles('foo')
            def handles_1(self, x): pass

            @handles('foo')
            def handles_2(self, x): pass
