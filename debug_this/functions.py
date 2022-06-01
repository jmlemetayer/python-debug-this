"""Function related helpers."""
from __future__ import annotations

import functools
import inspect
import logging
from typing import Any
from typing import Callable

logger = logging.getLogger(__name__)


def function(function: Callable[..., Any]) -> Callable[..., Any]:
    """Log the execution of a decorated function.

    Examples
    --------
    >>> import debug_this
    >>>
    >>> @debug_this.function
    >>> def example_function():
    ...     print("This is example_function")
    >>>
    >>> example_function()
    DEBUG:debug_this.function:  >>> example_function
    This is example_function
    DEBUG:debug_this.function:  <<< example_function
    """

    @functools.wraps(function)
    def debug_this_function(*args: Any, **kwargs: Any) -> Any:
        stack_level = len([x for x in inspect.stack() if x[3] != "debug_this_function"])

        logger.debug(f"{'  ' * stack_level}>>> {function.__qualname__}")
        value = function(*args, **kwargs)
        logger.debug(f"{'  ' * stack_level}<<< {function.__qualname__}")

        return value

    return debug_this_function
