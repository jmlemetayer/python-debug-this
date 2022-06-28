"""Test cases for the `debug_this` package."""
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
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


@debug_this.fucking_function(None, True)
def _print_parent_args_function() -> None:
    logger.info("This is function with print_parent as argument")


@debug_this.fucking_function(logger=logger)
def _logger_kwargs_function() -> None:
    logger.info("This is function with logger as keyword argument")


@debug_this.fucking_function(print_parent=True)
def _print_parent_kwargs_function() -> None:
    logger.info("This is function with print_parent as keyword argument")


class TestFunction:
    """Test cases related to the function helpers."""

    def test_fucking_function_basic(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated function is logged."""
        _example_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
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
        prefix = caplog.records[0].getMessage().split(">>>")[0]
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
        prefix = caplog.records[0].getMessage().split(">>>")[0]
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

    def test_fucking_function_print_parent_args(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a print_parent using args is working."""
        _print_parent_args_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "debug_this",
                logging.DEBUG,
                (
                    f"{prefix}>>> _print_parent_args_function "
                    "(parent: test_fucking_function_print_parent_args)"
                ),
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is function with print_parent as argument",
            ),
            (
                "debug_this",
                logging.DEBUG,
                f"{prefix}<<< _print_parent_args_function",
            ),
        ]

    def test_fucking_function_logger_kwargs(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a logger using kwargs is working."""
        _logger_kwargs_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
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

    def test_fucking_function_print_parent_kwargs(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a print_parent using kwargs is working."""
        _print_parent_kwargs_function()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "debug_this",
                logging.DEBUG,
                (
                    f"{prefix}>>> _print_parent_kwargs_function "
                    "(parent: test_fucking_function_print_parent_kwargs)"
                ),
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is function with print_parent as keyword argument",
            ),
            (
                "debug_this",
                logging.DEBUG,
                f"{prefix}<<< _print_parent_kwargs_function",
            ),
        ]

    def test_fucking_function_type_error(self) -> None:
        """Check that a type error is raised when used on invalid object."""
        # pylint: disable=unused-variable
        with pytest.raises(TypeError):

            @debug_this.fucking_function
            class InvalidTypeClass:
                pass


@debug_this.fucking_class
class _ExampleClass:
    """Do nothing. This is an example class."""

    def __init__(self, chained: bool | None = None) -> None:
        logger.info("This is an example constructor")

        if chained is True:
            self.example_method()

    def example_method(self) -> None:
        logger.info("This is an example method")


@debug_this.fucking_class(logger)
class _LoggerArgsClass:
    def __init__(self) -> None:
        logger.info("This is class with logger as argument")


@debug_this.fucking_class(None, True)
class _PrintParentArgsClass:
    def __init__(self) -> None:
        logger.info("This is class with print_parent as argument")


@debug_this.fucking_class(logger=logger)
class _LoggerKwargsClass:
    def __init__(self) -> None:
        logger.info("This is class with logger as keyword argument")


@debug_this.fucking_class(print_parent=True)
class _PrintParentKwargsClass:
    def __init__(self) -> None:
        logger.info("This is class with print_parent as keyword argument")


class TestClass:
    """Test cases related to the class helpers."""

    def test_fucking_class_basic(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated class is logged."""
        _ExampleClass()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            ("debug_this", logging.DEBUG, f"{prefix}>>> _ExampleClass.__init__"),
            ("tests.debug_this_test", logging.INFO, "This is an example constructor"),
            ("debug_this", logging.DEBUG, f"{prefix}<<< _ExampleClass.__init__"),
        ]

    def test_fucking_class_name(self) -> None:
        """Check that the decorated class name is correct."""
        assert _ExampleClass.__name__ == "_ExampleClass"

    def test_fucking_class_doc(self) -> None:
        """Check that the decorated class doc is correct."""
        assert _ExampleClass.__doc__ == "Do nothing. This is an example class."

    def test_fucking_class_chain(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated chain are logged."""
        _ExampleClass(chained=True)

        assert len(caplog.records) == 6
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            ("debug_this", logging.DEBUG, f"{prefix}>>> _ExampleClass.__init__"),
            ("tests.debug_this_test", logging.INFO, "This is an example constructor"),
            (
                "debug_this",
                logging.DEBUG,
                f"{prefix}  >>> _ExampleClass.example_method",
            ),
            ("tests.debug_this_test", logging.INFO, "This is an example method"),
            (
                "debug_this",
                logging.DEBUG,
                f"{prefix}  <<< _ExampleClass.example_method",
            ),
            ("debug_this", logging.DEBUG, f"{prefix}<<< _ExampleClass.__init__"),
        ]

    def test_fucking_class_logger_args(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that specifying a logger using args is working."""
        _LoggerArgsClass()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}>>> _LoggerArgsClass.__init__",
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is class with logger as argument",
            ),
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}<<< _LoggerArgsClass.__init__",
            ),
        ]

    def test_fucking_class_print_parent_args(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a print_parent using args is working."""
        _PrintParentArgsClass()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "debug_this",
                logging.DEBUG,
                (
                    f"{prefix}>>> _PrintParentArgsClass.__init__ "
                    "(parent: test_fucking_class_print_parent_args)"
                ),
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is class with print_parent as argument",
            ),
            (
                "debug_this",
                logging.DEBUG,
                f"{prefix}<<< _PrintParentArgsClass.__init__",
            ),
        ]

    def test_fucking_class_logger_kwargs(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a logger using kwargs is working."""
        _LoggerKwargsClass()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}>>> _LoggerKwargsClass.__init__",
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is class with logger as keyword argument",
            ),
            (
                "tests.debug_this_test",
                logging.DEBUG,
                f"{prefix}<<< _LoggerKwargsClass.__init__",
            ),
        ]

    def test_fucking_class_print_parent_kwargs(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check that specifying a print_parent using kwargs is working."""
        _PrintParentKwargsClass()

        assert len(caplog.records) == 3
        prefix = caplog.records[0].getMessage().split(">>>")[0]
        assert caplog.record_tuples == [
            (
                "debug_this",
                logging.DEBUG,
                (
                    f"{prefix}>>> _PrintParentKwargsClass.__init__ "
                    "(parent: test_fucking_class_print_parent_kwargs)"
                ),
            ),
            (
                "tests.debug_this_test",
                logging.INFO,
                "This is class with print_parent as keyword argument",
            ),
            (
                "debug_this",
                logging.DEBUG,
                f"{prefix}<<< _PrintParentKwargsClass.__init__",
            ),
        ]

    def test_fucking_class_type_error(self) -> None:
        """Check that a type error is raised when used on invalid object."""
        with pytest.raises(TypeError):

            @debug_this.fucking_class
            def invalid_type_function() -> None:
                pass
