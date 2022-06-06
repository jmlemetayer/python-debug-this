Welcome to debug_this's documentation
=====================================

.. image:: https://img.shields.io/pypi/v/debug-this
   :target: https://pypi.org/project/debug-this
.. image:: https://img.shields.io/readthedocs/python-debug-this
   :target: https://python-debug-this.readthedocs.io/en/latest
.. image:: https://img.shields.io/github/license/jmlemetayer/python-debug-this
   :target: https://github.com/jmlemetayer/python-debug-this/blob/main/LICENSE.md
.. image:: https://img.shields.io/github/workflow/status/jmlemetayer/python-debug-this/python-debug-this/main
   :target: https://github.com/jmlemetayer/python-debug-this/actions
.. image:: https://results.pre-commit.ci/badge/github/jmlemetayer/python-debug-this/main.svg
   :target: https://results.pre-commit.ci/latest/github/jmlemetayer/python-debug-this/main
.. image:: https://img.shields.io/codecov/c/gh/jmlemetayer/debug-this/main
   :target: https://codecov.io/gh/jmlemetayer/python-debug-this

*Python debug logging helpers*

Installation
------------

Using ``pip``::

    pip install debug_this

Usage
-----

The `debug_this` module export some decorators that can be used to debug your
fucking code:

:obj:`debug_this.fucking_function`
    To be used on those fucking functions that do not want to work as expected.
:obj:`debug_this.fucking_class`
    To be used on fucking classes that are... Well you know!

All these decorators can be used with or without arguments or keywords
arguments.

The available arguments are:

logger (:obj:`logging.Logger`, optional)
    Specify a logger instead of the default one.
print_parent (:obj:`bool`, optional)
    Print which function has called the decorated function.

Example
-------

>>> from __future__ import annotations
>>>
>>> import logging
>>>
>>> import debug_this
>>>
>>> logging.basicConfig(level=logging.DEBUG)
>>>
>>> logger = logging.getLogger(__name__)
>>>
>>> @debug_this.fucking_function(print_parent=True)
>>> def example_function() -> None:
...     logger.info("This is an example function")
>>>
>>> @debug_this.fucking_class(logger)
... class ExampleClass:
...     def __init__(self) -> None:
...         logger.info("This is an example class constructor")
...         ExampleClass.example_static_method(self)
...
...     def example_method(self) -> None:
...         logger.info("This is an example class method")
...         example_function()
...
...     @staticmethod
...     def example_static_method(cls: ExampleClass) -> None:
...         logger.info("This is an example class static method")
...         cls.example_method()
...
>>> if __name__ == "__main__":
...     ExampleClass()

The resulting logs should look like this::

    DEBUG:__main__:  >>> ExampleClass.__init__
    INFO:__main__:This is an example class constructor
    DEBUG:__main__:    >>> ExampleClass.example_static_method
    INFO:__main__:This is an example class static method
    DEBUG:__main__:      >>> ExampleClass.example_method
    INFO:__main__:This is an example class method
    DEBUG:debug_this:        >>> example_function (parent: example_method)
    INFO:__main__:This is an example function
    DEBUG:debug_this:        <<< example_function
    DEBUG:__main__:      <<< ExampleClass.example_method
    DEBUG:__main__:    <<< ExampleClass.example_static_method
    DEBUG:__main__:  <<< ExampleClass.__init__

License
-------

The `debug_this` module is released under the `MIT License`_

.. _`MIT License`: https://github.com/jmlemetayer/python-debug-this/blob/main/LICENSE.md

.. toctree::
   :hidden:

   Home <self>
   API <api>
