Switcheroo
==========

Efficient dispatch-based calling, that might be a switch statement in another language.

short usage
~~~~~~~~~~~

.. code-block:: python

    from switcheroo import Switch

    switch = Switch({
        'foo': lambda x: x+1,
    })

>>> switch['foo'](1)
2

>>> switch['bar'](1)
Traceback (most recent call last):
...
KeyError: 'bar'

.. code-block:: python

    from switcheroo import Switch, default

    switch = Switch({
        'foo': lambda x: x+1,
        default: lambda x: x-1,
    })

>>> switch['foo'](1)
2

>>> switch['bar'](1)
0

decorator usage
~~~~~~~~~~~~~~~

.. code-block:: python

    from switcheroo import Switch

    switch = Switch()

    @switch.handles('foo')
    def handle_foo(x):
        return x+1

    @switch.default
    def handle_others(x):
        return x-1

>>> switch['foo'](1)
2

>>> switch['bar'](1)
0

class helper usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class MoarThingz(object):

        switch = Switch()

        def __init__(self, state):
            self.state = state

        @switch.handles('foo')
        def handle_foo(self, x):
            return self.state - x

        @switch.default
        def handle_foo(self, x):
            return self.state + x

        def dispatch(self, case, factor, x):
            return factor * self.switch[case](self, x)

>>> things = MoarThingz(3)
>>> things.dispatch('foo', factor=1, x=1)
2
>>> things.dispatch('bar', factor=-1, x=2)
-5

subclass usage
~~~~~~~~~~~~~~

.. code-block:: python

    from switcheroo import Switch, handles, default

    class MySwitch(Switch):

        @handles('foo')
        def handles(x):
            return x+1

        @default
        def default(x):
            return x-1

>>> MySwitch['foo'](1)
2
>>> MySwitch['bar'](1)
0
