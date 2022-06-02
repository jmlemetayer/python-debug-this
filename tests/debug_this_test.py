"""Test cases for the `debug_this` package."""
from __future__ import annotations

import logging

import pytest

import debug_this

logger = logging.getLogger(__name__)


@debug_this.fucking_function
def _example_function() -> None:
    """Do nothing. This is an example function."""
    logger.info("This is an example function")


@debug_this.fucking_function
def _wrapper_function() -> None:
    logger.info("This is a wrapper function")
    _example_function()


@debug_this.fucking_function(logger)
def _logger_args_function() -> None:
    logger.info("This is function with logger as argument")


@debug_this.fucking_function(logger=logger)
def _logger_kwargs_function() -> None:
    logger.info("This is function with logger as keyword argument")


class TestFunction:
    """Test cases related to the function helpers."""

    def test_fucking_function_basic(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated function is logged."""
        _example_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].msg.split(">>>")[0]
        assert caplog.record_tuples == [
            ("debug_this", logging.DEBUG, f"{prefix}>>> _example_function"),
            ("tests.debug_this_test", logging.INFO, "This is an example function"),
            ("debug_this", logging.DEBUG, f"{prefix}<<< _example_function"),
        ]

    def test_fucking_function_name(self) -> None:
        """Check that the decorated function name is correct."""
        assert _example_function.__name__ == "_example_function"

    def test_fucking_function_doc(self) -> None:
        """Check that the decorated function doc is correct."""
        assert _example_function.__doc__ == "Do nothing. This is an example function."

    def test_fucking_function_chain(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated chain are logged."""
        _wrapper_function()

        assert len(caplog.records) == 6
        prefix = caplog.records[0].msg.split(">>>")[0]
        assert caplog.record_tuples == [
            ("debug_this", logging.DEBUG, f"{prefix}>>> _wrapper_function"),
            ("tests.debug_this_test", logging.INFO, "This is a wrapper function"),
            ("debug_this", logging.DEBUG, f"{prefix}  >>> _example_function"),
            ("tests.debug_this_test", logging.INFO, "This is an example function"),
            ("debug_this", logging.DEBUG, f"{prefix}  <<< _example_function"),
            ("debug_this", logging.DEBUG, f"{prefix}<<< _wrapper_function"),
        ]

    def test_fucking_function_logger_args(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a logger using args is working."""
        _logger_args_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].msg.split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}>>> _logger_args_function",
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is function with logger as argument",
            ),
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}<<< _logger_args_function",
            ),
        ]

    def test_fucking_function_logger_kwargs(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a logger using kwargs is working."""
        _logger_kwargs_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].msg.split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}>>> _logger_kwargs_function",
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is function with logger as keyword argument",
            ),
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}<<< _logger_kwargs_function",
            ),
        ]
