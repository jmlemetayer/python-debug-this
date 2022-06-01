"""Test cases for the `debug_this` package."""
from __future__ import annotations

import logging

import pytest

import debug_this

logger = logging.getLogger(__name__)


@debug_this.function
def _example_function() -> None:
    logger.info("This is example_function")


class TestFunction:
    """Test cases related to the function helpers."""

    def test_function_decorator_basic(self, caplog: pytest.LogCaptureFixture) -> None:
        """Check that the execution of a decorated function is logged."""
        _example_function()

        assert len(caplog.records) == 3
        assert caplog.records[0].levelname == "DEBUG"
        assert caplog.records[0].msg.endswith("  >>> _example_function")
        assert caplog.records[1].levelname == "INFO"
        assert caplog.records[1].msg == "This is example_function"
        assert caplog.records[2].levelname == "DEBUG"
        assert caplog.records[2].msg.endswith("  <<< _example_function")
