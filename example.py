# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
from __future__ import annotations

import logging

import debug_this

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@debug_this.fucking_function(print_parent=True)
def example_function() -> None:
    logger.info("This is an example function")


@debug_this.fucking_class(logger)
class ExampleClass:
    def __init__(self) -> None:
        logger.info("This is an example class constructor")
        ExampleClass.example_static_method(self)

    def example_method(self) -> None:
        logger.info("This is an example class method")
        example_function()

    @staticmethod
    def example_static_method(example_class: ExampleClass) -> None:
        logger.info("This is an example class static method")
        example_class.example_method()


if __name__ == "__main__":
    ExampleClass()
