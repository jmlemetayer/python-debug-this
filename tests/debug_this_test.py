"""Test cases for the `debug_this` package."""
from __future__ import annotations

import logging

import pytest

import debug_this

logger = logging.getLogger(__name__)


@debug_this.function
def _example_function() -> None:
    """Do nothing. This is an example function."""
    logger.info("This is _example_function")


@debug_this.function
def _wrapper_function() -> None:
    logger.info("This is _wrapper_function")
    _example_function()


class TestFunction:
    """Test cases related to the function helpers."""

    def test_function_decorator_basic(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated function is logged."""
        _example_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].msg.split(">>>")[0]
        assert caplog.record_tuples == [
            ("debug_this.functions", logging.DEBUG, f"{prefix}>>> _example_function"),
            ("tests.debug_this_test", logging.INFO, "This is _example_function"),
            ("debug_this.functions", logging.DEBUG, f"{prefix}<<< _example_function"),
        ]

    def test_function_decorator_name(self) -> None:
        """Check that the decorated function name is correct."""
        assert _example_function.__name__ == "_example_function"

    def test_function_decorator_doc(self) -> None:
        """Check that the decorated function doc is correct."""
        assert _example_function.__doc__ == "Do nothing. This is an example function."

    def test_function_decorator_chain(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated functions chain are logged."""
        _wrapper_function()

        assert len(caplog.records) == 6
        prefix = caplog.records[0].msg.split(">>>")[0]
        assert caplog.record_tuples == [
            ("debug_this.functions", logging.DEBUG, f"{prefix}>>> _wrapper_function"),
            ("tests.debug_this_test", logging.INFO, "This is _wrapper_function"),
            ("debug_this.functions", logging.DEBUG, f"{prefix}  >>> _example_function"),
            ("tests.debug_this_test", logging.INFO, "This is _example_function"),
            ("debug_this.functions", logging.DEBUG, f"{prefix}  <<< _example_function"),
            ("debug_this.functions", logging.DEBUG, f"{prefix}<<< _wrapper_function"),
        ]
