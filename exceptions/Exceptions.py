class PyECSError(Exception):
    """Base exception for all PyECS errors."""

    pass


class EntityNotFoundError(PyECSError):
    """Raised when an entity doesn't exist."""

    pass


class ComponentNotFoundError(PyECSError):
    """Raised when a component doesn't exist on an entity."""

    pass


class OperationFailedError(PyECSError):
    """Raised when an ECS operation fails."""

    pass