|CircleCI|_

.. |CircleCI| image:: https://circleci.com/gh/cjw296/switcheroo/tree/master.svg?style=shield
.. _CircleCI: https://circleci.com/gh/cjw296/switcheroo/tree/master

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

explicit usage
~~~~~~~~~~~~~~

.. code-block:: python

    from switcheroo import Switch

    def handle_foo(x):
        return x+1

    def handle_others(x):
        return x-1

    switch = Switch()
    switch.register('foo', handler=handle_foo)
    switch.default(handle_others)

>>> switch.lookup('foo')(1)
2

>>> switch.lookup('bar')(1)
0

>>> switch.override('foo', lambda x: x+2)
>>> switch.lookup('foo')(1)
3

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

.. code-block:: python

    @switch.overrides('foo')
    def new_handle_foo(x):
        return x+2

>>> switch['foo'](1)
3

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


changes
~~~~~~~

1.1.0 (26 Nov 2020)
-------------------

- Add support for overrides.

- Add support for more explicit usage.

1.0.0 (27 Feb 2019)
-------------------

- 100% coverage checking and automated releases.

0.2.0 (13 Dec 2018)
-------------------

- Handle subclasses when using the subclass pattern.

0.1.0 (24 Nov 2018)
-------------------

- Initial release.
