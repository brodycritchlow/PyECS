import functools
from collections.abc import Callable
from typing import Any

from pyecs.exceptions import (
    ComponentNotFoundError,
    EntityNotFoundError,
    OperationFailedError,
)
from pyecs.helpers.Statuses import StatusCodes


def generate_unsafe[**P, R](
    exception_type: type[Exception] = OperationFailedError, error_message: str | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator that automatically generates an unsafe version of a method.

    The unsafe version raises an exception instead of returning StatusCodes.FAILURE.
    The decorated function gets a new `unsafe` attribute that is the exception-raising version.

    Usage:
        @generate_unsafe(ComponentNotFoundError, "Component not found on entity")
        def get_component(self, entity: Entity, component_type: type[Component]) -> Component | Literal[StatusCodes.FAILURE]:
            ...

        # This automatically generates:
        # Safe version: component = world.get_component(entity, Position)  # Returns FAILURE on error
        # Strict version: component = world.get_component_or_raise(entity, Position)  # Raises exception on error
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        unsafe_name = f"{func.__name__}_or_raise"

        @functools.wraps(func)
        def unsafe_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            result = func(*args, **kwargs)
            if result == StatusCodes.FAILURE:
                msg = error_message or f"{func.__name__} failed"
                raise exception_type(msg)
            return result

        setattr(func, "_unsafe_version", (unsafe_name, unsafe_wrapper))  # noqa: B010

        return func

    return decorator


def process_unsafe_methods(cls: type[Any]) -> type[Any]:
    """
    Process all methods decorated with @generate_unsafe and add their unsafe versions to the class.
    """
    for _, method in list(vars(cls).items()):
        if hasattr(method, "_unsafe_version"):
            unsafe_name, unsafe_wrapper = method._unsafe_version
            setattr(cls, unsafe_name, unsafe_wrapper)
    return cls


def auto_unsafe(cls: type[Any]) -> type[Any]:
    """
    Class decorator that automatically generates unsafe versions for all methods
    that return StatusCodes.FAILURE.

    Usage:
        @auto_unsafe
        class ECSWorld:
            def get_component(self, ...) -> Component | Literal[StatusCodes.FAILURE]:
                ...
    """
    for name, method in vars(cls).items():
        if callable(method) and hasattr(method, "__annotations__"):
            return_annotation = method.__annotations__.get("return", "")
            if "StatusCodes.FAILURE" in str(return_annotation):
                if "component" in name.lower():
                    exception = ComponentNotFoundError
                    message = f"Component operation '{name}' failed"
                elif "entity" in name.lower():
                    exception = EntityNotFoundError
                    message = f"Entity operation '{name}' failed"
                else:
                    exception = OperationFailedError
                    message = f"Operation '{name}' failed"

                decorated = generate_unsafe(exception, message)(method)
                setattr(cls, name, decorated)

    return process_unsafe_methods(cls)
