"""Python debug logging helpers."""
from __future__ import annotations

import functools
import inspect
import logging
from typing import Any
from typing import Callable

module_logger = logging.getLogger(__name__)

__version__ = "0.2.0"


def fucking_function(*args_d: Any, **kwargs_d: Any) -> Any:
    """Log the execution of an unfriendly function.

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
    >>> @debug_this.fucking_function(logger)
    >>> def example_function():
    ...     logger.info("This is an example function")
    >>>
    >>> example_function()
    DEBUG:__main__:  >>> example_function
    INFO:__main__:This is an example function
    DEBUG:__main__:  <<< example_function
    """
    logger: logging.Logger | None = kwargs_d.get("logger", None)

    if len(args_d) == 1 and isinstance(args_d[0], logging.Logger):
        logger = args_d[0]

    if logger is None:
        logger = module_logger

    def fucking_function_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if not inspect.isfunction(func):
            raise TypeError("This decorator must be used on a function")

        @functools.wraps(func)
        def debug_this_fucking_function(*args_f: Any, **kwargs_f: Any) -> Any:
            stack_level = len(
                [x for x in inspect.stack() if x[3] != "debug_this_fucking_function"]
            )

            assert isinstance(logger, logging.Logger)  # makes mypy happy
            logger.debug(f"{'  ' * stack_level}>>> {func.__qualname__}")
            value = func(*args_f, **kwargs_f)
            logger.debug(f"{'  ' * stack_level}<<< {func.__qualname__}")

            return value

        return debug_this_fucking_function

    if len(args_d) == 1 and callable(args_d[0]):
        return fucking_function_decorator(args_d[0])
    else:
        return fucking_function_decorator
