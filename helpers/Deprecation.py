# ruff: noqa: B010
import functools
import warnings
from collections.abc import Callable
from typing import Protocol


class DeprecatedCallable[**P, R](Protocol):
    """Protocol for deprecated callable with custom attributes."""

    __deprecated__: bool
    __deprecation_reason__: str | None
    __use_instead__: str | None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


def deprecated_ecs[**P, R](
    reason: str | None = None, use_instead: str | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    ECS-specific deprecation decorator that includes version information.

    Args:
        reason: Optional reason for deprecation
        use_instead: Optional alternative function/method to use
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            msg = f"PyECS: {func.__name__} is deprecated"

            if reason:
                msg += f". {reason}"

            if use_instead:
                msg += f". Use {use_instead} instead"

            warnings.warn(msg, DeprecationWarning, stacklevel=3)
            return func(*args, **kwargs)

        setattr(wrapper, "__deprecated__", True)
        setattr(wrapper, "__deprecation_reason__", reason)
        setattr(wrapper, "__use_instead__", use_instead)

        return wrapper

    return decorator


def deprecated_external[**P, R](
    reason: str | None = None,
    use_instead: str | None = None,
    allowed_modules: list[str] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Deprecation decorator that only warns for external calls.

    Args:
        reason: Optional reason for deprecation
        use_instead: Optional alternative to suggest
        allowed_modules: List of module names that are allowed to call without warning
    """
    if allowed_modules is None:
        allowed_modules = []

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back and frame.f_back.f_back:
                globals_dict = frame.f_back.f_back.f_globals
                caller_module: str = (
                    globals_dict.get("__name__", "")
                    if isinstance(globals_dict.get("__name__"), str)
                    else ""
                )
                for allowed in allowed_modules:
                    if caller_module.startswith(allowed):
                        return func(*args, **kwargs)

            msg = f"PyECS: {func.__name__} is deprecated"

            if reason:
                msg += f". {reason}"

            if use_instead:
                msg += f". Use {use_instead} instead"

            warnings.warn(msg, DeprecationWarning, stacklevel=3)
            return func(*args, **kwargs)

        setattr(wrapper, "__deprecated__", True)
        setattr(wrapper, "__deprecation_reason__", reason)
        setattr(wrapper, "__use_instead__", use_instead)

        return wrapper

    return decorator


def warn_deprecated(message: str, use_instead: str | None = None, stacklevel: int = 3) -> None:
    """
    Issue a deprecation warning for usage patterns that can't be decorated.

    Args:
        message: The deprecation message
        use_instead: Optional alternative to suggest
        stacklevel: Stack level for warning (default 3)
    """
    msg = f"PyECS: {message}"

    if use_instead:
        msg += f". Use {use_instead} instead"

    warnings.warn(msg, DeprecationWarning, stacklevel=stacklevel)
