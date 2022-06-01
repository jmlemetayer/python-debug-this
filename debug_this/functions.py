"""Function related helpers."""
from __future__ import annotations

import functools
import inspect
import logging
from typing import Any
from typing import Callable

module_logger = logging.getLogger(__name__)


def function(*args: Any, **kwargs: Any) -> Any:
    """Log the execution of a decorated function.

    Parameters
    ----------
    logger: logging.Logger, optional
        Specify a logger instead of the default one.

    Examples
    --------
    >>> import logging
    >>> import debug_this
    >>>
    >>> logging.basicConfig(level=logging.DEBUG)
    >>>
    >>> logger = logging.getLogger(__name__)
    >>>
    >>> @debug_this.function(logger)
    >>> def example_function():
    ...     logger.info("This is example_function")
    >>>
    >>> example_function()
    DEBUG:__main__:  >>> example_function
    INFO:__main__:This is example_function
    DEBUG:__main__:  <<< example_function
    """
    logger: logging.Logger | None = kwargs.get("logger", None)

    if len(args) == 1 and isinstance(args[0], logging.Logger):
        logger = args[0]

    if logger is None:
        logger = module_logger

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(function)
        def debug_this_function(*args: Any, **kwargs: Any) -> Any:
            stack_level = len(
                [x for x in inspect.stack() if x[3] != "debug_this_function"]
            )

            assert isinstance(logger, logging.Logger)  # makes mypy happy
            logger.debug(f"{'  ' * stack_level}>>> {function.__qualname__}")
            value = function(*args, **kwargs)
            logger.debug(f"{'  ' * stack_level}<<< {function.__qualname__}")

            return value

        return debug_this_function

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator
